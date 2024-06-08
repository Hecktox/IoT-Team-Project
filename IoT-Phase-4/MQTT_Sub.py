import paho.mqtt.client as mqtt

led_status = ''
light_brightness = ''
rfid_data = ''

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("light-sensor/brightness")
    client.subscribe("led/status")
    client.subscribe("rfid/data")

def on_message(client, userdata, msg):
    global led_status, light_brightness, rfid_data
    if msg.topic == "light-sensor/brightness":
        light_brightness = msg.payload.decode()
    elif msg.topic == "led/status":
        led_status = msg.payload.decode()
    elif msg.topic == "rfid/data":
        rfid_data = msg.payload.decode()

def start_mqtt_client():
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.connect("localhost", 1883, 60)

    mqttc.loop_start()

def get_led_status():
    global led_status
    return led_status

def get_light_brightness():
    global light_brightness
    return light_brightness

def get_rfid_data():
    global rfid_data
    return rfid_data
