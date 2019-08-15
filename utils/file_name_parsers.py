import re


def dash_parser(current_file_name: str) -> tuple:
    """
    example: 00_01_24 - Twilight - - and harmony has been maintained in equestria for generations since ().wav
    :param current_file_name: string
    :return: tuple with (emotion, noise, quote, timestamp, pony_name, file_type)
    """
    reg_result = re.search(r'(?P<timestamp>\d\d_\d\d_\d\d) - (?P<pony_name>[^\-]+) -\s?(?P<emotion>[^\-]*) '
                           r'- (?P<quote>.+?)\s?\((?P<noise>.*)\)\s?\.(?P<file_type>\w+)$', current_file_name)
    timestamp = reg_result.group('timestamp')
    emotion = reg_result.group('emotion')
    quote = reg_result.group('quote')
    pony_name = reg_result.group('pony_name')
    noise = reg_result.group('noise')
    file_type = reg_result.group('file_type')

    parts = (
        emotion,
        noise,
        quote,
        timestamp,
        pony_name,
        file_type
    )
    return parts


def snake_case_parser(current_file_name: str) -> tuple:
    """
    example: 00_03_57_Twilight_Anxious Confused_Noisy_My failsafe spell, failed!.txt
    :param current_file_name: string
    :return: tuple with (emotion, noise, quote, timestamp, pony_name, file_type)
    """
    reg_result = re.search(r'(?P<timestamp>\d\d_\d\d_\d\d)_(?P<pony_name>[^_]+)_(?P<emotion>[^_]*)_'
                           r'(?P<noise>[^_]*)_(?P<quote>.+?)\.(?P<file_type>\w+)$', current_file_name)
    timestamp = reg_result.group('timestamp')
    emotion = reg_result.group('emotion')
    quote = reg_result.group('quote')
    quote = re.sub(r'_', ' ', quote)
    pony_name = reg_result.group('pony_name')
    noise = reg_result.group('noise')
    file_type = reg_result.group('file_type')

    parts = (
        emotion,
        noise,
        quote,
        timestamp,
        pony_name,
        file_type
    )
    return parts
