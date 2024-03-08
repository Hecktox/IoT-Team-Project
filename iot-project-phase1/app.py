from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO
import time

app = Flask(__name__, template_folder='views')

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED_PIN = 17
GPIO.setup(LED_PIN, GPIO.OUT)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/toggle', methods=['POST'])
def toggle_led():
    switch_status = request.form.get('switch_status')

    # Toggle the LED
    if switch_status == 'OFF':
        GPIO.output(LED_PIN, GPIO.HIGH)
        new_status = 'ON'
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        new_status = 'OFF'

    return jsonify({'status': new_status})

@app.route('/hold', methods=['POST'])
def hold_led():
    switch_status = request.form.get('switch_status')

    # Hold the LED
    if switch_status == 'ON':
        GPIO.output(LED_PIN, GPIO.HIGH)
        new_status = 'ON'
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        new_status = 'OFF'

    return jsonify({'status': new_status})

@app.route('/flashing', methods=['POST'])
def flashing_led():
    switch_status = request.form.get('switch_status')

    # Flash the LED
    if switch_status == 'OFF':
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.5)
        new_status = 'ON'
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        new_status = 'OFF'

    return jsonify({'status': new_status})

if __name__ == '__main__':
    app.run(debug=True)
