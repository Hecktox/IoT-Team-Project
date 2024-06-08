# noinspection PyUnresolvedReferences
import paho.mqtt.client as mqtt

light_brightness = ''

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("light-sensor/brightness")

def on_message(client, userdata, msg):
    global led_status, light_brightness
    if msg.topic == "light-sensor/brightness":
        # print(msg.topic + " " + str(msg.payload))
        light_brightness = msg.payload.decode()

def start_mqtt_client():
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.connect("192.168.137.68", 1883, 60)

    mqttc.loop_start()

def get_light_brightness():
    global light_brightness
    return light_brightness
