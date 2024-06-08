#include <WiFi.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "";
const char* password = "";

// MQTT broker details
const char* mqtt_server = "";
const int mqtt_port = 1883; 

WiFiClient espClient;
PubSubClient client(espClient);

// MQTT topics
const char* lightsensor_topic = "light-sensor/brightness";
const char* led_status_topic = "led/status";

const int photoresistorPin = 34; 
const int ledPin = 13; 

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  pinMode(photoresistorPin, INPUT);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  int sensorValue = analogRead(photoresistorPin);

  //brightness level (0-100)
  int brightness = map(sensorValue, 0, 4095, 0, 1000);

  Serial.print("Sensor Value: ");
  Serial.println(brightness);
  
  // Publish brightness level to MQTT topic
  String lightMessage = String(brightness);
//  client.publish(lightsensor_topic, lightMessage.c_str());
  
  String statusLed = "";
  if (brightness < 400) {
    digitalWrite(ledPin, HIGH);
    statusLed = "LED ON";
  } else {
    digitalWrite(ledPin, LOW);
    statusLed = "LED OFF";
  }

  Serial.print("LED Status: ");
  Serial.println(statusLed);


  // Publish a message every 5 seconds
//  static unsigned long lastMillis = 0;
//  if (millis() - lastMillis > 5000) {
//    lastMillis = millis();
    // Example message to publish
//    String message = "Hello, MQTT!";
    client.publish(lightsensor_topic, lightMessage.c_str());
    client.publish(led_status_topic, statusLed.c_str());
//  }
}
