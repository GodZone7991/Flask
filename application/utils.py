import os
import json
import csv


def check_existence(caches_path: str) -> bool:
    return os.path.isfile(caches_path)


def create_caches(caches_path: str) -> None:
    """
    The function checks existence and creates a cache folder.
    :param caches_path: a path-like string e.g. './somewhere/'
    :return: None
    """
    if not os.path.exists(caches_path):
        os.makedirs(caches_path)


def write_cache(cache_file, data: dict, file_format: str = 'json') -> None:
    """
    The function writes data into a json-like file.
    :param file_format: format of a saved file: csv or json
    :param cache_file: a file object
    :param data: a json-like object, e.g. dict
    :return: None
    """
    with open(cache_file, 'w', encoding='utf-8') as file:
        if file_format == 'json':
            json.dump(data, file)
        elif file_format == 'csv':
            print(data, type(data))
            writer = csv.DictWriter(file, fieldnames=data.pop().keys())
            writer.writeheader()
            writer.writerows(data)


def read_cache(cache_file, file_format: str = 'json') -> dict:
    """
    The function reads data from a cache file.
    :param cache_file: a file object
    :return: data: a json-like object e.g. dict
    """
    with open(cache_file, 'r', encoding='utf-8') as file:
        if file_format == 'json':
            data = json.load(file)
        elif file_format == 'csv':
            data = csv.reader(file)
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


def remove_cache(cache_file):
    if os.path.exists(cache_file):
        os.remove(cache_file)
        return "File was removed"
    else:
        return "File doesn't exist"
