# -*- coding: utf-8 -*-

# smtp with tls remote servers:

_GOOGLE = {
    'host': 'smtp.gmail.com',
    'port': 587
}

_OFFICE_365 = {
    'host': 'smtp.office365.com',
    'port': 587
}

_MSN = {
    'host': 'smtp-mail.outlook.com',
    'port': 587
}

_YAHOO = {
    'host': 'smtp.mail.yahoo.com',
    'port': 587
}

SERVERS = {
    'gmail.com': _GOOGLE,
    'microsoft365.com': _OFFICE_365,
    'office365.com': _OFFICE_365,
    'outlook.com': _OFFICE_365,
    'hotmail.com': _OFFICE_365,
    'live.com': _OFFICE_365,
    'msn.com': _MSN,
    'yahoo.com': _YAHOO,
    'ymail.com': _YAHOO
}

# separator between different parts of senders and targets in corresponding files:

SEP = '[***]'

# sleep timeout in seconds between each request:

SLEEP = 3
