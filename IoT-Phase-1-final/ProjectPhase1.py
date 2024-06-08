# noinspection PyUnresolvedReferences
from dash import Dash, html, Input, Output, callback
import dash_daq as daq
import RPi.GPIO as GPIO

app = Dash(__name__)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
LED_PIN = 17
GPIO.setup(LED_PIN, GPIO.OUT)

app.layout = html.Div([
    html.Div(
        'IoT Phase 1 Project',
        style={'text-align': 'center', 'margin': '10px'}
    ),
    daq.ToggleSwitch(
        id='led-switch',
        value=False,  # state of the button
    ),
    html.Div(
        id='led-switch-state',
        style={'text-align': 'center', 'margin-top': '20px'}

    ),
    html.Img(
        id='bulb',
        src='assets/bulb off.jpg',  # image path
        alt='LED light',
        style={'display': 'block', 'margin': 'auto'}
    )
])


# write the variables in the same order
@callback(
    # Output callbacks (inside the return)
    [Output('led-switch-state', 'children'),
     Output('led-switch', 'color'),
     Output('bulb', 'src')],

    # Input callback (inside the function)
    [Input('led-switch', 'value')]
)
def update_output(value):
    if value:
        GPIO.output(LED_PIN, GPIO.HIGH)
        print('The light is ON.')
        return 'The light is ON.', 'blue', 'assets/bulb on.jpg'  # return all output callbacks
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        print('The light is OFF.')
        return 'The light is OFF.', 'none', 'assets/bulb off.jpg'  # return all output callbacks


if __name__ == '__main__':
    app.run(host='192.168.2.99', port=8050, debug=True)

