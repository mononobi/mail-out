# -*- coding: utf-8 -*-

from mailout.extractors.base import BaseExtractor
from mailout.settings import SERVERS, SEP


class SenderExtractor(BaseExtractor):
    """
    sender extractor class.
    """

    def __init__(self):
        """
        initializes an instance of `SenderExtractor`.
        """

        super().__init__('senders.txt')
        self._senders = self._extract_senders()

    def _extract_senders(self):
        """
        extracts email senders.

        :rtype: list[dict]
        """

        senders = []
        added = []
        for item in self.file_lines:
            parts = item.split(SEP)
            if len(parts) not in (2, 3):
                if item.rstrip() != '':
                    print(f'Invalid sender data found: {item.rstrip()}')
                continue

            email = parts[0].rstrip()
            password = parts[1].rstrip()
            name = None
            if len(parts) == 3:
                name = parts[2].rstrip()

            if not email or email.isspace():
                print(f'Invalid sender email found: {item.rstrip()}')
                continue

            if not password or password.isspace():
                print(f'Invalid sender password found: {item.rstrip()}')
                continue

            if name is not None and (not name or name.isspace()):
                print(f'Invalid sender name found: {item.rstrip()}')
                continue

            if email.lower() in added:
                print(f'Sender address [{email}] is duplicate.')
                continue

            email_parts = email.split('@')
            if len(email_parts) != 2:
                print(f'Invalid sender email found: [{email}]')
                continue

            server = email_parts[1]
            if server.lower() not in SERVERS:
                print(f'Server [{server}] does not have any '
                      f'configurations in settings.')
                continue

            added.append(email.lower())
            senders.append(dict(email=email,
                                password=password,
                                name=name,
                                server=server.lower()))

        if not senders:
            raise ValueError('No valid senders found.')

        return senders

    @property
    def senders(self):
        """
        gets a list of all email senders.

        :rtype: list[dict]
        """

        return self._senders

    @property
    def emails(self):
        """
        gets a list of all senders email addresses.

        :rtype: list[str]
        """

        result = []
        for item in self._senders:
            result.append(item['email'])

        return result
