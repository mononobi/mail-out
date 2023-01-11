# -*- coding: utf-8 -*-

from mailout.extractors.base import BaseExtractor
from mailout.settings import SEP


class TargetExtractor(BaseExtractor):
    def __init__(self):
        super().__init__('targets.txt')
        self._targets = self._extract_targets()

    def _extract_targets(self):
        targets = []
        added = []
        with open(self.file_path) as file:
            data = file.readlines()
            for item in data:
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
            raise Exception('No valid targets found.')

        return targets

    @property
    def targets(self):
        return self._targets
