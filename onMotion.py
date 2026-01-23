#!usr/bin/python3
from gpiozero import LED, MotionSensor
from datetime import datetime
import logging
import smtplib
from picamera import PiCamera
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pushbullet import Pushbullet
from socket import gaierror
from signal import pause
from time import sleep
import schedule

logging.basicConfig(filename='/home/pi/my_log.log',filemode='a',level=logging.INFO,\
                    format='%(message)s:%(asctime)s')

print('onMotion.py gestarted')
logging.info('onMotion.py started')

# PIR stabilization delay
print('Waiting 35 seconds for PIR to stabilize...')
logging.info('PIR stabilization: waiting 60 seconds')
sleep(35)
print('PIR ready')
logging.info('PIR ready')

time="18:30"

pir = MotionSensor(27, pull_up=False)
relais = LED(13)
led_on = LED(25)

PATH_TO_PICTURE = "/home/pi/my_foto.jpg"

frm='marcus.luetolf@bluewin.ch'
to='marcus.luetolf@bluewin.ch'
smtpHost='smtpauths.bluewin.ch'
smtpPort=465
smtpUser='marcus.luetolf'
smtpPassword='gcbadRagaz256'
subj='von RPi Home Bonda'
msg='Foto von RPi Home Bonda'


PUSHBULLET_API_KEY = "o.CZT6a02IxSwl42MOgnWNzX8qCadA9dRV"
PHONE_NUMBER = "+41797438094"
pushbullet = Pushbullet(PUSHBULLET_API_KEY)

led_on.on()

def get_picture():
    camera=PiCamera()
    camera.rotation=270
    relais.on()
    camera.start_preview()
    sleep(2)
    camera.capture(PATH_TO_PICTURE, resize=(640, 480))
    camera.close()
    relais.off()
    print('Foto gemacht')
    logging.info('Foto gemacht')

def send_email():
    mime=MIMEMultipart()
    mime['From']=frm
    mime['To']=to
    mime['Subject']=Header(subj, 'utf-8')

    mime.attach(MIMEText(msg, 'plain', 'utf-8'))
    f=open(PATH_TO_PICTURE, 'rb')
    img = MIMEImage(f.read())
    f.close()
    mime.attach(img)

    try:
        smtp=smtplib.SMTP_SSL(smtpHost, smtpPort)
        smtp.login(smtpUser, smtpPassword)
        smtp.sendmail(frm, to, mime.as_string())
        print('email gesendet')
        logging.info('email sent')
        smtp.quit()
    except gaierror:
        logging.exception("email error")

def send_sms():
    try:
        pushbullet.push_note("PIR Alert", "PIR Home Bonda aktiviert")
        print('push notification sent')
        logging.info("push notification sent")
    except Exception as e:
        logging.exception(f"pushbullet error: {e}")

last_trigger_time = None
DEBOUNCE_SECONDS = 5

def task():
    global last_trigger_time

    #Debounce check
    now = datetime.now()
    print(f'Task caled at {now}')
    logging.info(f'Task called at {now}')

    if last_trigger_time is not None:
        elapsed = (now - last_trigger_time).total_seconds()
        print(f'Time since last trigger: {elapsed:.1f}s')
        logging.info(f'Time since last trigger: {elapsed:.1f}s')
        if elapsed < DEBOUNCE_SECONDS:
            print(f'BLOCKED by debounce (need {DEBOUNCE_SECONDS}s, only {elapsed:.1f}s passed)')
            logging.info(f'BLOCKED by debounce')
            return

    # Update the trigger time BEFORE executing (in case execution takes time)
    last_trigger_time = now
    print(f'Task EXECUTING')
    logging.info('Task EXECUTING')
    
    try:   
        get_picture()
        send_email()
        send_sms()
    except Exception as e:
        logging.exception(f"Task execution error {e}")

pir.when_motion = task

schedule.every().day.at(time).do(task)

while True:
    schedule.run_pending()
    sleep(5)    
