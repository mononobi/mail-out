# -*- coding: utf-8 -*-

from time import sleep

from mailout.client import Client
from mailout.extractors.mail import MailExtractor
from mailout.extractors.senders import SenderExtractor
from mailout.extractors.targets import TargetExtractor
from mailout.settings import SERVERS, SLEEP


class Manager:
    def __init__(self):
        print('*' * 200)
        print('Processing data...')
        self._mail_extractor = MailExtractor()
        self._sender_extractor = SenderExtractor()
        self._target_extractor = TargetExtractor()

    def _get_client(self, server_name):
        server = SERVERS.get(server_name.lower())
        if not server:
            raise Exception(f'Server [{server_name}] does not have any '
                            f'configurations in settings.')

        return Client(server['host'], server['port'])

    def _confirm(self):
        message = self._mail_extractor.message.format(name='TARGET NAME')
        print('*' * 200)
        print('You are going to send emails, please confirm these information:')
        print('*' * 100)
        print('Email Subject:')
        print(self._mail_extractor.subject)
        print('*' * 100)
        print('Email Message:')
        print(message)
        print('*' * 100)
        print('Senders Count:')
        print(len(self._sender_extractor.senders))
        print('*' * 100)
        print('Senders Addresses:')
        print(self._sender_extractor.emails)
        print('*' * 100)
        print('Targets Count:')
        print(len(self._target_extractor.targets))

        response = input('Do you confirm these information? [Y/n]\n')
        if response.strip().lower() in ('', 'y'):
            return

        print('Please review the files and try again.')
        exit(0)

    def perform(self):
        self._confirm()
        success_sent = 0
        failed_sent = 0
        failed_sender = 0
        for sender in self._sender_extractor.senders:
            try:
                print('*' * 200)
                print(f'Sending from sender [{sender["email"]}].')
                client = self._get_client(sender['server'])
                client.authenticate(sender['email'], sender['password'])
                for target in self._target_extractor.targets:
                    try:
                        print(f'Sending to target [{target["name"]}]-[{target["email"]}]')
                        message = self._mail_extractor.message.format(name=target['name'])
                        client.send(target['email'], self._mail_extractor.subject, message)
                        success_sent += 1
                        sleep(SLEEP)
                    except Exception as target_error:
                        failed_sent += 1
                        print(f'Error occurred on target [{target["email"]}]:')
                        print(str(target_error))
                        continue

                client.terminate()

            except Exception as sender_error:
                failed_sender += 1
                print(f'Error occurred on sender [{sender["email"]}]:')
                print(str(sender_error))
                continue

        print('*' * 200)
        print(f'Operation finished:')
        print(f'Emails Sent: {success_sent}')
        print(f'Emails Failed: {failed_sent}')
        print(f'Failed Senders Count: {failed_sender}')
