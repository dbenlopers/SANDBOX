# -*- coding: utf-8 -*-
"""
This class are preliminary work for manage config
"""
from __future__ import absolute_import
import json
import configparser


class ConfigManager(object):
    """
    Config manager for cfg file
    """
    def __init__(self, file):
        self.__load_file(file)

    def __load_file(self, file_to_open):
        """
        Load cfg file
        :param file_to_open:
        :return:
        """
        self._config = configparser.ConfigParser()
        self._config.read(file_to_open)

    def get_section(self, property_name):
        """
        Return section from a cfg file
        :param property_name:
        :return:
        """
        # if key doesn't exist, it return None by default
        return self._config[property_name]


class JSONConfigManager(ConfigManager):
    """
    Config manager for json file
    """
    def __init__(self, file):
        super().__init__(file)

    def __load_file(self, file_to_open="DefaultConfigParameters.json"):
        """
        load json file
        :param file_to_open: read by default DefaultConfigParameters
        :return:
        """
        with open(file_to_open) as json_data:
            self._config = json.load(json_data)
            json_data.close()

    def get_section(self, property_name):
        """
        Return section from json file, first level
        :param property_name:
        :return:
        """
        # if key doesn't exist, it return None by default
        return self._config.get(property_name)