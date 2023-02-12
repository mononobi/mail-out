# -*- coding: utf-8 -*-

from time import sleep
from smtplib import SMTPServerDisconnected, SMTPSenderRefused, SMTPConnectError, SMTPDataError

from mailout.client import Client
from mailout.extractors.mail import MailExtractor
from mailout.extractors.senders import SenderExtractor
from mailout.extractors.sent import SentExtractor
from mailout.extractors.targets import TargetExtractor
from mailout.settings import SERVERS, SLEEP


class Manager:
    """
    manager class.

    it handles the whole process of sending emails to targets.
    """

    def __init__(self):
        """
        initializes an instance of `Manager`.
        """

        print('*' * 200)
        print('Processing data...')
        self._mail_extractor = MailExtractor()
        self._sender_extractor = SenderExtractor()
        self._target_extractor = TargetExtractor()
        self._sent_extractor = SentExtractor()

    def _get_client(self, server_name):
        """
        gets a client to communicate with given email server.

        :param srt server_name: email server name from settings.

        :rtype: Client
        """

        server = SERVERS.get(server_name.lower())
        if not server:
            raise ValueError(f'Server [{server_name}] does not have any '
                             f'configurations in settings.')

        return Client(server['host'], server['port'])

    def _confirm(self):
        """
        performs interactive confirmation for sending emails.
        """

        message = self._mail_extractor.message.format(target_name='TARGET NAME',
                                                      sender_name='SENDER NAME')
        subject = self._mail_extractor.subject.format(target_name='TARGET NAME',
                                                      sender_name='SENDER NAME')

        print('*' * 200)
        print('You are going to send emails, please confirm these information:')
        print('*' * 100)
        print('Email Body Type:')
        print(self._mail_extractor.body_type)
        print('Email Subject:')
        print(subject)
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
        if self._sent_extractor.has_any():
            print('There is a "sent.txt" file available, so some targets might be ignored.')

        response = input('Do you confirm these information? [Y/n]\n')
        if response.strip().lower() in ('', 'y'):
            return

        print('Please review the files and try again.')
        exit(0)

    def _renew(self, sender, current_client=None):
        """
        renews the connection to the email server for the given sender.

        :param dict sender: a dict containing sender info.
        :param Client current_client: current client in use, if available.

        :rtype: Client
        """

        if current_client:
            current_client.terminate()

        client = self._get_client(sender['server'])
        client.authenticate(sender['email'], sender['password'])
        return client

    def perform(self):
        """
        performs the email sending operation.
        """

        self._confirm()
        success_sent = 0
        failed_sent = 0
        failed_sender = 0
        ignored_count = 0
        client = None
        for sender_index, sender in enumerate(self._sender_extractor.senders):
            try:
                print('*' * 200)
                print(f'Sending from sender [{sender_index + 1}]-[{sender["email"]}]')
                client = self._renew(sender)
                for target_index, target in enumerate(self._target_extractor.targets):
                    try:
                        if self._sent_extractor.is_sent(sender['email'], target['email']):
                            print(f'Ignoring target '
                                  f'[{target_index + 1}]-[{target["name"]}]-[{target["email"]}]')
                            ignored_count += 1
                            continue

                        print(f'Sending to target '
                              f'[{target_index + 1}]-[{target["name"]}]-[{target["email"]}]')
                        message = self._mail_extractor.message.format(target_name=target['name'],
                                                                      sender_name=sender['name'])
                        subject = self._mail_extractor.subject.format(target_name=target['name'],
                                                                      sender_name=sender['name'])
                        client.send(target['email'], subject, message,
                                    self._mail_extractor.body_type, sender['name'])
                        success_sent += 1
                        self._sent_extractor.add_sent(sender['email'], target['email'])
                        sleep(SLEEP)
                    except Exception as target_error:
                        failed_sent += 1
                        print(f'Error occurred on target '
                              f'[{target_index + 1}]-[{target["name"]}]-[{target["email"]}]:')
                        print(str(target_error))

                        if isinstance(target_error, (SMTPServerDisconnected, SMTPSenderRefused)):
                            print(f'Server [{sender["server"]}] is refusing the operation. '
                                  f'Waiting for 90 seconds...')
                            client.terminate()
                            sleep(90)
                            client = self._renew(sender, client)

                        if isinstance(target_error, SMTPDataError):
                            print(f'Your daily quota limit has been reached '
                                  f'for server [{sender["server"]}]')
                            print('Exiting...')
                            self.print_summary(success_sent, failed_sent,
                                               ignored_count, failed_sender)
                            exit(0)

                        continue

                client.terminate()

            except Exception as sender_error:
                failed_sender += 1
                print(f'Error occurred on sender [{sender_index + 1}]-[{sender["email"]}]:')
                print(str(sender_error))

                if isinstance(sender_error, SMTPConnectError):
                    print(f'Server [{sender["server"]}] has blocked the connection. '
                          f'Waiting for 90 seconds...')

                    client.terminate()
                    sleep(90)
                    client = self._renew(sender, client)
                continue

        self.print_summary(success_sent, failed_sent, ignored_count, failed_sender)

    def print_summary(self, success_sent, failed_sent, ignored_count, failed_sender):
        print('*' * 200)
        print('Operation finished:')
        print(f'Emails Sent: {success_sent}')
        print(f'Emails Failed: {failed_sent}')
        print(f'Ignored Targets Count: {ignored_count}')
        print(f'Failed Senders Count: {failed_sender}')
