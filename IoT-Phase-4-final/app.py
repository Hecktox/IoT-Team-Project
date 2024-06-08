# noinspection PyUnresolvedReferences
import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Dash, html, callback, Input, Output, dcc
from dash import clientside_callback
#import bluetooth
import re
import Email_System as Email
import RPi.GPIO as GPIO
import Freenove_DHT as DHT
import MQTT_Sub as MQTT_Sub
import threading
from time import sleep
from threading import Thread
from dash import State
import db_write as db
import motor as motor

# Setup start
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

is_email_sent = False
RSSI_THRESHOLD = -80
devices_nearby = 0

DHTPin = 11  # GPIO 17
LED_PIN = 40  # GPIO 21
Motor1 = 33  # Enable Pin GPIO 13
Motor2 = 35  # Input Pin GPIO 19
Motor3 = 37  # Input Pin GPIO 26

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(Motor1, GPIO.OUT)
GPIO.setup(Motor2, GPIO.OUT)
GPIO.setup(Motor3, GPIO.OUT)
# Setup end

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

app.layout = html.Div(
    children=[
        dbc.Nav(
            [
                html.Div(
                    id='color-mode-switch',
                    children=[
                        html.H1("Smart Home"),
                        html.Span(
                            [
                                dbc.Label(className="fa fa-moon", html_for="switch"),
                                dbc.Switch(id="switch", value=True, className="d-inline-block ms-1", persistence=True),
                                dbc.Label(className="fa fa-sun", html_for="switch"),
                            ]
                        ),
                    ]
                ),
            ],
            pills=True,
            style={'position': 'fixed', 'top': 0, 'left': 0, 'right': 0, 'zIndex': 1000,}
        ),
        
        html.Div(
            id='profile',
            children=[
                html.P('Profile',
                       style={'color': 'grey', 'textAlign': 'center', 'font-family': 'Verdana', 'fontSize': '40px'}),
                html.Img(src='/assets/profile.webp',
                         style={'width': '150px', 'height': '150px', 'borderRadius': '50%', 'margin': '0 auto',
                                'display': 'block'}),
                html.Label('Name', style={'color': 'grey', 'margin-bottom': '5px', 'display': 'block',
                                          'font-family': 'Verdana'}),
                dcc.Input(id='name', type='text', value='',
                          style={'width': '100%', 'margin-bottom': '20px', 'height': '50px'}),
                html.Label('Temp. Threshold', style={'color': 'grey', 'margin-bottom': '5px', 'display': 'block',
                                                     'font-family': 'Verdana'}),
                dcc.Input(id='temp-threshold', type='number', value=0,
                          style={'width': '100%', 'margin-bottom': '20px', 'height': '50px', 'font-family': 'Verdana'}),
                html.Label('Humidity Threshold', style={'color': 'grey', 'margin-bottom': '5px', 'display': 'block',
                                                        'font-family': 'Verdana'}),
                dcc.Input(id='humidity-threshold', type='number', value=0,
                          style={'width': '100%', 'margin-bottom': '20px', 'height': '50px', 'font-family': 'Verdana'}),
                html.Label('Light Intensity Threshold',
                           style={'color': 'grey', 'margin-bottom': '5px', 'display': 'block',
                                  'font-family': 'Verdana'}),
                dcc.Input(id='light-intensity-threshold', type='number', value=0,
                          style={'width': '100%', 'margin-bottom': '20px', 'height': '50px'}),

                html.Button('Submit', id='submit-button', n_clicks=0,
                            style={'width': '100%', 'margin-top': '20px', 'height': '50px',
                                   'backgroundColor': 'rgb(29, 119, 242)', 'color': 'white',
                                   'borderRadius': '10px', 'fontFamily': 'Verdana'}),
                html.Label('', id='email-sent-logged-in', style={'padding-top': '20px', 'font-size': '30px'})
            ],
            style={'flex': 1, 'width': '200%', 'borderRadius': '10px', 'padding': '20px', 'textAlign': 'center', 'font-family': 'Verdana'}
        ),

        html.Div(
            id='phases-container',
            children=[
                html.Div(
                    id='right-phases',
                    children=[
                        html.Div(
                            id='phase2',
                            children=[
                                html.Div([
                                    html.Div(
                                        daq.Thermometer(
                                            id='temperature-gauge',
                                            label='Temperature',
                                            labelPosition='top',
                                            showCurrentValue=True,
                                            value=0,
                                            min=-0,
                                            max=40,
                                            style={'width': '350px', 'height': '325px', 'margin-right': '30px',
                                                   'margin-left': '10px', 'border': '5px solid lightgrey',
                                                   'backgroundColor': 'rgb(129, 133, 137)', 'borderRadius': '10px',
                                                   'fontFamily': 'Verdana', 'color': 'white'}
                                        ),
                                        style={'width': '50%', 'display': 'inline-block'}
                                    ),
                                    html.Div(
                                        daq.Gauge(
                                            color={
                                                "gradient": True,
                                                "ranges": {
                                                    "green": [0, 18],
                                                    "yellow": [18, 24],
                                                    "red": [24, 30]
                                                },
                                                "value": "red"
                                            },
                                            id='humidity-gauge',
                                            showCurrentValue=True,
                                            label="Humidity",
                                            value=0,
                                            min=0,
                                            max=50,
                                            style={'width': '350px', 'height': '325px', 'margin-right': '50px',
                                                   'margin-left': '75px', 'border': '5px solid lightgrey',
                                                   'backgroundColor': 'rgb(129, 133, 137)', 'borderRadius': '10px',
                                                   'fontFamily': 'Verdana', 'color': 'white'},
                                        ),
                                        style={'width': '50%', 'display': 'inline-block'}
                                    )
                                ], style={'display': 'flex', 'justifyContent': 'space-between'}),
                            ],
                            style={'flex': 1, 'padding': '20px'}
                        ),
                        html.Div(
                            id='phase3',
                            children=[
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div("Light Control",
                                                         style={'color': 'white', 'textAlign': 'center',
                                                                'font-family': 'Verdana'}),
                                                html.Img(id='led-img',
                                                         src='/assets/led_off.png',
                                                         style={'width': '100px', 'height': '100px',
                                                                'borderRadius': '50%', 'margin-bottom': '20px'}),
                                                html.P('Light Intensity:',
                                                       id='light-intensity',
                                                       style={'color': 'white', 'textAlign': 'center',
                                                              'font-family': 'Verdana', 'margin-bottom': '20px'}),
                                                html.P('Light Status: Off',
                                                       id='light-status',
                                                       style={'color': 'white', 'textAlign': 'center',
                                                              'font-family': 'Verdana',
                                                              'margin-bottom': '20px'}),
                                            ],
                                            style={'display': 'inline-block', 'border': '5px solid lightgrey',
                                                   'padding': '20px', 'borderRadius': '10px', 'text-align': 'center',
                                                   'margin-right': '150px', 'width': '350px', 'height': '285px',
                                                   'backgroundColor': 'rgb(129, 133, 137)', 'margin-left': '5px'}
                                        ),

                                        html.Div(
                                            [
                                                html.Div("Fan Control", style={'color': 'white', 'textAlign': 'center',
                                                                              'font-family': 'Verdana'}),
                                                html.Img(id='fan-img',
                                                         src='/assets/fan_off.png',
                                                         style={'width': '100px', 'height': '100px',
                                                                'borderRadius': '50%', 'margin-bottom': '20px'}),
                                                html.P('Fan Status: off', id="fan-status", style={'color': 'white', 'textAlign': 'center',
                                                                             'font-family': 'Verdana',
                                                                             'margin-bottom': '20px'}),
                                                html.P('', id="email-sent-fan", style={'color': 'white', 'textAlign': 'center',
                                                                             'font-family': 'Verdana',
                                                                             'margin-bottom': '20px'}),
                                            ],
                                            style={'display': 'inline-block', 'border': '5px solid lightgrey',
                                                   'padding': '20px', 'borderRadius': '10px', 'text-align': 'center',
                                                   'width': '350px', 'height': '285px',
                                                   'backgroundColor': 'rgb(129, 133, 137)', 'margin-right': '5px'}
                                        ),
                                    ],
                                    style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}
                                )

                            ],
                            style={'flex': 1, 'padding': '20px'}
                        ),
                        # html.Div(
                        #     id='phase4',
                        #     children=[
                        #         html.Img(src='/assets/bluetooth_png.png',
                        #                  style={'width': '100px', 'height': '35px', 'marginLeft': '10px'}),
                        #         html.Div([
                        #             html.Div(id="device_count",
                        #                      style={'color': 'white', 'textAlign': 'center', 'font-family': "Verdana",
                        #                             'margin-top': '20px', 'backgroundColor': 'rgb(29, 119, 242)',
                        #                             'width': '300px', 'height': '40px', 'lineHeight': '40px',
                        #                             'borderRadius': '10px'}),
                        #              dcc.Interval(
                        #                  id="interval-component",
                        #                  interval=2000,
                        #                  n_intervals=0
                        #              )
                        #         ], style={'display': 'flex', 'alignItems': 'center'}),
                        #     ],
                        #     style={'flex': 1, 'padding': '20px'}
                        # )

                    ],
                    style={'display': 'flex', 'flexDirection': 'column', 'flex': 1}
                )
            ],
            style={'display': 'flex', 'flex': 1, 'justifyContent': 'flex-end'}
        ),
        dbc.Toast(
            "Email regarding",
            id="email-toast",
            header="New Email",
            is_open=False,
            dismissable=True,
            duration=4000,
            icon="success",
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", "top": 20, "right": 20, "width": 350},
        ),
        dcc.Interval(
            id='interval-component',
            interval=4000,  # Update every 2 seconds
            n_intervals=0
        ),
        dcc.Interval(
            id='interval-temp',
            interval=2000,  # Update every 2 seconds
            n_intervals=0
        ),
    ],
    style={'display': 'flex', 'flexDirection': 'row', 'height': '100vh', 'margin': 0, 'padding': 0}
)

clientside_callback(
    """
    function(switchOn) {
    document.documentElement.setAttribute("data-bs-theme", switchOn ? "light" : "dark");
    return window.dash_clientside.no_update;
    }
    """,
    Output("switch", "value"),
    Input("switch", "value"),
)

MQTT_Sub.start_mqtt_client()


def open_toast(n):
    if n == 0:
        return dash.no_update
    return True


# Functions

# Bluetooth
'''def scan_devices():
    global devices_nearby
    while True:
        nearby_devices = bluetooth.discover_devices(duration=2, lookup_names=False, lookup_class=True)
        devices_nearby = len(nearby_devices)


scan_thread = Thread(target=scan_devices)
scan_thread.daemon = True
scan_thread.start()


@app.callback(
    Output('device_count', 'children'),
    [Input('interval-component', 'n_intervals')])
def update_device_count(n):
    return f"Bluetooth devices nearby: {devices_nearby}"
'''
    
# Database
current_rfid = None

@app.callback(
    [Output('name', 'value'),
     Output('temp-threshold', 'value'),
     Output('humidity-threshold', 'value'),
     Output('light-intensity-threshold', 'value'),
     Output('email-sent-logged-in', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_profile(n):
    global current_rfid, is_email_sent
    rfid_data, _ = db.get_user_by_rfid()
    if rfid_data and rfid_data != current_rfid:
        current_rfid = rfid_data
        user = db.get_user_thresholds_by_rfid(rfid_data)
        if user:
            is_email_sent = False
            Email.send_email_login(user[2])
            return user[2], user[3], user[4], user[5], 'Logged in successfully email sent'
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, ''

@app.callback(
    Input('submit-button', 'n_clicks'),
    State('name', 'value'),
    State('temp-threshold', 'value'),
    State('humidity-threshold', 'value'),
    State('light-intensity-threshold', 'value')
)
def submit_form(n_clicks, name, temp_threshold, humidity_threshold, light_intensity_threshold):
    if n_clicks and n_clicks > 0:
        print(f"Submit button clicked. n_clicks: {n_clicks}")
        rfid_data, _ = db.get_user_by_rfid()
        if rfid_data:
            db.update_user_thresholds(rfid_data, temp_threshold, humidity_threshold, light_intensity_threshold)
            return f'User RFID: {rfid_data}, Name: {name}, Temp. Threshold: {temp_threshold}, Humidity Threshold: {humidity_threshold}, Light Intensity Threshold: {light_intensity_threshold}'
        else:
            return 'No RFID data found.'
    else:
        return ''

# Motor
@callback(
    [Output('humidity-gauge', 'value'),
     Output('temperature-gauge', 'value')],
    [Input('interval-temp', 'n_intervals')],
)
def update_gauges(n):
    dht = DHT.DHT(DHTPin)
    while True:
        dht.readDHT11()
        print(dht.temperature)
        return [dht.humidity, dht.temperature]


@callback(
    [Output('fan-img', 'src'),
     Output('fan-status', 'children'),
     Output('email-sent-fan', 'children')],
    [Input('temp-threshold', 'value'),
    Input('temperature-gauge', 'value')]
)
def send_email(temp_threshold, temperature):
    global current_rfid
    if current_rfid is not None:
        send_response = Email.send_email_fan(temp_threshold, temperature)
        print(send_response)
        if send_response == "Email sent successfully":
            print("vcscsccscs ccscs")
            return ['assets/fan_off.png', "Fan Status: off", "Email sent"]

    receive_response = Email.receive_email_fan()
    print(receive_response)

    if not receive_response or ('Error' in str(receive_response)):
        motor.motor_off(Motor1)
        return ['assets/fan_off.png', "Fan Status: off", ""]
    else:
        motor.motor_on(Motor1, Motor2, Motor3)
        return ['assets/fan_on.png', "Fan Status: on", ""]


# Photoresistor
@callback(
    Output('light-intensity', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_light_sensor_value(n):
    return f"Light Intensity: {MQTT_Sub.get_light_brightness()}"


@callback(
    [Output('led-img', 'src'),
     Output('light-status', 'children'),
     Output('email-toast', 'children'),
     Output('email-toast', 'is_open')],
    [Input('light-intensity-threshold', 'value'),
    Input('light-intensity', 'children')]
)
def update_light_status_and_notify(light_intensity_threshold, light_intensity):
    global is_email_sent, current_rfid
    # Get number in string with regex
    match = re.search(r'\d+', light_intensity)
    # Convert to Int
    light_intensity = int(match.group())
    print(light_intensity_threshold > light_intensity)
    print("light_intensity")

    if light_intensity_threshold > light_intensity and current_rfid is not None:
        if not is_email_sent:
            print("Sending email light")
            Email.send_email_light()
            print("Email sent")
            is_email_sent = True
            GPIO.output(LED_PIN, GPIO.HIGH)
            return ["assets/led_on.png", "Light Status: On", "Email regarding light status", True]
        else:
            GPIO.output(LED_PIN, GPIO.HIGH)
            return ["assets/led_on.png", "Light Status: On", "Email regarding light status", False]
    else:
        if is_email_sent:
            print("Email not sent")
            is_email_sent = False
            GPIO.output(LED_PIN, GPIO.LOW)
            return ["assets/led_off.png", "Light Status: Off", "Email regarding light status", False]
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
            return ["assets/led_off.png", "Light Status: Off", "Email regarding light status", False]

# Run the Dash app
if __name__ == '__main__':
    app.run(
        host='192.168.51.68',
        port=8050,
        debug=True
    )