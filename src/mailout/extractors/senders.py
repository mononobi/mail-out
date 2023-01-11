# -*- coding: utf-8 -*-

from mailout.extractors.base import BaseExtractor
from mailout.settings import SERVERS, SEP


class SenderExtractor(BaseExtractor):
    def __init__(self):
        super().__init__('senders.txt')
        self._senders = self._extract_senders()

    def _extract_senders(self):
        senders = []
        added = []
        with open(self.file_path) as file:
            data = file.readlines()
            for item in data:
                parts = item.split(SEP)
                if len(parts) != 2:
                    if item.rstrip() != '':
                        print(f'Invalid sender data found: {item.rstrip()}')
                    continue

                email = parts[0].rstrip()
                password = parts[1].rstrip()
                if not email or email.isspace():
                    print(f'Invalid sender email found: {item.rstrip()}')
                    continue

                if not password or password.isspace():
                    print(f'Invalid sender password found: {item.rstrip()}')
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
                senders.append(dict(email=email, password=password, server=server.lower()))

        if not senders:
            raise Exception('No valid senders found.')

        return senders

    @property
    def senders(self):
        return self._senders

    @property
    def emails(self):
        result = []
        for item in self._senders:
            result.append(item['email'])

        return result
