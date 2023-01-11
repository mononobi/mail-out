# -*- coding: utf-8 -*-

import os

import mailout


class BaseExtractor:
    def __init__(self, file_name, create=False):
        root = os.path.dirname(mailout.__file__)
        self.__file_path = os.path.join(root, 'files', file_name)
        if create and not os.path.isfile(self.__file_path):
            with open(self.__file_path, mode='w') as file:
                file.write('')

        if not os.path.isfile(self.__file_path):
            raise Exception(f'[{file_name}] does not exist in files directory.')

    @property
    def file_path(self):
        return self.__file_path
