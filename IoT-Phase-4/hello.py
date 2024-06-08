import dash
from dash import html, dcc
import dash_daq as daq
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    children=[
        html.Div(
            id='profile',
            children=[
                html.P('Profile', style={'color': 'grey', 'textAlign': 'center', 'font-family': 'Verdana', 'fontSize': '40px'}),
                html.Img(src='/assets/my_sunshine.jpg', style={'width': '150px', 'height': '150px', 'borderRadius': '50%', 'margin': '0 auto', 'display': 'block'}),
                html.Label('User ID', style={'color': 'grey', 'margin-bottom': '5px', 'display': 'block', 'font-family': 'Verdana'}),
                dcc.Input(id='user-id', type='text', value='', style={'width': '100%', 'margin-bottom': '20px', 'height': '50px'}),
                html.Label('Name', style={'color': 'grey', 'margin-bottom': '5px', 'display': 'block', 'font-family': 'Verdana'}),
                dcc.Input(id='name', type='text', value='', style={'width': '100%', 'margin-bottom': '20px', 'height': '50px'}),
                html.Label('Temp. Threshold', style={'color': 'grey', 'margin-bottom': '5px', 'display': 'block', 'font-family': 'Verdana'}),
                dcc.Input(id='temp-threshold', type='number', value=0, style={'width': '100%', 'margin-bottom': '20px', 'height': '50px', 'font-family': 'Verdana'}),
                html.Label('Humidity Threshold', style={'color': 'grey', 'margin-bottom': '5px', 'display': 'block', 'font-family': 'Verdana'}),
                dcc.Input(id='humidity-threshold', type='number', value=0, style={'width': '100%', 'margin-bottom': '20px', 'height': '50px', 'font-family': 'Verdana'}),
                html.Label('Light Intensity Threshold', style={'color': 'grey', 'margin-bottom': '5px', 'display': 'block', 'font-family': 'Verdana'}),
                dcc.Input(id='light-intensity-threshold', type='number', value=0, style={'width': '100%', 'margin-bottom': '20px', 'height': '50px'}),
                html.Button('Submit Changes', id='submit-button', n_clicks=0, style={'width': '100%', 'height': '50px', 'backgroundColor': 'lightblue', 'margin-top': '20px', 'font-family': 'Verdana'}),
                # Toast
                dbc.Toast(
                    [html.P("Email has been sent!", className="mb-0")],
                    id="message",
                    duration=3000,
                    is_open=False,
                    style={'position': 'fixed', 'top': '70px', 'left': '20px', 'width': '300px'}
                ),
                dbc.Button(
                    "Email Status",
                    id="button_toggle",
                    color="secondary",
                    className="mb-3",
                    n_clicks=0,
                    style={'position': 'fixed', 'top': '20px', 'left': '20px'}
                ),
            ],
            style={'flex': 1, 'width': '200%', 'borderRadius': '10px',  'padding': '20px', 'textAlign': 'center', }
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
                                            style={'width': '350px', 'height': '325px', 'margin-right': '30px', 'margin-left': '10px', 'border': '5px solid lightgrey', 'backgroundColor': 'rgb(129, 133, 137)', 'borderRadius': '10px', 'fontFamily': 'Verdana', 'color': 'white'}
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
                                            max=50,
                                            min=0,
                                            style={'width': '350px', 'height': '325px', 'margin-right': '50px', 'margin-left': '75px', 'border': '5px solid lightgrey', 'backgroundColor': 'rgb(129, 133, 137)', 'borderRadius': '10px', 'fontFamily': 'Verdana', 'color': 'white'},
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
                                                html.Div("Light Control", style={'color': 'white', 'textAlign': 'center', 'font-family': 'Verdana'}),
                                                html.Img(src='/assets/led_off.png', style={'width': '100px', 'height': '100px', 'borderRadius': '50%', 'margin-bottom': '20px'}),
                                                daq.BooleanSwitch(
                                                    id='light-switch',
                                                    on=False,
                                                    disabled=True,
                                                    style={'font-family': 'Verdana', 'color': 'green', 'margin-bottom': '20px'}
                                                ),
                                                html.P('Light Intensity:', style={'color': 'white', 'textAlign': 'center', 'font-family': 'Verdana', 'margin-bottom': '20px'}),
                                                html.P('Light Status:', style={'color': 'white', 'textAlign': 'center', 'font-family': 'Verdana', 'margin-bottom': '20px'}),
                                            ],
                                            style={'display': 'inline-block', 'border': '5px solid lightgrey', 'padding': '20px', 'borderRadius': '10px', 'text-align': 'center', 'margin-right': '150px', 'width': '350px', 'height': '285px', 'backgroundColor': 'rgb(129, 133, 137)', 'margin-left': '5px'}
                                        ),

                                        html.Div(
                                            [
                                                html.Div("Fan Control", style={'color': 'white', 'textAlign': 'center', 'font-family': 'Verdana'}),
                                                html.Img(src='/assets/fan_off.png', style={'width': '100px', 'height': '100px', 'borderRadius': '50%', 'margin-bottom': '20px'}),
                                                daq.BooleanSwitch(
                                                    id='fan-switch',
                                                    on=False,
                                                    disabled=True,
                                                    style={'font-family': 'Verdana', 'color': 'green', 'margin-bottom': '20px'}
                                                ),
                                                html.P('Fan Status:', style={'color': 'white', 'textAlign': 'center', 'font-family': 'Verdana', 'margin-bottom': '20px'}),
                                            ],
                                            style={'display': 'inline-block', 'border': '5px solid lightgrey', 'padding': '20px', 'borderRadius': '10px', 'text-align': 'center', 'width': '350px', 'height': '285px', 'backgroundColor': 'rgb(129, 133, 137)', 'margin-right': '5px'}
                                        ),
                                    ],
                                    style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}
                                )

                            ],
                            style={'flex': 1, 'padding': '20px'}
                        ),
                        html.Div(
                            id='phase4',
                            children=[
                                html.Img(src='/assets/bluetooth_png.png', style={'width': '100px', 'height': '35px', 'marginLeft': '10px'}),
                                html.Div([
                                    html.P('Bluetooth Devices Nearby', style={'color': 'white', 'textAlign': 'center', 'font-family': "Verdana", 'margin-top': '20px', 'backgroundColor': 'rgb(29, 119, 242)', 'width': '300px', 'height': '40px', 'lineHeight': '40px', 'borderRadius': '10px'}),
                                    dcc.Input(id='bluetooth-devices', type='text', value='', style={'width': '100px', 'margin-top': '20px', 'marginLeft': '20px', 'height': '30px', 'marginBottom': '15px', 'border': '5px solid rgb(29, 119, 242)', 'borderRadius': '10px'})
                                ], style={'display': 'flex', 'alignItems': 'center'}),
                                html.Div([
                                    html.P('RSSI Threshold (dBm)', style={'color': 'white', 'textAlign': 'center', 'font-family': "Verdana", 'margin-top': '20px', 'backgroundColor': 'rgb(29, 119, 242)', 'width': '300px', 'height': '40px', 'lineHeight': '40px', 'borderRadius': '10px'}),
                                    dcc.Input(id='rssi-threshold', type='number', value=0, style={'width': '100px', 'margin-top': '20px', 'marginLeft': '20px', 'height': '30px', 'marginBottom': '15px', 'border': '5px solid rgb(29, 119, 242)', 'borderRadius': '10px'})
                                ], style={'display': 'flex', 'alignItems': 'center'})
                            ],
                            style={'flex': 1,  'padding': '20px'}
                        )
                    ],
                    style={'display': 'flex', 'flexDirection': 'column', 'flex': 1}
                )
            ],
            style={'display': 'flex', 'flex': 1, 'justifyContent': 'flex-end'}
        ),
        
    ],
    style={'display': 'flex', 'flexDirection': 'row', 'height': '100vh', 'margin': 0, 'padding': 0, 'backgroundColor': 'rgb(52, 52, 52)'}
)

@app.callback(
    Output("message", "is_open"), [Input("button_toggle", "n_clicks")]
)
def open_toast(n):
    if n == 0:
        return dash.no_update
    return True

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)


