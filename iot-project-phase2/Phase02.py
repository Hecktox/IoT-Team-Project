'''
Maximus Taube
IoT Project Phase02
'''

import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT
import smtplib
import imaplib
import email

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
Motor1 = 15  # GPIO 22
Motor2 = 13  # GPIO 27 
Motor3 = 16  # GPIO 23
GPIO.setup(Motor1, GPIO.OUT)
GPIO.setup(Motor2, GPIO.OUT)
GPIO.setup(Motor3, GPIO.OUT)
DHTPin = 11  # GPIO 17

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Write email and app password here
EMAIL_ADDRESS = 'email'
EMAIL_PASSWORD = 'app password'

IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

email_sent = False

def send_email(to_email, subject, message):
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    email_message = f"From: {EMAIL_ADDRESS}\nTo: {to_email}\nSubject: {subject}\n\n{message}"

    server.sendmail(EMAIL_ADDRESS, to_email, email_message)

    server.quit()

def receive_emails():
    server = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.select('inbox')

    _, data = server.search(None, 'ALL')
    email_ids = data[0].split()

    for email_id in email_ids:
        _, data = server.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        print(f"Raw Email:\n{raw_email}\n\n")
        
        if b'YES' in raw_email.upper():
            GPIO.output(Motor1, GPIO.HIGH)
            GPIO.output(Motor2, GPIO.LOW)
            GPIO.output(Motor3, GPIO.HIGH)
            print("Motor turned on.")
            
            time.sleep(30)

        server.store(email_id, '+FLAGS', '\\Deleted')
    
    server.expunge()
    server.close()
    server.logout()

def loop():
    global email_sent
    dht = DHT.DHT(11)
    counts = 0
    while True:
        counts += 1
        print("Measurement counts: ", counts)
        for i in range(0, 15):
            chk = dht.readDHT11()
            if chk is dht.DHTLIB_OK:
                print("DHT11,OK!")
                break
            time.sleep(0.1)
        print("Humidity : %.2f, \t Temperature : %.2f \n" % (dht.humidity, dht.temperature))
        
        if dht.temperature > 24 and not email_sent:
            message = f"The current temperature is {dht.temperature}. Would you like to turn on the fan?"
            send_email(EMAIL_ADDRESS, 'Fan Control', message)
            print("Email sent. Waiting for response...")
            email_sent = True
            time.sleep(30)
            receive_emails()
            email_sent = False
        elif dht.temperature <= 23.3:
            GPIO.output(Motor1, GPIO.LOW)
            GPIO.output(Motor2, GPIO.HIGH)
            GPIO.output(Motor3, GPIO.HIGH)
            print("Motor turned off.")
        
        time.sleep(2)

if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()


