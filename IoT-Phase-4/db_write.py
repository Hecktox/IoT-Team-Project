import sqlite3
import MQTT_Sub as mqtt_sub
import dht11 as app
import time
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'Phase04.db')

mqtt_sub.start_mqtt_client()

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

def get_user_thresholds_by_rfid(rfid_data):
    conn = sqlite3.connect(db_path, timeout=10)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM UserThresholds WHERE RFID = ?', (rfid_data,))
    user = cursor.fetchone()
    conn.close()
    return user

try:
    conn = sqlite3.connect(db_path, timeout=10)
    cursor = conn.cursor()

    while True:
        rfid_data, _ = get_user_by_rfid()
        if rfid_data:
            user = get_user_thresholds_by_rfid(rfid_data)
            if user:
                print(f"User with RFID {rfid_data} found: {user[2]}")
                current_temp = app.get_temp_data()
                current_humidity = app.get_humi_data()
                current_light_intensity = int(mqtt_sub.light_brightness)

                if current_temp > user[3] or current_humidity > user[4] or current_light_intensity > user[5]:
                    print("Updating database.")
                    cursor.execute('UPDATE UserThresholds SET TempThreshold = ?, HumidityThreshold = ?, LightIntensityThreshold = ? WHERE RFID = ?',
                                (int(current_temp), int(current_humidity), int(current_light_intensity), rfid_data))
                    conn.commit()

                else:
                    print("Current values are not over the currently stored thresholds. Skipping update.")
            else:
                print("No user found with scanned RFID.")
        else:
            print("No RFID data received.")

        time.sleep(1)

except KeyboardInterrupt:
    print("Process stopped by user")
finally:
    conn.close()


