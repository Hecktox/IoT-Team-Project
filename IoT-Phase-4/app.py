import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
DHTPin = 11  # GPIO 17

DHT11_Humi = 0.0
DHT11_Temp = 0.0

def loop():
    global DHT11_Humi, DHT11_Temp
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
        DHT11_Humi = dht.humidity
        DHT11_Temp = dht.temperature
        print("Humidity : %.2f, \t Temperature : %.2f \n" % (DHT11_Humi, DHT11_Temp))
        time.sleep(0.5)

if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
