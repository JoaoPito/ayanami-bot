import os

def create_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def join_path_with_filename(path, filename):
    return os.path.join(path, filename)