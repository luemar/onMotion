#!usr/bin/python3

import smtplib
import ssl
from email.mime.text import MIMEText

port = 465  # server port (SSL)
smtp = 'smtpauths.bluewin.ch'  # SMTP server
password = 'gcbadRagaz256'  # dein Passwort
user = 'marcus.luetolf'  # dein Nutzername
sender_email = 'marcus.luetolf@bluewin.ch'  # deine email
receiver_email = 'marcus.luetolf@bluewin.ch'  # Empfänger email
subject = 'von RPi Seemoeve'  # dein Betreff
# deine Nachricht
text = 'RPi Seemoeve eingeschaltet'

message = MIMEText(text, 'plain')
message['Subject'] = subject
message['From'] = sender_email
message['To'] = receiver_email

with smtplib.SMTP_SSL(smtp, port, context=ssl.create_default_context()) as server:
    server.login(user, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
