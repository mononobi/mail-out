# -*- coding: utf-8 -*-

from mailout.extractors.base import BaseExtractor
from mailout.settings import SEP


class TargetExtractor(BaseExtractor):
    """
    target extractor class.
    """

    def __init__(self):
        """
        initializes an instance of `TargetExtractor`.
        """

        super().__init__('targets.txt')
        self._targets = self._extract_targets()

    def _extract_targets(self):
        """
        extracts email targets.

        :rtype: list[dict]
        """

        targets = []
        added = []
        for item in self.file_lines:
            parts = item.split(SEP)
            if len(parts) != 2:
                if item.rstrip() != '':
                    print(f'Invalid target data found: {item.rstrip()}')
                continue

            email = parts[0].rstrip()
            name = parts[1].rstrip()
            if not email or email.isspace():
                print(f'Invalid target email found: {item.rstrip()}')
                continue

            if not name or name.isspace():
                print(f'Invalid target name found: {item.rstrip()}')
                continue

            if email.lower() in added:
                print(f'Target address [{email}] is duplicate.')
                continue

            added.append(email.lower())
            targets.append(dict(email=email, name=name))

        if not targets:
            raise ValueError('No valid targets found.')

        return targets

    @property
    def targets(self):
        """
        gets a list of all email targets.

        :rtype: list[dict]
        """

        return self._targets
