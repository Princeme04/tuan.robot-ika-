/* ============================================================================
 * ESP32 Web Dashboard - Main Firmware
 * 
 * Runs a standalone web server and REST API monitoring service
 * automatically in the background using ESP32's Dual-Core FreeRTOS (Core 0).
 * 
 * Features:
 *  - 1-Click Upload (No filesystem plugins or separate data files needed!)
 *  - Zero external hardware required
 *  - Runs in the background without blocking your loop()
 * ============================================================================ */

#include <Arduino.h>
#include "ESP32Dashboard.h"

// ============================================================================
// WI-FI CONFIGURATION
// Replace with your 2.4 GHz Wi-Fi network credentials.
// ============================================================================
const char* WIFI_SSID     = "HUAWEI-2.4G";
const char* WIFI_PASSWORD = "56785678";

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("========================================");
  Serial.println("   ESP32 Web Dashboard & System Monitor ");
  Serial.println("========================================");

  // Start the dashboard monitor in the background (Core 0)
  Dashboard.begin(WIFI_SSID, WIFI_PASSWORD);
}

void loop() {
  // ==========================================================================
  // YOUR MAIN PROJECT CODE GOES HERE (Runs on Core 1)
  //
  // You can run any sensor reading, motor control, math calculations,
  // or logic here. The dashboard runs automatically in the background
  // on Core 0 without slowing down your project!
  // ==========================================================================

  // Example: Print a heartbeat every 5 seconds to demonstrate loop is running
  static unsigned long lastHeartbeat = 0;
  if (millis() - lastHeartbeat > 5000) {
    lastHeartbeat = millis();
    Serial.println("[MAIN PROJECT] Loop running smoothly on Core " + String(xPortGetCoreID()) + " | Free RAM: " + String(ESP.getFreeHeap()) + " bytes");
  }

  delay(10);
}
