import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
DHTPin = 11  # GPIO 17

DHT11_Humi = 0.0
DHT11_Temp = 0.0

def update_gauges():
    global DHT11_Humi, DHT11_Temp
    dht = DHT.DHT(DHTPin)
    dht.readDHT11()
    DHT11_Humi = dht.humidity
    DHT11_Temp = dht.temperature

def get_humi_data():
    update_gauges()
    global DHT11_Humi
    return DHT11_Humi

def get_temp_data():
    global DHT11_Temp
    return DHT11_Temp
