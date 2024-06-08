import RPi.GPIO as GPIO
from time import sleep

# GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

Temperature = 22
Motor1 = 33 # Enable Pin GPIO 13
Motor2 = 35 # Input Pin GPIO 19
Motor3 = 37 # Input Pin GPIO 26

GPIO.setup(Motor1,GPIO.OUT)
GPIO.setup(Motor2,GPIO.OUT)
GPIO.setup(Motor3,GPIO.OUT)

def setup_gpio():
    Motor1 = 33  # Enable Pin GPIO 13
    Motor2 = 35  # Input Pin GPIO 19
    Motor3 = 37  # Input Pin GPIO 26

    GPIO.setup(Motor1, GPIO.OUT)
    GPIO.setup(Motor2, GPIO.OUT)
    GPIO.setup(Motor3, GPIO.OUT)

def motor_on(temperature):
    if  temperature >= 22:
        GPIO.output(Motor1, GPIO.HIGH)
        GPIO.output(Motor2, GPIO.LOW)
        GPIO.output(Motor3, GPIO.HIGH)

def motor_off():
    GPIO.output(Motor1, GPIO.LOW)


motor_on(Temperature)
sleep(5)
motor_off()
GPIO.cleanup()