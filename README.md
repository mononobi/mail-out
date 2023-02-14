# mail-out
A simple command line client for sending emails using different email providers.

# features
- Sending emails from single/multiple senders to single/multiple targets.
- Supporting text or html email body.
- Circumventing the email servers rate limiting.
- Performing a single operation multiple times and only sending emails to those
  targets which have been failed in previous operations without sending a duplicate
  email from any sender to any target.
- Detailed log output during each operation.
- Adding support for any email provider just by adding its respective configs.
- Sending emails from senders with different email providers in a single operation.
- Automatically removing duplicate senders or targets.

# data
You should first fill these three files with real data and then run the app:
- **files/mail.txt**: Contains the body type, subject and body of the email to be sent. 
  It could have `{target_name}` and/or `{sender_name}` placeholders to be replaced by 
  each target and sender name at runtime.

  The body type is the first line of the file and could be either `<<-text->>` or `<<-html->>`.
- **files/senders.txt**: Contains the email address, password and optional sender name of each 
  email to be used as source address. If more than one sender is provided, the email would be 
  sent from each sender to all targets.
  The provided sender name would be replaced in email subject and message if there is a
  `{sender_name}` placeholder. 

  Note that if you don't want to provide `sender_name` in this file, you shouldn't also 
  add `{sender_name}` placeholder in `mail.txt` file, otherwise an error would be raised.
- **files/targets.txt**: Contains the email address and name of each target to send email to it.
  the provided target name would be replaced in email subject and message if there is a 
  `{target_name}` placeholder.

# servers
The app can connect to any smtp server which supports tls. 
The already available configurations support these email services:
- **Google**: gmail.com
- **Microsoft**: microsoft365.com, office365.com, outlook.com, hotmail.com, live.com, msn.com
- **Yahoo**: yahoo.com, ymail.com

You can add any other server configurations into `SERVERS` variable of `settings` module.
The app will use the correct configuration for each sender email address.

# run
python3 run.py

# two-step verification note
If your email account has two-step verification enabled, you should create an app password
for your account and use that app password in `senders.txt` file instead of your account's 
main password.

Here are the links for Google, Microsoft and Yahoo accounts app password guide, any other email 
provider would also have something similar to app passwords:

- [Google App Password](https://support.google.com/accounts/answer/185833?hl=en)
- [Microsoft App Password](https://support.microsoft.com/en-us/account-billing/using-app-passwords-with-apps-that-don-t-support-two-step-verification-5896ed9b-4263-e681-128a-a6f2979a7944)
- [Yahoo App Password](https://help.yahoo.com/kb/SLN15241.html)
