#include <WiFi.h>
#include <PubSubClient.h>
#include <SPI.h>
#include <MFRC522.h>

// WiFi credentials
const char* ssid = "SM-A505W7965";
const char* password = "angu5588";

// MQTT broker details
const char* mqtt_server = "192.168.228.236";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

// MQTT topics
const char* lightsensor_topic = "light-sensor/brightness";
const char* led_status_topic = "led/status";
const char* rfid_topic = "rfid/data";

const int photoresistorPin = 34;
const int ledPin = 13;

// RFID pins
#define SS_PIN   2  // SDA
#define RST_PIN  23 // RST
#define SCK_PIN  18 // SCK
#define MOSI_PIN 4  // MOSI
#define MISO_PIN 5  // MISO

MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
MFRC522::MIFARE_Key key;

// Init array that will store new NUID
byte nuidPICC[4];

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

  SPI.begin(SCK_PIN, MISO_PIN, MOSI_PIN, SS_PIN); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522
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
  client.publish(lightsensor_topic, lightMessage.c_str());

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

  // RFID logic
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    Serial.println("RFID card detected.");
    String rfidData = "";
    for (byte i = 0; i < rfid.uid.size; i++) {
      rfidData += String(rfid.uid.uidByte[i], HEX);
    }
    Serial.print("RFID Data: ");
    Serial.println(rfidData);

    client.publish(rfid_topic, rfidData.c_str());

    // Halt PICC
    rfid.PICC_HaltA();
    // Stop encryption on PCD
    rfid.PCD_StopCrypto1();
  }

  // Delay to prevent flooding MQTT messages
  delay(1000);
}