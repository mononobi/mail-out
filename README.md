# mail-out
A simple command line client for sending emails using different email providers.

# data
You should first fill these three files with real data and then run the app:
- **files/mail.txt**: Contains the subject and body of the email to be sent. 
  it could have a {name} place holder to be replaced by each target name at runtime.
- **files/senders.txt**: Contains the email address and password of each email to be used 
  as source address. If more than one sender is provided, the email would be sent from 
  each sender to all targets.
- **files/targets.txt**: Contains the email address and name of each target to send email to it.
  the provided name would be replaced in email message if there is a {name} place holder.

# run
python3 run.py
