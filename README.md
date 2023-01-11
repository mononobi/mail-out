# mail-out
A simple command line client for sending emails using different email providers.

# data
You should first fill these three files with real data and then run the app:
- **files/mail.txt**: Contains the subject and body of the email to be sent. 
  it could have a `{name}` placeholder to be replaced by each target name at runtime.
- **files/senders.txt**: Contains the email address and password of each email to be used 
  as source address. If more than one sender is provided, the email would be sent from 
  each sender to all targets.
- **files/targets.txt**: Contains the email address and name of each target to send email to it.
  the provided name would be replaced in email message if there is a `{name}` placeholder.

# servers
The app can connect to any smtp server which supports tls. 
The already available configurations support these email services:
- **Google**: gmail.com
- **Microsoft**: microsoft365.com, office365.com, outlook.com, hotmail.com, live.com, msn.com
- **Yahoo**: yahoo.com, ymail.com

You can add any other server configurations into `SERVERS` variable of `settings` module.
The app will use the correct configuration for each sender email address.

# features
- Sending emails from single/multiple senders to single/multiple targets.
- Circumventing the email servers rate limiting.
- Performing a single operation multiple times and only sending emails to those 
  targets which have been failed in previous operations without sending a duplicate 
  email from any sender to any target.
- Detailed log output during each operation.
- Adding support for any email provider just by adding its respective configs.
- Sending emails from senders with different email providers in a single operation.
- Automatically removing duplicate senders or targets.

# run
python3 run.py
