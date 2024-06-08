import sqlite3
import MQTT_Sub as mqtt_sub
import dht11 as dht11
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'Phase04.db')

def get_user_by_rfid():
    rfid_data = mqtt_sub.get_rfid_data()
    print(f"RFID data received: {rfid_data}")
    if not rfid_data:
        return None, None
    
    conn = sqlite3.connect(db_path, timeout=10)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM UserThresholds WHERE RFID = ?', (rfid_data,))
    user = cursor.fetchone()
    conn.close()
    return rfid_data, list(user) if user else None

def is_value_over_thresholds(temp, humidity, light_intensity, user_thresholds):
    return temp > user_thresholds[3] or humidity > user_thresholds[4] or light_intensity > user_thresholds[5], temp, humidity, light_intensity

def update_user_thresholds(rfid_data, temp, humidity, light_intensity):
    conn = sqlite3.connect(db_path, timeout=10)
    cursor = conn.cursor()
    cursor.execute('UPDATE UserThresholds SET TempThreshold = ?, HumidityThreshold = ?, LightIntensityThreshold = ? WHERE RFID = ?',
                    (int(temp), int(humidity), int(light_intensity), rfid_data))
    conn.commit()
    conn.close()

def compare_values_with_thresholds():
    rfid_data, _ = get_user_by_rfid()
    if rfid_data:
        user = get_user_thresholds_by_rfid(rfid_data)
        if user:
            print(f"User with RFID {rfid_data} found: {user[2]}")
            current_temp = dht11.get_temp_data()
            current_humidity = dht11.get_humi_data()
            current_light_intensity = int(mqtt_sub.light_brightness)

            is_over_thresholds, temp, humidity, light_intensity = is_value_over_thresholds(current_temp, current_humidity, current_light_intensity, user)
            
            if is_over_thresholds:
                print("Values are over the thresholds. Updating database.")
                update_user_thresholds(rfid_data, temp, humidity, light_intensity)
            else:
                print("Current values are not over the currently stored thresholds. Skipping update.")
        else:
            print("No user found with scanned RFID.")
    else:
        print("No RFID data received.")

def get_user_thresholds_by_rfid(rfid_data):
    conn = sqlite3.connect(db_path, timeout=10)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM UserThresholds WHERE RFID = ?', (rfid_data,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_name_by_rfid(rfid_data):
    conn = sqlite3.connect(db_path, timeout=10)
    cursor = conn.cursor()
    cursor.execute('SELECT Name FROM UserThresholds WHERE RFID = ?', (rfid_data,))
    name = cursor.fetchone()
    conn.close()
    return name