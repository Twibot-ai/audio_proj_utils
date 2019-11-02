import json
import utils.files as utils_files
import os
import utils.file_name_parsers as parsers
import utils.audio_converter as converter
import shutil


class CreateDataset:

    def __init__(self, path_to_audio, destination_path, dataset_dir_name, pony_name, noise_filter):
        self.content = []
        self.counter = 0
        self.parse_func = parsers.snake_case_parser

        if path_to_audio == 'help':
            print(self.help())
            return

        self.path_to_audio = path_to_audio
        self.prefix = pony_name[:3].upper()
        self.converted_files = destination_path + '\\' + self.prefix + '\\' + dataset_dir_name + '\\'
        self.pony_name = pony_name
        self.noise_filter = self.noise_levels_to_list(noise_filter)

    def call(self):
        if not self.validate():
            return

        utils_files.create_dir(self.converted_files)
        utils_files.create_dir(self.converted_files + 'audio\\')

        self.iterate_seasons()

        self.create_datasets()

    def iterate_seasons(self):
        for season in range(1, 10):
            season_dir = 'S' + str(season)
            for ep in range(1, 27):
                ep_dir = 's' + str(season) + 'e' + str(ep)
                print(ep_dir)

                sound_path = self.path_to_audio + '\\' + season_dir + '\\' + ep_dir

                if not utils_files.file_exist(sound_path):
                    continue

                self.convert_files(sound_path, season, ep)

    def convert_files(self, sound_path, season, episode):
        files_list = utils_files.get_files_in_path(sound_path)

        for f in files_list:

            result = self.convert_file(f)

            if result is None:
                continue

            emotion, noise, quote, timestamp, pony_name, file_type, new_name = result

            self.counter += 1
            self.content.append({
                'emotion': emotion,
                'noise': noise,
                'quote': quote,
                'timestamp': timestamp,
                'pony_name': pony_name,
                'file_type': file_type,
                'file_name': new_name,
                'season': season,
                'episode': episode
            })

    def convert_file(self, f):
        # only files
        if type(f) == list:
            return

        file_name = os.path.basename(f)

        # Skip if marked
        if self.skip_marked(file_name):
            return

        emotion, noise, quote, timestamp, pony_name, file_type = self.parse_func(file_name)

        # Skip if name isn't correct
        if self.pony_name != pony_name:
            return

        # Skip other levels of noise
        if noise not in self.noise_filter:
            return

        new_name = f'{self.prefix}_{self.counter}.wav'
        new_file_path = self.converted_files + 'audio\\' + new_name

        if file_type == 'flac':
            converter.flac2wav(f, new_file_path, file_type, frame_rate=22050, sample_width=2)
            file_type = 'wav'
        elif file_type == 'wav':
            shutil.copyfile(f, new_file_path)
        else:
            return

        print(file_name + ' => ' + new_name)

        return emotion, noise, quote, timestamp, pony_name, file_type, new_name

    def help(self):
        lines = [
            "Usage: python main.py create_dataset <path to all audio> <path to save> <end dataset dir>"
            " <pony_name> <noise level>",
            "Noise level can be: Clean, 'Very Noisy', Noisy",
            'All audio should be stored like this: S1/s1e1/*.*'
            """Example of usage: 
            python main.py create_dataset "F:\projects\pony_pre_proj\all" "F:\projects\pony_pre_proj" Deepvoice3"
            " Twilight 'Noisy,Clean,Very Noisy'"""
        ]
        return '\n'.join(lines)

    def create_datasets(self):
        self.create_deepvoice3_dataset()
        self.create_full_info_dump()
        self.create_tacatron2_dataset()

    def create_full_info_dump(self):
        json_string = json.dumps(self.content)
        utils_files.create_file(self.converted_files + 'full_dataset.json', json_string)

    def create_deepvoice3_dataset(self):
        dataset_hash = {}
        for record in self.content:
            dataset_hash['./datasets/audio/' + record['file_name']] = record['quote']

        json_string = json.dumps(dataset_hash)
        utils_files.create_file(self.converted_files + 'dataset.json', json_string)

    def create_tacatron2_dataset(self):
        # https://github.com/NVIDIA/tacotron2
        train_rows = []
        train_rows_mel = []
        train_file_names = []

        validation_rows = []
        validation_rows_mel = []
        validation_file_names = []

        index = 0
        for c in self.content:
            file_name = c['file_name'].replace('.wav', '')
            row_mel = "{file_name}.pt|{quote}".format(file_name=file_name, quote=c['quote'])
            row_wav = "{file_name}.wav|{quote}".format(file_name=file_name, quote=c['quote'])

            if index % 20 == 0:
                validation_rows.append(row_wav)
                validation_rows_mel.append(row_mel)
                validation_file_names.append(c['file_name'])
            else:
                train_rows.append(row_wav)
                train_rows_mel.append(row_mel)
                train_file_names.append(c['file_name'])
            index += 1

        utils_files.create_file(self.converted_files + 'train_taca2.txt', "\n".join(train_rows))
        utils_files.create_file(self.converted_files + 'train_mel_taca2.txt', "\n".join(train_rows_mel))
        utils_files.create_file(self.converted_files + 'train_names_taca2.txt', "|".join(train_file_names))

        utils_files.create_file(self.converted_files + 'validation_taca2.txt', "\n".join(validation_rows))
        utils_files.create_file(self.converted_files + 'validation_mel_taca2.txt', "\n".join(validation_rows_mel))
        utils_files.create_file(self.converted_files + 'validation_names_taca2.txt', "|".join(validation_file_names))

    def skip_marked(self, file_name):
        return file_name[0] == '#'

    def validate(self):

        if self.path_to_audio is None or not utils_files.file_exist(self.path_to_audio):
            return False

        if self.prefix is None:
            return False

        if self.pony_name is None:
            return False

        if self.noise_filter is None:
            return False

        return True

    def noise_levels_to_list(self, noise_filter):
        if noise_filter is None:
            return
        return noise_filter.replace('Clean', '').split(',')

