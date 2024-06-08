
# noinspection PyUnresolvedReferences
import RPi.GPIO as GPIO
import Freenove_DHT as DHT
import dash_daq as daq
import email_system as email_system
import time
from dash import Dash, html, callback, Input, Output, dcc

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
DHTPin = 11


app = Dash(__name__)

app.layout = html.Div([
    html.Div(
        'IoT Phase 2 Project',
        style={'text-align': 'center', 'margin': '10px'}
    ),
    daq.Thermometer(
        id='temperature-gauge',
        label='Temperature',
        labelPosition='top',
        showCurrentValue=True,
        units="C",
        value=0,
        min=-30,
        max=40,
        style={'margin-bottom': '5%'}
    ),
    daq.Gauge(
        color={
            "gradient": True,
            "ranges": {
                "green": [0, 18],
                "yellow": [18, 24],
                "red": [24, 30]
            }
        },
        id='humidity-gauge',
        showCurrentValue=True,
        label="Humidity",
        value=0,
        max=50,
        min=0,
    ),
    html.Div(
        id='email',
        style={'text-align': 'center', 'margin': '10px'}
    ),
    html.Img(
        id='fan',
        src='assets/fan off.png',
        alt='Fan',
        style={'display': 'block', 'margin': 'auto'}
    ),
    dcc.Interval(
        id='interval-component',
        interval=2000,  # Update every 2 seconds
        n_intervals=0
    ),
])


@callback(
    [Output('humidity-gauge', 'value'),
     Output('temperature-gauge', 'value'),],
    [Input('interval-component', 'n_intervals')],
    prevent_initial_call=True
)
def update_gauges(n):
    dht = DHT.DHT(DHTPin)
    while True:
        dht.readDHT11()	
        print(f'Humidity: {dht.humidity}', f'Temperature: {dht.temperature}')
        return [dht.humidity, dht.temperature]


@callback(
    [Output('fan', 'src')],
    [Input('temperature-gauge', 'value')]
)
def send_email(temperature):
    send_response = email_system.send_email(temperature)
    print(send_response)

    receive_response = email_system.receive_email()
    print(receive_response)

    if not receive_response or ('Error' in str(receive_response)):
        return ['assets/fan off.png']
    return ['assets/fan on.png']

if __name__ == '__main__':
    app.run(host='192.168.137.68', port=8050, debug=True)
    MotorEnable = 36  # Enable Pin GPIO 16
    MotorInput2 = 38  # Input Pinn GPIO 20
    MotorInput3 = 40  # Input Pinn GPIO 21

    GPIO.setup(MotorEnable, GPIO.OUT)
    GPIO.setup(MotorInput2, GPIO.OUT)
    GPIO.setup(MotorInput3, GPIO.OUT)