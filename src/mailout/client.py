# -*- coding: utf-8 -*-

import smtplib

from email.message import EmailMessage


class Client:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._client = smtplib.SMTP(host, port)
        self._is_connected = True
        self._sender_address = None

    def authenticate(self, sender_address, sender_pass):
        if not self._is_connected:
            self._client.connect(self._host, self._port)

        self._client.starttls()
        self._client.login(sender_address, sender_pass)
        self._sender_address = sender_address

    def send(self, target_address, subject, message):
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = subject
        self._client.send_message(msg, self._sender_address, target_address)

    def terminate(self):
        self._is_connected = False
        self._client.quit()
