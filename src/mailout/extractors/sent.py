# -*- coding: utf-8 -*-

from mailout.extractors.base import BaseExtractor
from mailout.settings import SEP


class SentExtractor(BaseExtractor):
    def __init__(self):
        super().__init__('sent.txt', create=True)
        self._sent = self._extract_sent()

    def _extract_sent(self):
        result = {}
        with open(self.file_path) as file:
            data = file.readlines()
            for item in data:
                if item.strip() == '':
                    continue

                parts = item.split(SEP)
                if len(parts) != 2:
                    continue

                sender = parts[0].rstrip()
                target = parts[1].rstrip()
                if not sender or sender.isspace() or not target or target.isspace():
                    continue

                self._add_sent(sender, target, result)

        return result

    def _add_sent(self, sender, target, container):
        current_items = container.setdefault(sender.lower(), set())
        current_items.add(target.lower())

    def add_sent(self, sender, target):
        self._add_sent(sender, target, self._sent)

        with open(self.file_path, mode='a') as file:
            file.write(f'{sender.lower()}{SEP}{target}\n')

    def is_sent(self, sender, target):
        current_items = self._sent.get(sender.lower(), set())
        return target.lower() in current_items

    def has_any(self):
        return len(self._sent) > 0
