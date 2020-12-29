import os


def create_caches(caches_path: str) -> None:
    """
    The function checks existence and creates a cache folder.
    :param caches_path: a path-like string e.g. './somewhere/'
    :return: None
    """
    if not os.path.exists(caches_path):
        os.makedirs(caches_path)
