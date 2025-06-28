#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>

// -------- CONFIG --------
const char* ssid = "WIFI_SSID";
const char* password = "WIFI_PASSWORD";
const char* serverURL = "http://192.168.1.x:5000/update";  // แก้เป็น IP เครื่องรัน Flask

#define DHTPIN D4      // GPIO2
#define DHTTYPE DHT22
#define SOILPIN A0     // ขา Analog

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  delay(1000);

  dht.begin();

  // Connect Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi connected");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    int soilValue = analogRead(SOILPIN);

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("❌ Failed to read DHT22");
      delay(10000);
      return;
    }

    Serial.printf("🌡 %.1f°C | 💧 %.1f%% | 🌱 Soil: %d\n", temperature, humidity, soilValue);

    WiFiClient client;
    HTTPClient http;
    http.begin(client, serverURL);  // ✅ ใช้ client
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    String postData = "temp=" + String(temperature) +
                      "&humidity=" + String(humidity) +
                      "&soil=" + String(soilValue);

    int code = http.POST(postData);
    Serial.printf("📡 HTTP Code: %d\n", code);
    http.end();
  } else {
    Serial.println("❌ WiFi disconnected");
  }

  delay(15000);
}

