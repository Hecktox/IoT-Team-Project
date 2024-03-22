'''
Maximus Taube
IoT Project Phase02
'''
import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT

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

def loop():
    dht = DHT.DHT(DHTPin)
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
        
        # Check if temperature is greater than 24
        if dht.temperature > 24:
            # Turn on the motor
            GPIO.output(Motor1, GPIO.HIGH)
            GPIO.output(Motor2, GPIO.LOW)
            GPIO.output(Motor3, GPIO.HIGH)
            print("Motor turned on.")
        else:
            # Turn off the motor
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

