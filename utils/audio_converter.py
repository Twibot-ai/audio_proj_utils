import os
from pydub import AudioSegment
from pathlib import Path


def flacs2wavs(folder):
    """
    Converts flacs to wav
    :param folder: folder with audio
    """
    filelist = os.listdir(folder)
    for index, entire_fn in enumerate(filelist):
        file_name = entire_fn.split(".")[0]
        extension = entire_fn.split(".")[1]
        if extension != 'flac':
            continue
        audio = AudioSegment.from_file(folder + entire_fn, format=extension)
        audio.export(folder + file_name + ".wav", format="wav")


def flac2wav(file, dist_path, file_type):
    audio = AudioSegment.from_file(Path(file), format=file_type)
    audio.export(dist_path, format="wav")
