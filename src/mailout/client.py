# -*- coding: utf-8 -*-

import smtplib

from email.message import EmailMessage

from mailout.common import BodyTypeEnum


class Client:
    """
    client class.

    it handles the connection and authentication to different email providers.
    """

    def __init__(self, host, port):
        """
        initializes an instance of `Client`.

        :param str host: email server host url.
        :param int port: email server port number.
        """

        self._host = host
        self._port = port
        self._client = smtplib.SMTP(host, port)
        self._sender_address = None

    def authenticate(self, sender_address, sender_pass):
        """
        authenticates the given email on the email server.

        :param str sender_address: sender email address.
        :param str sender_pass: sender email password.
        """

        self._client.starttls()
        self._client.login(sender_address, sender_pass)
        self._sender_address = sender_address

    def send(self, target_address, subject, message,
             body_type, target_name=None, sender_name=None):
        """
        sends an email to the provided target address.

        :param str target_address: target email address to send email to.
        :param str subject: email subject to be sent.
        :param str message: email message to be sent.
        :param str body_type: email body type to be sent.
                              it could be `<<-text->>` or `<<-html->>`.
        :param str target_name: target name to be added to email metadata if provided.
        :param str sender_name: sender name to be added to email metadata if provided.
        """

        msg = EmailMessage()
        msg.set_charset('utf-8')
        subtype = {}
        if body_type == BodyTypeEnum.HTML.value:
            subtype = dict(subtype='html')

        msg.set_content(message, **subtype)
        msg['Subject'] = subject

        if target_name:
            msg['To'] = f'{target_name} <{target_address}>'
        else:
            msg['To'] = target_address

        if sender_name:
            msg['From'] = f'{sender_name} <{self._sender_address}>'
        else:
            msg['From'] = self._sender_address

        self._client.send_message(msg, self._sender_address, target_address)

    def terminate(self):
        """
        terminates the connection to the email server if it's not already terminated.
        """

        try:
            self._client.quit()
        except Exception:
            pass
