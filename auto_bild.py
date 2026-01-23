#!/usr/bin/python3
import smtplib, sys
from picamera import PiCamera
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from pushbullet import Pushbullet
import logging

logging.basicConfig(filename='/home/pi/my_log.log',\
                    filemode='w',level=logging.DEBUG,\
                    format='%(message)s:%(asctime)s')

logging.info('auto_bild.py started')
frm='marcus.luetolf@bluewin.ch'
to='marcus.luetolf@bluewin.ch'
smtpHost='smtpauths.bluewin.ch'
smtpPort=465

smtpUser='marcus.luetolf'

smtpPassword='gcbadRagaz256'
subj='von RPi Seemoeve'
msg='Foto von  Seemoeve'
fn='NoIRx.jpg'

camera=PiCamera()
print('camera objekt erstellt')
camera.capture(fn, resize=(640, 480))
print('Foto aufgenommen')
camera.close()
logging.info('crontab Foto gemacht')

mime=MIMEMultipart()
mime['From']=frm
mime['To']=to
mime['Subject']=Header(subj, 'utf-8')

mime.attach(MIMEText(msg, 'plain', 'utf-8'))
f=open(fn, 'rb')
img = MIMEImage(f.read())
f.close()
mime.attach(img)

try:
    smtp=smtplib.SMTP_SSL(smtpHost, smtpPort)
    smtp.login(smtpUser, smtpPassword)
    smtp.sendmail(frm, to, mime.as_string())
    logging.info('crontab email gesendet')
    print('email gesendet')
    smtp.quit()
except KeyboardInterrupt:
    print('Ende Program')
    sys.exit()


