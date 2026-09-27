# ESP32 Web Dashboard

A modern, responsive, standalone system monitoring web dashboard for ESP32. The ESP32 acts as a self-contained web server and REST API backend, serving a dark-neutral dashboard to any PC, smartphone, or tablet browser on the local Wi-Fi network without requiring external sensors, displays, cloud services, or CDN dependencies.

---

## 1. Features

- **Zero External Hardware Required**: Uses the ESP32's internal registers, timers, flash memory, and Wi-Fi subsystem.
- **REST-like API**:
  - `GET /api/status`: Real-time system health polled every ~1s (Uptime, Free Heap, RSSI, CPU, IP).
  - `GET /api/system`: Hardware model, core count, flash specs, watermark heap, and SDK versions.
  - `GET /api/wifi`: Network credentials state, Gateway, Subnet, MAC address, Channel, and BSSID.
  - `POST /api/restart`: Gracefully schedules a microcontroller software reboot with client status notification.
- **Modern Responsive Dashboard**:
  - Dark-neutral card-based layout with clean CSS variables.
  - Real-time live status indicator (`● ONLINE` vs `● OFFLINE`).
  - Heap memory usage visualization with calculated percentage and progress bar.
  - RSSI Wi-Fi signal indicator with level bars and qualitative ratings (*Excellent*, *Good*, *Fair*, *Weak*).
  - Human-readable uptime formatter (e.g. `2d 4h 21m 10s`).
  - Mobile & desktop responsive layout.
- **Zero External Internet Dependencies**: Served entirely from the ESP32 (no Google Fonts, Bootstrap, React, or CDNs).

---

## 2. Architecture & Concept

```text
                    Local Wi-Fi Network
                             │
        ┌────────────────────┴────────────────────┐
        │                                         │
    PC Browser                              Phone Browser
        │                                         │
        └────────────────────┬────────────────────┘
                             │ (HTTP Port 80)
                             ▼
                     ESP32 Web Server
                             │
             ┌───────────────┴───────────────┐
             │                               │
         REST API                      Web Dashboard
  (/api/status, /api/system)       (index.html, style.css, app.js)
             │                               │
             └───────────────┬───────────────┘
                             ▼
                   ESP32 Internal Metrics
            (Free Heap, Flash, CPU, RSSI, etc.)
```

### Technical Design Choices

1. **Why `WebServer.h`?**
   `WebServer.h` is built directly into the official ESP32 Arduino Core. It is stable, officially maintained by Espressif, lightweight, and does not suffer from third-party library version incompatibilities.
2. **Why `LittleFS`?**
   `LittleFS` is the modern, power-loss resilient filesystem for ESP32 flash memory, replacing the legacy SPIFFS with better performance and lower RAM consumption.
3. **Safe Asynchronous Restart Pattern**:
   When `POST /api/restart` is received, the server returns an HTTP 200 JSON payload to the browser immediately, arming a 1-second delayed flag. The actual `ESP.restart()` call executes in `loop()`, ensuring the network socket cleanly flushes without dropping the client's HTTP response.

---

## 3. Project Structure

```text
ESP32-Web-Dashboard/
│
├── ESP32-Web-Dashboard.ino      # Main Arduino firmware, REST API, & Web Server
│
├── data/                        # Files stored in ESP32 Flash via LittleFS
│   ├── index.html               # Semantic HTML5 Dashboard Structure
│   ├── style.css                # Pure CSS3 styling & CSS variables
│   └── app.js                   # Vanilla JS Polling, DOM Updates, & Reboot Logic
│
└── README.md                    # Project Documentation & API Guide
```

---

## 4. Hardware & Software Requirements

### Hardware
* ESP32 Development Board (e.g., ESP32 NodeMCU, ESP32-WROOM-32, etc.)
* Micro-USB or USB-C data cable (ensure it carries data, not power-only).

### Software
* [Arduino IDE](https://www.arduino.cc/en/software) (Version 1.8.19+ or 2.x)
* **ESP32 Arduino Board Package**:
  - In Arduino IDE: `File` → `Preferences` → `Additional Boards Manager URLs`:
    ```text
    https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
    ```
  - Open `Tools` → `Board` → `Boards Manager`, search for `esp32` and install.
* **Arduino ESP32 LittleFS Filesystem Plugin** (For uploading the `data/` folder):
  - For Arduino IDE 2.x: [arduino-littlefs-upload](https://github.com/earlephilhower/arduino-littlefs-upload)
  - For Arduino IDE 1.8.x: [arduino-esp32fs-plugin](https://github.com/lorol/arduino-esp32fs-plugin)

---

## 5. Installation & Setup

### Step 1: Configure Wi-Fi Credentials
Open `ESP32-Web-Dashboard.ino` in Arduino IDE and locate lines 30–31:

```cpp
const char* WIFI_SSID     = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
```
Change `YOUR_WIFI_NAME` and `YOUR_WIFI_PASSWORD` to match your local 2.4 GHz Wi-Fi network.

### Step 2: Configure Board Settings
In the Arduino IDE menu, select:
- **Board**: `ESP32 Dev Module` (or your specific board model)
- **Upload Speed**: `921600` (or `115200`)
- **Flash Size**: `4MB (32Mb)`
- **Partition Scheme**: `Default 4MB with spiffs (1.2MB APP/1.5MB SPIFFS)` or `Minimal SPIFFS (1.9MB APP with OTA/190KB SPIFFS)`
- **Port**: Select your active COM port (e.g., `COM3`, `COM5`).

### Step 3: Upload Firmware
Click the **Upload** arrow in Arduino IDE to flash `ESP32-Web-Dashboard.ino`.

### Step 4: Upload the `data` Folder to LittleFS
1. Ensure the Serial Monitor is **closed**.
2. Run the LittleFS upload command from Arduino IDE:
   - **Arduino IDE 2.x**: Press `Ctrl+Shift+P`, type `Upload LittleFS to Pico/ESP8266/ESP32`, and press Enter.
   - **Arduino IDE 1.8.x**: Click `Tools` → `ESP32 Sketch Data Upload`.
3. Wait for the upload to complete.

### Step 5: Open the Dashboard
1. Open the Arduino **Serial Monitor** at baud rate `115200`.
2. Press the `EN` / `RST` button on your ESP32 board.
3. You will see the connection log:
   ```text
   ================================
   ESP32 Web Dashboard
   ================================
   [WIFI] Connecting to Wi-Fi...
   [WIFI] Connected!
   [WIFI] IP Address: 192.168.1.50
   [WIFI] RSSI: -47 dBm
   [HTTP] Web server started.
   [HTTP] Open http://192.168.1.50 in your browser.
   ================================
   ```
4. Open your browser on any PC or phone connected to the same Wi-Fi and navigate to:
   ```text
   http://192.168.1.50
   ```

---

## 6. REST API Documentation

All API responses return JSON with standard `Access-Control-Allow-Origin: *` headers.

### 1. `GET /api/status`
Lightweight real-time metrics polled every 1000ms.

**Example Response:**
```json
{
  "status": "online",
  "uptime": 3827,
  "freeHeap": 182340,
  "heapSize": 328000,
  "wifiRSSI": -47,
  "cpuFrequency": 240,
  "ip": "192.168.1.50"
}
```

### 2. `GET /api/system`
Complete system and hardware specifications.

**Example Response:**
```json
{
  "chipModel": "ESP32-D0WDQ6",
  "chipRevision": 1,
  "cpuCores": 2,
  "cpuFrequency": 240,
  "flashSize": 4194304,
  "flashSpeed": 80000000,
  "heapSize": 328000,
  "freeHeap": 182340,
  "minFreeHeap": 170120,
  "maxAllocHeap": 110592,
  "sketchSize": 254816,
  "freeSketchSpace": 1048576,
  "resetReason": "Power-on event",
  "sdkVersion": "v4.4.4"
}
```

### 3. `GET /api/wifi`
Wi-Fi connection metrics.

**Example Response:**
```json
{
  "ssid": "MyHomeNetwork",
  "ip": "192.168.1.50",
  "gateway": "192.168.1.1",
  "subnetMask": "255.255.255.0",
  "mac": "24:6F:28:XX:XX:XX",
  "rssi": -47,
  "channel": 6,
  "bssid": "A0:04:60:XX:XX:XX",
  "status": "connected"
}
```

### 4. `POST /api/restart`
Initiates an asynchronous reboot of the ESP32 after a 1000ms delay.

**Example Response:**
```json
{
  "status": "restarting",
  "message": "ESP32 is rebooting in 1 second..."
}
```

---

## 7. Troubleshooting Guide

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **ESP32 COM port does not appear** | Missing USB-to-UART driver (CP2102 or CH340) or bad USB cable | Install the Silicon Labs CP210x or WCH CH340 driver. Use a data-capable USB cable. |
| **A fatal error occurred: Failed to connect to ESP32** | Board not in bootloader mode | Hold down the physical `BOOT` button on the ESP32 while the upload displays `Connecting........_____`. |
| **Wi-Fi connection fails / hangs on `Connecting...`** | Incorrect credentials or 5GHz network | Ensure SSID/Password are correct and you are connecting to a **2.4 GHz** Wi-Fi band. ESP32 does not support 5 GHz Wi-Fi. |
| **Browser says `ESP32 Web Server is Running! ... files not found in LittleFS`** | The sketch was uploaded, but the `data/` folder was not flashed | Run the **Upload LittleFS** tool in Arduino IDE to upload `data/index.html`, `style.css`, and `app.js`. |
| **Browser cannot load `http://192.168.1.xxx`** | Client device is on a different subnet or guest network | Verify that your phone/PC is on the same local network and AP isolation is disabled. |
| **Status says `● OFFLINE`** | HTTP requests timed out or ESP32 was disconnected | Verify the ESP32 has power and check the Serial Monitor for error logs. |

---

## 8. Security & Scope

> [!WARNING]
> This project is created for **local network learning and private lab environments**. It does not implement password authentication, CSRF tokens, or HTTPS. **Do NOT forward port 80 or expose this dashboard directly to the public internet.**
# tuan.robot-ika-
