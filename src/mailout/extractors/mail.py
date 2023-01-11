# -*- coding: utf-8 -*-

from mailout.extractors.base import BaseExtractor


class MailExtractor(BaseExtractor):
    def __init__(self):
        super().__init__('mail.txt')
        self._email = self._extract_email()

    def _extract_email(self):
        with open(self.file_path) as file:
            data = file.readlines()
            if len(data) < 2:
                raise Exception('Invalid email structure found.')

            subject = data[0].rstrip()
            message_data = data[1:]
            message = ''.join(message_data).strip()

            if not subject or subject.isspace():
                raise Exception('Invalid email subject found.')

            if not message or message.isspace():
                raise Exception('Invalid email message found.')

        return dict(subject=subject, message=message)

    @property
    def message(self):
        return self._email['message']

    @property
    def subject(self):
        return self._email['subject']
