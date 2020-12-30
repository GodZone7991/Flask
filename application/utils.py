import os
import json


def create_caches(caches_path: str) -> None:
    """
    The function checks existence and creates a cache folder.
    :param caches_path: a path-like string e.g. './somewhere/'
    :return: None
    """
    if not os.path.exists(caches_path):
        os.makedirs(caches_path)


def write_cache(cache_file, data: dict) -> None:
    """
    The function writes data into a json-like file.
    :param cache_file: a file object
    :param data: a json-like object, e.g. dict
    :return: None
    """
    with open(cache_file, 'w', encoding='utf-8') as file:
        json.dump(data, file)


def read_cache(cache_file) -> dict:
    """
    The function reads data from a cache file.
    :param cache_file: a file object
    :return: data: a json-like object e.g. dict
    """
    with open(cache_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


def add_cache_data(file, **kwargs) -> None:
    """
    The function writes accepted data to the file. The data is named parameters.
    :param file: a file object
    :param kwargs: named parameters
    :return: None
    """
    user_info = read_cache(file)
    for k, v in kwargs.items():
        user_info[k] = v
    write_cache(file, user_info)
