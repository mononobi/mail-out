# -*- coding: utf-8 -*-

from mailout.extractors.base import BaseExtractor
from mailout.settings import SEP


class SentExtractor(BaseExtractor):
    """
    sent extractor class.
    """

    def __init__(self):
        """
        initializes an instance of `SentExtractor`.
        """

        super().__init__('sent.txt', create=True)
        self._sent = self._extract_sent()

    def _extract_sent(self):
        """
        extracts sent emails.

        :rtype: dict[str, set]
        """

        result = {}
        for item in self.file_lines:
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
        """
        adds a sent item into the given container for the given sender and target.

        :param str sender: sender email address.
        :param str target: target email address.
        :param dict container: a dict containing all previous sent items.
        """

        current_items = container.setdefault(sender.lower(), set())
        current_items.add(target.lower())

    def add_sent(self, sender, target):
        """
        adds a sent item for the given sender and target.

        :param str sender: sender email address.
        :param str target: target email address.
        """

        self._add_sent(sender, target, self._sent)

        with open(self.file_path, mode='a') as file:
            file.write(f'{sender.lower()}{SEP}{target.lower()}\n')

    def is_sent(self, sender, target):
        """
        gets a value indicating that an email from sender to target has been already sent.

        :param str sender: sender email address.
        :param str target: target email address.

        :rtype: bool
        """

        current_items = self._sent.get(sender.lower(), set())
        return target.lower() in current_items

    def has_any(self):
        """
        gets a value indicating that there is any history of sent emails.

        :rtype: bool
        """

        return len(self._sent) > 0
