# -*- coding: utf-8 -*-

import smtplib

from email.message import EmailMessage


class Client:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._client = smtplib.SMTP(host, port)
        self._sender_address = None

    def authenticate(self, sender_address, sender_pass):
        self._client.starttls()
        self._client.login(sender_address, sender_pass)
        self._sender_address = sender_address

    def send(self, target_address, subject, fromname, message):
        msg = EmailMessage()
        msg.set_charset('utf-8')
        msg.set_content(message)
        msg['Subject'] = subject
        msg['From'] = fromname
        msg['To'] = target_address
        msg.set_content(message, subtype='html')
        self._client.send_message(msg, self._sender_address, target_address)

    def terminate(self):
        try:
            self._client.quit()
        except Exception:
            pass
