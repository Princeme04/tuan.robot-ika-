#ifndef ESP32_DASHBOARD_H
#define ESP32_DASHBOARD_H

#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <LittleFS.h>
#include <esp_system.h>
#include <esp_chip_info.h>
#include "dashboard_ui.h"

/**
 * ESP32Dashboard Class
 * 
 * Runs a standalone web server and REST API monitoring service
 * in a dedicated FreeRTOS background task (Core 0).
 * 
 * This allows your main project code in setup() and loop() (Core 1)
 * to run freely at full speed without any delays or blocking from web traffic!
 */
class ESP32Dashboard {
private:
  WebServer* _server;
  TaskHandle_t _taskHandle;
  bool _shouldRestart;
  unsigned long _restartTime;
  String _customJsonData;
  portMUX_TYPE _mux;

  static void serverTaskWrapper(void* parameter) {
    ESP32Dashboard* instance = static_cast<ESP32Dashboard*>(parameter);
    instance->runServerLoop();
  }

  void runServerLoop() {
    Serial.println("[DASHBOARD] Background monitor task started on Core " + String(xPortGetCoreID()));
    
    while (true) {
      if (_server != nullptr) {
        _server->handleClient();
      }

      // Check for scheduled reboot
      if (_shouldRestart && (millis() - _restartTime >= 1000)) {
        Serial.println("[SYSTEM] Executing scheduled reboot now...");
        vTaskDelay(pdMS_TO_TICKS(100));
        ESP.restart();
      }

      // Yield 2ms to prevent watchdog starvation on Core 0
      vTaskDelay(pdMS_TO_TICKS(2));
    }
  }

  String getResetReasonString(esp_reset_reason_t reason) {
    switch (reason) {
      case ESP_RST_POWERON:   return "Power-on event";
      case ESP_RST_EXT:       return "External pin reset";
      case ESP_RST_SW:        return "Software reset via esp_restart";
      case ESP_RST_PANIC:     return "Software exception / panic";
      case ESP_RST_INT_WDT:   return "Interrupt Watchdog reset";
      case ESP_RST_TASK_WDT:  return "Task Watchdog reset";
      case ESP_RST_WDT:       return "Other Watchdog reset";
      case ESP_RST_DEEPSLEEP: return "Wakeup from Deep Sleep";
      case ESP_RST_BROWNOUT:  return "Brownout reset (Voltage drop)";
      case ESP_RST_SDIO:      return "Reset over SDIO";
      default:                return "Unknown reset reason";
    }
  }

  String getContentType(String filename) {
    if (filename.endsWith(".html") || filename.endsWith(".htm")) return "text/html";
    else if (filename.endsWith(".css")) return "text/css";
    else if (filename.endsWith(".js"))  return "application/javascript";
    else if (filename.endsWith(".json")) return "application/json";
    else if (filename.endsWith(".ico")) return "image/x-icon";
    else if (filename.endsWith(".svg")) return "image/svg+xml";
    else if (filename.endsWith(".png")) return "image/png";
    else if (filename.endsWith(".jpg") || filename.endsWith(".jpeg")) return "image/jpeg";
    return "text/plain";
  }

  bool handleFileRead(String path) {
    if (path.endsWith("/")) path += "index.html";
    String contentType = getContentType(path);

    if (LittleFS.exists(path)) {
      File file = LittleFS.open(path, "r");
      if (path.endsWith(".html")) {
        _server->sendHeader("Cache-Control", "no-cache, no-store, must-revalidate");
      } else {
        _server->sendHeader("Cache-Control", "max-age=3600");
      }
      _server->streamFile(file, contentType);
      file.close();
      return true;
    }
    return false;
  }

  void handleStatus() {
    unsigned long uptimeSeconds = millis() / 1000;
    uint32_t freeHeap = ESP.getFreeHeap();
    uint32_t heapSize = ESP.getHeapSize();
    int rssi = WiFi.status() == WL_CONNECTED ? WiFi.RSSI() : 0;
    uint32_t cpuFreq = ESP.getCpuFreqMHz();
    String ip = WiFi.localIP().toString();

    String json = "{";
    json += "\"status\":\"online\",";
    json += "\"uptime\":" + String(uptimeSeconds) + ",";
    json += "\"freeHeap\":" + String(freeHeap) + ",";
    json += "\"heapSize\":" + String(heapSize) + ",";
    json += "\"wifiRSSI\":" + String(rssi) + ",";
    json += "\"cpuFrequency\":" + String(cpuFreq) + ",";
    json += "\"ip\":\"" + ip + "\"";

    // Append any custom project metrics if provided
    portENTER_CRITICAL(&_mux);
    if (_customJsonData.length() > 0) {
      json += "," + _customJsonData;
    }
    portEXIT_CRITICAL(&_mux);

    json += "}";

    _server->sendHeader("Access-Control-Allow-Origin", "*");
    _server->sendHeader("Cache-Control", "no-cache, no-store, must-revalidate");
    _server->send(200, "application/json", json);
  }

  void handleSystemInfo() {
    esp_chip_info_t chipInfo;
    esp_chip_info(&chipInfo);

    String chipModel = ESP.getChipModel();
    uint8_t chipRevision = ESP.getChipRevision();
    uint8_t cpuCores = ESP.getChipCores();
    uint32_t cpuFreq = ESP.getCpuFreqMHz();
    uint32_t flashSize = ESP.getFlashChipSize();
    uint32_t flashSpeed = ESP.getFlashChipSpeed();
    uint32_t totalHeap = ESP.getHeapSize();
    uint32_t freeHeap = ESP.getFreeHeap();
    uint32_t minFreeHeap = ESP.getMinFreeHeap();
    uint32_t maxAllocHeap = ESP.getMaxAllocHeap();
    uint32_t sketchSize = ESP.getSketchSize();
    uint32_t freeSketchSpace = ESP.getFreeSketchSpace();
    String sdkVer = ESP.getSdkVersion();
    String resetReason = getResetReasonString(esp_reset_reason());

    String json = "{";
    json += "\"chipModel\":\"" + chipModel + "\",";
    json += "\"chipRevision\":" + String(chipRevision) + ",";
    json += "\"cpuCores\":" + String(cpuCores) + ",";
    json += "\"cpuFrequency\":" + String(cpuFreq) + ",";
    json += "\"flashSize\":" + String(flashSize) + ",";
    json += "\"flashSpeed\":" + String(flashSpeed) + ",";
    json += "\"heapSize\":" + String(totalHeap) + ",";
    json += "\"freeHeap\":" + String(freeHeap) + ",";
    json += "\"minFreeHeap\":" + String(minFreeHeap) + ",";
    json += "\"maxAllocHeap\":" + String(maxAllocHeap) + ",";
    json += "\"sketchSize\":" + String(sketchSize) + ",";
    json += "\"freeSketchSpace\":" + String(freeSketchSpace) + ",";
    json += "\"resetReason\":\"" + resetReason + "\",";
    json += "\"sdkVersion\":\"" + sdkVer + "\"";
    json += "}";

    _server->sendHeader("Access-Control-Allow-Origin", "*");
    _server->sendHeader("Cache-Control", "no-cache, no-store, must-revalidate");
    _server->send(200, "application/json", json);
  }

  void handleWifiInfo() {
    bool isConnected = (WiFi.status() == WL_CONNECTED);
    String ssid = isConnected ? WiFi.SSID() : "Disconnected";
    String ip = isConnected ? WiFi.localIP().toString() : "0.0.0.0";
    String gateway = isConnected ? WiFi.gatewayIP().toString() : "0.0.0.0";
    String subnet = isConnected ? WiFi.subnetMask().toString() : "0.0.0.0";
    String mac = WiFi.macAddress();
    int rssi = isConnected ? WiFi.RSSI() : 0;
    int channel = isConnected ? WiFi.channel() : 0;
    String bssid = isConnected ? WiFi.BSSIDstr() : "00:00:00:00:00:00";
    String status = isConnected ? "connected" : "disconnected";

    String json = "{";
    json += "\"ssid\":\"" + ssid + "\",";
    json += "\"ip\":\"" + ip + "\",";
    json += "\"gateway\":\"" + gateway + "\",";
    json += "\"subnetMask\":\"" + subnet + "\",";
    json += "\"mac\":\"" + mac + "\",";
    json += "\"rssi\":" + String(rssi) + ",";
    json += "\"channel\":" + String(channel) + ",";
    json += "\"bssid\":\"" + bssid + "\",";
    json += "\"status\":\"" + status + "\"";
    json += "}";

    _server->sendHeader("Access-Control-Allow-Origin", "*");
    _server->sendHeader("Cache-Control", "no-cache, no-store, must-revalidate");
    _server->send(200, "application/json", json);
  }

  void handleRestart() {
    Serial.println("[HTTP] POST /api/restart received. Scheduling reboot...");
    String json = "{\"status\":\"restarting\",\"message\":\"ESP32 is rebooting in 1 second...\"}";
    _server->sendHeader("Access-Control-Allow-Origin", "*");
    _server->send(200, "application/json", json);

    _shouldRestart = true;
    _restartTime = millis();
  }

  void handleRootOrNotFound() {
    if (handleFileRead(_server->uri())) return;

    if (_server->uri().startsWith("/api/")) {
      String json = "{\"error\":404,\"message\":\"API endpoint not found: " + _server->uri() + "\"}";
      _server->sendHeader("Access-Control-Allow-Origin", "*");
      _server->send(404, "application/json", json);
      return;
    }

    _server->sendHeader("Cache-Control", "no-cache, no-store, must-revalidate");
    _server->send_P(200, "text/html", DASHBOARD_HTML);
  }

public:
  ESP32Dashboard() : _server(nullptr), _taskHandle(nullptr), _shouldRestart(false), _restartTime(0), _customJsonData("") {
    _mux = portMUX_INITIALIZER_UNLOCKED;
  }

  /**
   * Starts the Dashboard web server in a dedicated FreeRTOS background task.
   * 
   * @param ssid Wi-Fi SSID (Optional if already connected in user code)
   * @param password Wi-Fi Password (Optional)
   * @param port HTTP Port (default 80)
   */
  void begin(const char* ssid = nullptr, const char* password = nullptr, uint16_t port = 80) {
    LittleFS.begin(true);

    // Connect to Wi-Fi if credentials are provided
    if (ssid != nullptr && password != nullptr && WiFi.status() != WL_CONNECTED) {
      Serial.println("\n[DASHBOARD] Connecting to Wi-Fi: " + String(ssid));
      WiFi.mode(WIFI_STA);
      WiFi.begin(ssid, password);

      unsigned long start = millis();
      while (WiFi.status() != WL_CONNECTED && millis() - start < 15000) {
        delay(400);
        Serial.print(".");
      }
      Serial.println();

      if (WiFi.status() == WL_CONNECTED) {
        Serial.println("[DASHBOARD] Wi-Fi connected! IP: http://" + WiFi.localIP().toString());
      } else {
        Serial.println("[DASHBOARD] Wi-Fi connection timeout. Please check credentials.");
      }
    }

    // Allocate WebServer
    if (_server == nullptr) {
      _server = new WebServer(port);
    }

    // Setup routes
    _server->on("/api/status", HTTP_GET, [this]() { this->handleStatus(); });
    _server->on("/api/system", HTTP_GET, [this]() { this->handleSystemInfo(); });
    _server->on("/api/wifi",   HTTP_GET, [this]() { this->handleWifiInfo(); });
    _server->on("/api/restart", HTTP_POST, [this]() { this->handleRestart(); });
    _server->on("/", HTTP_GET, [this]() { this->handleRootOrNotFound(); });
    _server->onNotFound([this]() { this->handleRootOrNotFound(); });

    _server->begin();
    Serial.println("[DASHBOARD] Web server listening on port " + String(port));

    // Launch background task on Core 0 with 4KB stack and priority 1
    if (_taskHandle == nullptr) {
      xTaskCreatePinnedToCore(
        serverTaskWrapper,       // Task function
        "DashboardTask",         // Name
        4096,                    // Stack size (bytes)
        this,                    // Parameter
        1,                       // Priority
        &_taskHandle,            // Task handle
        0                        // Core ID (0 = Protocol Core)
      );
    }
  }

  /**
   * Set custom key-value pairs to appear in the live status API.
   * Example: setCustomMetric("\"temperature\": 27.5, \"relayState\": \"ON\"");
   */
  void setCustomMetric(const String& customJsonFragment) {
    portENTER_CRITICAL(&_mux);
    _customJsonData = customJsonFragment;
    portEXIT_CRITICAL(&_mux);
  }

  /**
   * Returns the local IP string
   */
  String getIP() {
    return WiFi.localIP().toString();
  }
};

// Global singleton instance for easy drop-in use
extern ESP32Dashboard Dashboard;
#ifndef ESP32_DASHBOARD_INSTANCE_DEFINED
#define ESP32_DASHBOARD_INSTANCE_DEFINED
ESP32Dashboard Dashboard;
#endif

#endif // ESP32_DASHBOARD_H
