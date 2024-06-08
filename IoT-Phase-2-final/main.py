import Freenove_DHT as DHT
import RPi.GPIO as GPIO
import time

def sensor_data_generator():
    dht = DHT.DHT(11)
    while True:
        sumCnt = 0
        okCnt = 0
        sumCnt += 1
        chk = dht.readDHT11()
        if chk == 0:
            okCnt += 1
        okRate = 100.0 * okCnt / sumCnt
        yield chk, dht.humidity, dht.temperature
        time.sleep(3)

if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        for chk, humidity, temperature in sensor_data_generator():
            if chk is not None:
                print("chk : %d, \t Humidity : %.2f, \t Temperature : %.2f " % (chk, humidity, temperature))
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
