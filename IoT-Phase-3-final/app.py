import sqlite3
import os
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import email_system as notification_email
import MQTT_Sub as mqtt_sub
from datetime import datetime, timedelta

last_email_time = None
email_interval = 60

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'Phase03.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('SELECT Name, RFID FROM UserThresholds')
user_rows = cursor.fetchall()
user_options = [{'label': user[0], 'value': user[1]} for user in user_rows]

conn.close()

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

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div([
        html.H1("Login", style={'textAlign': 'center', 'margin-bottom': '10px', 'color': colors['text'], **font_style}),
        html.Label("Select User", style={'font-weight': 'bold', 'color': colors['text'], **font_style}),
        dcc.Dropdown(id='user-dropdown', options=user_options, value=None, style={'width': '100%', **font_style}),
        html.Label("RFID", style={'font-weight': 'bold', 'margin-top': '5px', 'color': colors['text'], **font_style}),
        dcc.Input(id='password-input', type='text', value='', style={'width': '100%', **font_style}),
        html.Button('Login', id='login-button', n_clicks=0, style={'width': '100%', 'margin-top': '5px', 'background-color': colors['button'], 'color': colors['button_text'], **font_style}),
        html.Div(id='login-message', style={'textAlign': 'center', 'margin-top': '5px', 'font-weight': 'bold', 'color': colors['error'], **font_style}),
    ], style={'max-width': '400px', 'margin': 'auto', 'padding': '10px', 'border': f'1px solid {colors["border"]}', 'border-radius': '5px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'}),
    html.Div(id='page-content', style={'max-width': '800px', 'margin': 'auto', 'padding': '10px'})
])

dashboard_layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        id='Title',
        children='Phase 3',
        style={'textAlign': 'center', 'font-family': 'Arial, sans-serif', 'font-weight': 'bold', 'color': colors['text']}
    ),
    html.Div(
        className='container',
        style={'textAlign': 'center'},
        children=[
            html.Div(
                id='light-status-text',
                children='Light Status',
                style={'color': colors['text'], 'font-size': '24px', 'font-family': 'Arial, sans-serif', 'font-weight': 'bold'}
            ),
            html.Img(
                id='led',
                src='assets/LED OFF.jpg',
                alt='LED light',
                style={'display': 'block', 'margin': 'auto'}
            ),
        ]
    ),
    html.Div(
        className='container',
        style={'textAlign': 'center'},
        children=[
            html.Div(
                id='light-intensity-text',
                children=['Light Intensity: ', html.Span(id='light-intensity-value', children="Placeholder")],
                style={'color': colors['text'], 'font-size': '24px', 'font-family': 'Arial, sans-serif', 'font-weight': 'bold'}
            ),
            html.Div(
                dcc.Slider(
                    id="light-sensor-slider",
                    min=0,
                    max=1000,
                    value=0,
                    disabled=True,
                ),
                style={'padding': '20px'}
            ),
        ]
    ),
    html.H1(
        id='email-status',
        children='',
        style={'textAlign': 'center', 'color': colors['text']}
    ),
    dcc.Interval(
        id='interval-component',
        interval=2000,
        n_intervals=0
    ),
    html.Div(
        id='email-sent-message',
        children='Email has been sent',
        style={'textAlign': 'center', 'color': colors['success'], 'font-size': '18px', 'font-weight': 'bold', 'display': 'none'}
    )
])

def email_message(light_value):
    if light_value > 400:
        return "Email has been sent"
    else:
        return ""

mqtt_sub.start_mqtt_client()

@app.callback(
    [Output('led', 'src'),
     Output('light-sensor-slider', 'value'),
     Output('email-status', 'children'),
     Output('light-intensity-value', 'children'),
     Output('email-sent-message', 'style')],
    Input('interval-component', 'n_intervals'),
    State('user-dropdown', 'value')
)
def update_mqtt_data(n, logged_in_user):
    global last_email_time
    if mqtt_sub.get_led_status() == 'LED ON':
        if last_email_time is None or datetime.now() - last_email_time >= timedelta(seconds=email_interval):
            notification_email.send_email()
            last_email_time = datetime.now()
            return f"assets/{mqtt_sub.get_led_status()}.jpg", light_value, "Email Sent", light_value, {'textAlign': 'center', 'color': 'green', 'font-size': '18px', 'font-weight': 'bold', 'display': 'block'}
    light_value = int(mqtt_sub.get_light_brightness())
    print(f"Light: {light_value}")
    email_status = email_message(light_value)
    
    if logged_in_user:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT LightIntensityThreshold FROM UserThresholds WHERE RFID=?', (logged_in_user,))
        current_threshold = cursor.fetchone()[0]
        conn.close()
        
        if light_value > current_threshold:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('UPDATE UserThresholds SET LightIntensityThreshold=? WHERE RFID=?', (light_value, logged_in_user))
            conn.commit()
            conn.close()
    
    return f"assets/{mqtt_sub.get_led_status()}.jpg", light_value, email_status, light_value, {'display': 'none'}

@app.callback(
    Output('page-content', 'children'),
    Output('login-message', 'children'),
    Input('login-button', 'n_clicks'),
    State('user-dropdown', 'value'),
    State('password-input', 'value')
)
def login(n_clicks, selected_user, password):
    print(selected_user)
    print(password)
    if n_clicks > 0:
        if selected_user and password == selected_user:
            return dashboard_layout, ''
        else:
            return '', html.Div("Invalid user or password")
    else:
        return '', ''

if __name__ == '__main__':
    app.run(host='192.168.51.68', port=8050, debug=True)