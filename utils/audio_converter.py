import os
from pydub import AudioSegment
from pathlib import Path

# https://github.com/jiaaro/pydub/blob/master/API.markdown


def flacs2wavs(folder, frame_rate=None):
    """
    Converts flacs to wav
    :param folder: folder with audio
    :param frame_rate frame rate for end audio
    """
    filelist = os.listdir(folder)
    for index, entire_fn in enumerate(filelist):
        file_name = entire_fn.split(".")[0]
        extension = entire_fn.split(".")[1]
        if extension != 'flac':
            continue
        audio = AudioSegment.from_file(folder + entire_fn, format=extension)
        if frame_rate is not None:
            audio = audio.set_frame_rate(frame_rate)
        audio.export(folder + file_name + ".wav", format="wav")


def flac2wav(file, dist_path, file_type, frame_rate=None, sample_width=None):
    audio = AudioSegment.from_file(Path(file), format=file_type)
    if frame_rate is not None:
        audio = audio.set_frame_rate(frame_rate)
    if sample_width is not None:
        # https://github.com/NVIDIA/tacotron2/issues/126
        audio = audio.set_sample_width(sample_width)
    # print(audio.sample_width, audio.frame_width, audio.max)
    audio.export(dist_path, format="wav")


def audio_length(file):
    audio = AudioSegment.from_file(Path(file))
    return audio.duration_seconds
