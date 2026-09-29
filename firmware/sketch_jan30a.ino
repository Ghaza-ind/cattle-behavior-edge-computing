#include <Wire.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <MPU6050.h>

// ================== KONFIGURASI ==================
const char* ssid     = "POCO F6";
const char* password = "12345677";

// GANTI DENGAN IP RASPBERRY PI
const char* serverUrl = "http://10.175.224.176:5000/api/data";
// =================================================

MPU6050 mpu;
WiFiClient wifiClient;

// Variabel sensor
int16_t ax, ay, az;
int16_t gx, gy, gz;

// ================== BATCH CONFIG ==================
#define TOTAL_DATA 10
#define INTERVAL 100   // 100ms x 10 = 1 detik

unsigned long lastReadTime = 0;
int dataCount = 0;

String dataBuffer[TOTAL_DATA];
// ==================================================

void setup() {
  Serial.begin(9600);
  delay(1000);

  Wire.begin(D2, D1);

  Serial.println("Inisialisasi MPU6050...");
  mpu.initialize();

  if (!mpu.testConnection()) {
    Serial.println("MPU6050 tidak terdeteksi!");
    while (1);
  }
  Serial.println("MPU6050 siap!");

  WiFi.begin(ssid, password);
  Serial.print("Menghubungkan WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi terhubung!");
  Serial.println(WiFi.localIP());
}

void loop() {

  // Sampling tiap 100ms
  if (millis() - lastReadTime >= INTERVAL) {
    lastReadTime = millis();

    mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    Serial.print("Data ke-");
    Serial.println(dataCount + 1);

    String jsonData = "{";
    jsonData += "\"ax\":" + String(ax) + ",";
    jsonData += "\"ay\":" + String(ay) + ",";
    jsonData += "\"az\":" + String(az) + ",";
    jsonData += "\"gx\":" + String(gx) + ",";
    jsonData += "\"gy\":" + String(gy) + ",";
    jsonData += "\"gz\":" + String(gz);
    jsonData += "}";

    dataBuffer[dataCount] = jsonData;
    dataCount++;
  }

  // Jika sudah 10 data → kirim
  if (dataCount >= TOTAL_DATA) {

    if (WiFi.status() == WL_CONNECTED) {

      HTTPClient http;
      http.begin(wifiClient, serverUrl);
      http.addHeader("Content-Type", "application/json");

      String finalJson = "[";

      for (int i = 0; i < TOTAL_DATA; i++) {
        finalJson += dataBuffer[i];
        if (i < TOTAL_DATA - 1) finalJson += ",";
      }

      finalJson += "]";

      Serial.println("Mengirim 10 data...");

      int httpResponseCode = http.POST(finalJson);

      Serial.print("HTTP Response: ");
      Serial.println(httpResponseCode);

      String response = http.getString();
      Serial.println(response);

      http.end();
    }
    else {
      Serial.println("WiFi terputus!");
    }

    // reset buffer
    dataCount = 0;
  }
}