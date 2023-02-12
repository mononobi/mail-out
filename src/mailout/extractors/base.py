# -*- coding: utf-8 -*-

import os

import mailout


class BaseExtractor:
    """
    base extractor class.

    it provides utilities to read all the contents of a given file.
    all application extractors should be subclassed from this.
    """

    def __init__(self, file_name, create=False):
        """
        initializes an instance of `BaseExtractor`.

        :param str file_name: the file name in files directory to read its content.
        :param bool create: specifies that if a file with given name does not
                            exist, create it instead of raising an error.
        """

        root = os.path.dirname(mailout.__file__)
        self.__file_path = os.path.join(root, 'files', file_name)
        if create and not os.path.isfile(self.__file_path):
            with open(self.__file_path, mode='w') as file:
                file.write('')

        if not os.path.isfile(self.__file_path):
            raise FileNotFoundError(f'[{file_name}] does not exist in files directory.')

        self.__file_lines = []
        with open(self.__file_path) as file:
            self.__file_lines = file.readlines()

    @property
    def file_path(self):
        """
        gets the fully qualified file path.

        :rtype: str
        """

        return self.__file_path

    @property
    def file_lines(self):
        """
        gets file content as a list of lines.

        :rtype: list[str]
        """

        return list(self.__file_lines)
