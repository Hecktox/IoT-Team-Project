# noinspection PyUnresolvedReferences
import RPi.GPIO as GPIO
import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
import time
from dash import Dash, html, callback, Input, Output, dcc

is_email_sent = True
is_alert_sent = False

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dbc.Toast(
            "Email regarding fan status",
            id="positioned-toast",
            header="Email Status",
            is_open=False,
            dismissable=True,
            duration=4000,
            icon="success",
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", "top": 20, "right": 20, "width": 350},
        ),
        dcc.Interval(
            id='interval-component',
            interval=2000,  # Update every 2 seconds
            n_intervals=0
        )
    ]
)

@app.callback(
    Output("positioned-toast", "is_open"),
    [Input("interval-component", "n_intervals")],
)
def trigger_toast(n):
    global is_email_sent, is_alert_sent
    return is_email_sent

if __name__ == '__main__':
    app.run(host='192.168.187.68', port=8050, debug=True)
