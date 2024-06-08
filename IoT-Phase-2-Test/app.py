# noinspection PyUnresolvedReferences
import RPi.GPIO as GPIO
import Freenove_DHT as DHT
import dash_daq as daq
# import email_system as email_system
import time
from dash import Dash, html, callback, Input, Output, dcc
import motor as motor

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

DHTPin = 11 # GPIO 17
Motor1 = 33 # Enable Pin GPIO 13
Motor2 = 35 # Input Pin GPIO 19
Motor3 = 37 # Input Pin GPIO 26

GPIO.setup(Motor1,GPIO.OUT)
GPIO.setup(Motor2,GPIO.OUT)
GPIO.setup(Motor3,GPIO.OUT)

app = Dash(__name__)

app.layout = html.Div([
    html.H1('IoT Phase 2 Testing'),
    html.H2(
        'Fan off',
        id='fan',
    ),
    daq.Thermometer(
        id='temperature-gauge',
        showCurrentValue=True,
        value=0,
        min=-30,
        max=40
    ),
    daq.Gauge(
        id='humidity-gauge',
        showCurrentValue=True,
        value=0,
        min=0,
        max=50
    ),
    dcc.Interval(
        id='interval-component',
        interval=5000,  # Update every 2 seconds
        n_intervals=0
    ),
])

@callback(
    [Output('humidity-gauge', 'value'),
     Output('temperature-gauge', 'value')],
    [Input('interval-component', 'n_intervals')],
)
def update_gauges(n):
    dht = DHT.DHT(DHTPin)
    while True:
        dht.readDHT11()
        print(f'Humidity: {dht.humidity}', f'Temperature: {dht.temperature}')
        return [dht.humidity, dht.temperature]

@callback(
    [Output('fan', 'children')],
    [Input('temperature-gauge', 'value')]
)
def control_fan(temperature):
    print(f'Temperature: {temperature}')
    if  temperature > 25:
        motor.motor_on(Motor1, Motor2, Motor3)
        return ['Fan on']
    else:
        motor.motor_off(Motor1)
        return ['Fan off']

if __name__ == '__main__':
    app.run(host='192.168.2.99', port=8050, debug=True)