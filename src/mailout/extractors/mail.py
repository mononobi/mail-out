# -*- coding: utf-8 -*-

from mailout.common import BodyTypeEnum
from mailout.extractors.base import BaseExtractor


class MailExtractor(BaseExtractor):
    """
    mail extractor class.
    """

    def __init__(self):
        """
        initializes an instance of `MailExtractor`.
        """

        super().__init__('mail.txt')
        self._email = self._extract_email()

    def _extract_email(self):
        """
        extracts email subject and body.

        :rtype: dict
        """

        if len(self.file_lines) < 3:
            raise ValueError('Invalid email structure found.')

        body_type = self.file_lines[0].rstrip()
        subject = self.file_lines[1].rstrip()
        message_data = self.file_lines[2:]
        message = ''.join(message_data).strip()

        if not body_type or body_type.isspace():
            raise ValueError('Invalid email body type found.')

        if body_type not in BodyTypeEnum.accepted_types():
            raise ValueError(f'Invalid email body type found: [{body_type}]')

        if not subject or subject.isspace():
            raise ValueError('Invalid email subject found.')

        if not message or message.isspace():
            raise ValueError('Invalid email message found.')

        return dict(subject=subject, message=message, body_type=body_type)

    @property
    def message(self):
        """
        gets the email body.

        :rtype: str
        """

        return self._email['message']

    @property
    def subject(self):
        """
        gets the email subject.

        :rtype: str
        """

        return self._email['subject']

    @property
    def body_type(self):
        """
        gets the email body type.

        :rtype: str
        """

        return self._email['body_type']
