/* ============================================================================
 * Example: Running Another Project with Background Dashboard Monitoring
 * 
 * This example shows how you can run any project (e.g. blinking built-in LED,
 * reading sensors, robotics, AI math) while keeping the ESP32 Web Dashboard
 * active in the background.
 * ============================================================================ */

#include <Arduino.h>
#include "ESP32Dashboard.h"

// Wi-Fi Credentials
const char* WIFI_SSID     = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// Built-in LED on most ESP32 Dev boards is GPIO 2
const int LED_PIN = 2;

// Simulated project sensor/state variable
int sensorValue = 0;
int loopCounter = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(LED_PIN, OUTPUT);

  // 1. Start the Web Dashboard in the background on Core 0
  Dashboard.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.println("[PROJECT] Main project initialized on Core " + String(xPortGetCoreID()));
}

void loop() {
  // ==========================================================================
  // YOUR MAIN PROJECT LOGIC (Runs on Core 1 at full speed)
  // ==========================================================================

  // Example: Blink LED every 500ms
  digitalWrite(LED_PIN, HIGH);
  delay(500);
  digitalWrite(LED_PIN, LOW);
  delay(500);

  loopCounter++;
  sensorValue = random(20, 35); // Simulated sensor reading

  // 2. (Optional) Feed live custom variables into the dashboard API!
  // This will appear seamlessly in the status JSON
  Dashboard.setCustomMetric("\"sensorValue\": " + String(sensorValue) + ", \"loopCount\": " + String(loopCounter));

  Serial.println("[PROJECT] Cycle #" + String(loopCounter) + " | Sensor: " + String(sensorValue) + " | Free RAM: " + String(ESP.getFreeHeap()));
}
