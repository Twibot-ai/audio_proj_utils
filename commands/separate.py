import utils.files as utils_files
import os
import utils.file_name_parsers as parsers
import shutil


class SeparatePony:

    def __init__(self,  path_to_audio, destination_path, end_dir_name, pony_name):
        self.parse_func = parsers.snake_case_parser

        if path_to_audio == 'help':
            print(self.help())
            return

        self.path_to_audio = path_to_audio
        self.prefix = pony_name[:3].upper()
        self.converted_files = destination_path + '\\' + self.prefix + '\\' + end_dir_name + '\\'
        self.pony_name = pony_name

    def call(self):
        utils_files.create_dir(self.converted_files)
        utils_files.create_dir(self.converted_files + 'audio\\')

        self.iterate_episodes()

    def help(self):
        lines = [
            "Usage: python main.py separate <path to all audio> <path to save> <end_dir_name> <pony_name>",
            'All audio should be stored like this: S1/s1e1/*.*'
            """Example of usage: 
            python main.py separate "F:\projects\pony_pre_proj\all" "F:\projects\pony_pre_proj" twilight_folder Twilight"""
        ]
        return '\n'.join(lines)

    def iterate_episodes(self):
        for season in range(1, 10):
            season_dir = 'S' + str(season)
            for ep in range(1, 27):
                ep_dir = 's' + str(season) + 'e' + str(ep)
                print(ep_dir)

                sound_path = self.path_to_audio + '\\' + season_dir + '\\' + ep_dir

                if not utils_files.file_exist(sound_path):
                    continue

                self.copy_files(sound_path, season, ep)

    def copy_files(self, sound_path, season, ep):
        files_list = utils_files.get_files_in_path(sound_path)

        for f in files_list:
            self.copy_file(f)

    def copy_file(self, f):
        # only files
        if type(f) == list:
            return

        file_name = os.path.basename(f)

        emotion, noise, quote, timestamp, pony_name, file_type = self.parse_func(file_name)

        # Skip if name isn't correct
        if self.pony_name != pony_name:
            return

        new_name = f'{file_name}.{file_type}'
        new_file_path = self.converted_files + 'audio\\' + new_name

        shutil.copyfile(f, new_file_path)

        print(file_name + ': copied!')
