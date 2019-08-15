import os


def get_files_in_path(dir_path):
    """
    generates recursively list of all files in dir_path
    :param dir_path:
    :return:
    """
    files = []
    full_list = os.scandir(dir_path)

    for f in full_list:
        if os.path.isfile(f):
            files.append(f)
        else:
            to_merge = get_files_in_path(os.path.abspath(f))
            files.append(to_merge)

    return files


def file_exist(path):
    return os.path.exists(path)


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_base_name(f):
    os.path.basename(f)
