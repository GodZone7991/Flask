import os
import json
import csv


def create_caches(caches_path: str) -> None:
    """
    The function checks existence and creates a cache folder.
    :param caches_path: a path-like string e.g. './somewhere/'
    :return: None
    """
    if not os.path.exists(caches_path):
        os.makedirs(caches_path)


class UserCache:
    """
    A service class for handling user's cache
    """

    def __init__(self, user_id: str, cache_path: str = '.telegram_caches/'):
        self.user_id = user_id
        self.cache_file = ''.join([cache_path, user_id])

    @property
    def cached_data(self) -> dict:
        """
        The method reads data from a cache file.
        :return: data: a json-like object e.g. dict
        """
        with open(self.cache_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data

    def write_cache(self, data: dict) -> None:
        """
        The method writes data into a json-like file.
        :param data: a json-like object, e.g. dict
        :return: None
        """
        with open(self.cache_file, 'w', encoding='utf-8') as file:
            json.dump(data, file)

    def is_exist(self) -> bool:
        return os.path.isfile(self.cache_file)

    def update_cache(self, **kwargs) -> None:
        """
        The method writes accepted data to the file. The data is named parameters.
        :param kwargs: named parameters
        :return: None
        """
        caching_data = self.cached_data
        for k, v in kwargs.items():
            caching_data[k] = v
        self.write_cache(caching_data)

    def remove_cache(self) -> str:
        """
        The method removes cache file and returns a name of removed file.
        :return: str: a string with a name of file
        """
        file = self.cache_file
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
            return f"File {file} was removed"
        else:
            return f"File {file} doesn't exist"


def check_existence(caches_path: str) -> bool:
    return os.path.isfile(caches_path)


def write_file(file, data: dict, file_format: str = 'json') -> None:
    """
    The function writes data into a json-like file.
    :param file_format: format of a saved file: csv or json
    :param file: a file object
    :param data: a json-like object, e.g. dict
    :return: None
    """
    with open(file, 'w', encoding='utf-8') as file:
        if file_format == 'json':
            json.dump(data, file)
        elif file_format == 'csv':
            print(data, type(data))
            writer = csv.DictWriter(file, fieldnames=data.pop().keys())
            writer.writeheader()
            writer.writerows(data)
