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
            converter.flac2wav(f, new_file_path, file_type)
            file_type = 'wav'
        elif file_type == 'wav':
            shutil.copyfile(f, new_file_path)
        else:
            return

        print(file_name + ' => ' + new_name)

        return emotion, noise, quote, timestamp, pony_name, file_type, new_name

    def help(self):
        lines = [
            "Usage: python main.py create_dataset <path to all audio> <path to save> <pony_name> <noise level>",
            "Noise level can be: Clean, 'Very Noisy', Noisy",
            'All audio should be stored like this: S1/s1e1/*.*'
            """Example of usage: 
            python main.py create_dataset "F:\projects\pony_pre_proj\all" "F:\projects\pony_pre_proj" Twilight 'Noisy,Clean,Very Noisy'"""
        ]
        return '\n'.join(lines)

    def create_datasets(self):
        json_file = open(self.converted_files + 'full_dataset.json', 'w+')

        json_string = json.dumps(self.content)
        json_file.write(json_string)
        json_file.close()

        json_for_dataset = open(self.converted_files + 'dataset.json', 'w+')
        dataset_hash = {}
        for record in self.content:
            dataset_hash['./datasets/audio/' + record['file_name']] = record['quote']
        json_string = json.dumps(dataset_hash)
        json_for_dataset.write(json_string)
        json_for_dataset.close()

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

