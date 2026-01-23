#!/usr/bin/python3
from flask import Flask, jsonify
from gpiozero import LED
from picamera import PiCamera
from time import sleep
import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Same config as onMotion_3.py
PATH_TO_PICTURE = "/home/pi/manual_foto.jpg"  # Different filename!
relais = LED(13)

frm = 'marcus.luetolf@bluewin.ch'
to = 'marcus.luetolf@bluewin.ch'
smtpHost = 'smtpauths.bluewin.ch'
smtpPort = 465
smtpUser = 'marcus.luetolf'
smtpPassword = 'gcbadRagaz256'

def get_picture():
    camera = PiCamera()
    camera.rotation = 270
    relais.on()
    camera.start_preview()
    sleep(2)
    camera.capture(PATH_TO_PICTURE, resize=(640, 480))
    camera.close()
    relais.off()
    return True

def send_email():
    mime = MIMEMultipart()
    mime['From'] = frm
    mime['To'] = to
    mime['Subject'] = Header('Manual trigger - RPi Home Bonda', 'utf-8')
    
    mime.attach(MIMEText('Manually triggered photo', 'plain', 'utf-8'))
    f = open(PATH_TO_PICTURE, 'rb')
    img = MIMEImage(f.read())
    f.close()
    mime.attach(img)
    
    smtp = smtplib.SMTP_SSL(smtpHost, smtpPort)
    smtp.login(smtpUser, smtpPassword)
    smtp.sendmail(frm, to, mime.as_string())
    smtp.quit()

@app.route('/trigger')
def trigger():
    try:
        get_picture()
        send_email()
        return jsonify({"status": "success", "message": "Photo taken and emailed"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def home():
    return """
    <h1>RPi Camera Control</h1>
    <button onclick="fetch('/trigger').then(r=>r.json()).then(d=>alert(d.message))">
        Take Photo
    </button>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
