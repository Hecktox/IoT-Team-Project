# noinspection PyUnresolvedReferences
import dash
import RPi.GPIO as GPIO
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import email_system as notification_email
from dash import Dash, html, callback, Input, Output, dcc
import MQTT_Sub as mqtt_sub

is_email_sent = False

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
LED_PIN = 40 # GPIO 21
GPIO.setup(LED_PIN, GPIO.OUT)

colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'border': '#333333',
    'button': '#7FDBFF',
    'button_text': '#FFFFFF',
    'error': '#FF4136',
    'success': '#2ECC40'
}

font_style = {
    'font-family': 'Helvetica, sans-serif'
}

app.layout = html.Div([
    html.H1('IoT Phase 3 Testing'),
    html.H2(
        'Fan off',
        id='fan',
    ),
    html.Img(
        id='led',
        src='assets/LED OFF.jpg',
        alt='LED light',
        style={'display': 'block', 'margin': 'auto'}
    ),
    dcc.Slider(
        id="light-sensor-slider",
        min=0,
        max=1000,
        value=0,
        disabled=True,
    ),
    html.H1(
        id='email-status',
        children='',
        style={'textAlign': 'center', 'color': colors['text']}
    ),
    dcc.Interval(
        id='interval-component',
        interval=100,  # Update every 2 seconds
        n_intervals=0
    ),
])


@callback(
    Output('light-sensor-slider', 'value'),
    Input('interval-component', 'n_intervals')
)
def update_light_sensor_value(n):
    print(mqtt_sub.get_light_brightness())
    return int(mqtt_sub.get_light_brightness())

@callback(
    [Output('led', 'src'),
     Output('email-status', 'children')],
    Input('light-sensor-slider', 'value')
)
def update_light_status_and_notify(light_intensity):
    global is_email_sent
    if light_intensity < 400:
        if not is_email_sent:
            # notification_email.send_email()
            print("Email sent")
            is_email_sent = True
            GPIO.output(LED_PIN, GPIO.HIGH)
            return ["assets/LED ON.jpg", "Email sent"]
        else:
            GPIO.output(LED_PIN, GPIO.HIGH)
            return ["assets/LED ON.jpg", "Email sent"]
    else:
        if is_email_sent:
            print("Email not sent")
            is_email_sent = False
            GPIO.output(LED_PIN, GPIO.LOW)
            return ["assets/LED OFF.jpg", ""]
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
            return ["assets/LED OFF.jpg", ""]

if __name__ == '__main__':
    mqtt_sub.start_mqtt_client()
    app.run(host='192.168.137.68', port=8050, debug=True)
