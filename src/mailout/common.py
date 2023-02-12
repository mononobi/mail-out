# -*- coding: utf-8 -*-

from enum import Enum


class BodyTypeEnum(Enum):
    """
    body type enum.
    """

    TEXT = '<<-text->>'
    HTML = '<<-html->>'

    @classmethod
    def accepted_types(cls):
        """
        gets a list of all accepted body types.

        :rtype: list[str]
        """

        return cls.TEXT.value, cls.HTML.value
