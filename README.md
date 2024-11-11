# auto-email
* This script automates the process of sending and receiving emails.
It sends a scheduled reminder email every day and checks for recent emails in the inbox.


## How to run
* Create a virtual environment
`python -m venv .venv`

* Install dependencies
`pip install -r requirements.txt`

* Add info to `.env`
* The info should include the senders email adress which goes into the EMAIL_ADDRESS section, the password shouldn't be your normal password rather your application-specific password. The RECIPIENT_ADDRESS and the password should also be the application-specific password of the email address.

* NOTE: You can only have an app password with 2FA enabled on your google account.

* The SMTP_SERVER and IMAP_SERVER both depend on what email you choose to send and receive from, same as the SMTP_PORT and IMAP_PORT (e.g, for Gmail SMTP, use smtp.gmail.com and port 587 for TSL or 465 for SSL.) 

* Run project
`python email_notification.py `

## Todo
* Add instructions on how to run
* Add `requirements.txt`
