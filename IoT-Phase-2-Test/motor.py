import RPi.GPIO as GPIO

# Motor1 = 33 # Enable Pin GPIO 13
# Motor2 = 35 # Input Pin GPIO 19
# Motor3 = 37 # Input Pin GPIO 26

def motor_on(enable, input_1, input_2):
    GPIO.output(enable, GPIO.HIGH)
    GPIO.output(input_1, GPIO.LOW)
    GPIO.output(input_2, GPIO.HIGH)

def motor_off(enable):
    GPIO.output(enable, GPIO.LOW)



