import base64
import os
from PIL import Image

dir_base = r"C:\Kuliahhh\piranticerdas\esp32 web\ESP32-Web-Dashboard"
out_bg1 = os.path.join(dir_base, "bg1_opt.jpg")
out_bg2 = os.path.join(dir_base, "bg2_opt.jpg")

# 1. Optimize images
img1 = Image.open(os.path.join(dir_base, "801757.jpg"))
ratio1 = 1100 / float(img1.size[0])
if ratio1 < 1.0:
    img1 = img1.resize((1100, int(float(img1.size[1]) * ratio1)), Image.Resampling.LANCZOS)
img1.save(out_bg1, "JPEG", quality=60, optimize=True)

img2 = Image.open(os.path.join(dir_base, "801771.jpg"))
ratio2 = 1100 / float(img2.size[0])
if ratio2 < 1.0:
    img2 = img2.resize((1100, int(float(img2.size[1]) * ratio2)), Image.Resampling.LANCZOS)
img2.save(out_bg2, "JPEG", quality=62, optimize=True)

with open(out_bg1, "rb") as f:
    bg1_b64 = base64.b64encode(f.read()).decode("utf-8")

with open(out_bg2, "rb") as f:
    bg2_b64 = base64.b64encode(f.read()).decode("utf-8")

header_code = f"""#ifndef DASHBOARD_UI_H
#define DASHBOARD_UI_H

#include <pgmspace.h>

const char DASHBOARD_HTML[] PROGMEM = R\"rawliteral(<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>ESP32 Web Dashboard</title>
  <style>
    :root {{
      --bg-primary: #0b0f19;
      --card-bg: rgba(15, 23, 42, 0.68);
      --card-border: rgba(255, 255, 255, 0.12);
      --card-hover-border: rgba(56, 189, 248, 0.4);
      --text-primary: #ffffff;
      --text-secondary: #cbd5e1;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --accent-hover: #0284c7;
      --accent-dim: rgba(56, 189, 248, 0.2);
      --success: #10b981;
      --success-dim: rgba(16, 185, 129, 0.22);
      --warning: #f59e0b;
      --warning-dim: rgba(245, 158, 11, 0.22);
      --danger: #ef4444;
      --danger-hover: #dc2626;
      --danger-dim: rgba(239, 68, 68, 0.22);
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 16px;
      --shadow-sm: 0 4px 20px rgba(0, 0, 0, 0.4);
      --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    
    body {{
      color: var(--text-primary);
      font-family: var(--font-family);
      font-size: 14px;
      line-height: 1.5;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
      background-color: #0b0f19;
      background-size: cover;
      background-repeat: no-repeat;
      background-attachment: fixed;
      transition: background-image 0.4s ease-in-out;
    }}

    /* Background Themes with Face Visibility Enhancements */
    body.theme-1 {{
      background-image: linear-gradient(to bottom, rgba(11, 15, 25, 0.35), rgba(11, 15, 25, 0.65)), url('data:image/jpeg;base64,{bg1_b64}');
      background-position: center 15%;
    }}

    body.theme-2 {{
      background-image: linear-gradient(to bottom, rgba(11, 15, 25, 0.25), rgba(11, 15, 25, 0.6)), url('data:image/jpeg;base64,{bg2_b64}');
      background-position: right 30%;
    }}

    .app-container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 24px 20px 40px;
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }}

    /* Glassmorphism Header */
    .dashboard-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(15, 23, 42, 0.72);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-lg);
      padding: 16px 24px;
      margin-bottom: 24px;
      box-shadow: var(--shadow-sm);
    }}

    .header-brand {{ display: flex; align-items: center; gap: 16px; }}
    .brand-icon {{
      background: var(--accent-dim);
      color: var(--accent);
      padding: 10px;
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}

    .header-title {{ font-size: 1.35rem; font-weight: 700; letter-spacing: -0.02em; color: var(--text-primary); text-shadow: 0 2px 4px rgba(0,0,0,0.6); }}
    .header-subtitle {{ font-size: 0.82rem; color: var(--text-secondary); }}

    .header-controls {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .header-status {{ text-align: right; display: flex; flex-direction: column; align-items: flex-end; gap: 4px; }}

    .status-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      backdrop-filter: blur(8px);
    }}

    .status-dot {{ width: 8px; height: 8px; border-radius: 50%; background-color: currentColor; box-shadow: 0 0 8px currentColor; }}
    .badge-online {{ background-color: var(--success-dim); color: var(--success); border: 1px solid rgba(16, 185, 129, 0.4); }}
    .badge-offline {{ background-color: var(--danger-dim); color: var(--danger); border: 1px solid rgba(239, 68, 68, 0.4); }}
    .badge-connecting {{ background-color: var(--warning-dim); color: var(--warning); border: 1px solid rgba(245, 158, 11, 0.4); }}
    .last-updated {{ font-size: 0.75rem; color: var(--text-secondary); text-shadow: 0 1px 2px rgba(0,0,0,0.6); }}

    /* Glassmorphic Cards */
    .card {{
      background: var(--card-bg);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-md);
      padding: 20px;
      box-shadow: var(--shadow-sm);
      transition: all 0.25s ease;
    }}
    .card:hover {{ 
      border-color: var(--card-hover-border); 
      transform: translateY(-2px);
      box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    }}

    .metrics-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}

    .metric-card {{ display: flex; flex-direction: column; justify-content: space-between; }}
    .metric-label {{
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-secondary);
      margin-bottom: 8px;
    }}

    .metric-value-row {{ display: flex; align-items: baseline; gap: 8px; margin-bottom: 8px; }}
    .metric-value {{
      font-size: 1.45rem;
      font-weight: 700;
      color: var(--text-primary);
      font-family: var(--font-mono);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      text-shadow: 0 2px 4px rgba(0,0,0,0.4);
    }}

    .metric-footer {{ font-size: 0.75rem; color: var(--text-muted); }}
    .badge-sub {{
      font-size: 0.7rem;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: var(--radius-sm);
      background: rgba(15, 23, 42, 0.8);
      color: var(--text-secondary);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}

    .progress-bar-container {{
      width: 100%;
      height: 6px;
      background-color: rgba(15, 23, 42, 0.8);
      border-radius: 9999px;
      overflow: hidden;
      margin: 6px 0 8px;
      border: 1px solid rgba(255, 255, 255, 0.05);
    }}
    .progress-bar {{ height: 100%; background-color: var(--accent); border-radius: 9999px; transition: width 0.4s ease; box-shadow: 0 0 8px var(--accent); }}

    .signal-bars {{ display: flex; align-items: flex-end; gap: 3px; height: 14px; margin: 6px 0 8px; }}
    .signal-bars .bar {{ width: 4px; background-color: rgba(255,255,255,0.2); border-radius: 1px; transition: background-color 0.2s ease; }}
    .signal-bars .bar-1 {{ height: 25%; }}
    .signal-bars .bar-2 {{ height: 50%; }}
    .signal-bars .bar-3 {{ height: 75%; }}
    .signal-bars .bar-4 {{ height: 100%; }}

    .signal-bars.level-1 .bar-1 {{ background-color: var(--danger); box-shadow: 0 0 6px var(--danger); }}
    .signal-bars.level-2 .bar-1, .signal-bars.level-2 .bar-2 {{ background-color: var(--warning); box-shadow: 0 0 6px var(--warning); }}
    .signal-bars.level-3 .bar-1, .signal-bars.level-3 .bar-2, .signal-bars.level-3 .bar-3 {{ background-color: var(--success); box-shadow: 0 0 6px var(--success); }}
    .signal-bars.level-4 .bar {{ background-color: var(--success); box-shadow: 0 0 6px var(--success); }}

    .details-layout {{ display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 20px; margin-bottom: 24px; }}
    .right-stack {{ display: flex; flex-direction: column; gap: 20px; }}

    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 14px;
      margin-bottom: 16px;
      border-bottom: 1px solid var(--card-border);
    }}
    .card-header-left {{ display: flex; align-items: center; gap: 10px; color: var(--text-primary); }}
    .card-title {{ font-size: 1.05rem; font-weight: 600; text-shadow: 0 1px 3px rgba(0,0,0,0.5); }}

    .info-table {{ display: flex; flex-direction: column; }}
    .info-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 9px 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }}
    .info-row:last-child {{ border-bottom: none; }}
    .info-key {{ color: var(--text-secondary); font-size: 0.85rem; }}
    .info-val {{ color: var(--text-primary); font-size: 0.85rem; font-family: var(--font-mono); font-weight: 500; text-align: right; }}

    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      border: none;
      outline: none;
      transition: all 0.2s ease;
      font-family: var(--font-family);
      backdrop-filter: blur(8px);
    }}
    .btn-sm {{ padding: 5px 12px; font-size: 0.75rem; }}
    .btn-secondary {{ background-color: rgba(15, 23, 42, 0.7); color: var(--text-secondary); border: 1px solid var(--card-border); }}
    .btn-secondary:hover {{ background-color: rgba(30, 41, 59, 0.9); color: var(--text-primary); border-color: var(--accent); }}
    .btn-danger {{ background-color: rgba(239, 68, 68, 0.85); color: #ffffff; border: 1px solid rgba(239, 68, 68, 0.5); }}
    .btn-danger:hover {{ background-color: var(--danger-hover); box-shadow: 0 0 12px var(--danger); }}
    .btn-theme {{ background: var(--accent-dim); color: var(--accent); border: 1px solid rgba(56, 189, 248, 0.4); }}
    .btn-theme:hover {{ background: rgba(56, 189, 248, 0.3); }}

    .action-desc {{ color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 16px; line-height: 1.5; }}
    .action-btn-group {{ display: flex; gap: 12px; }}

    .text-accent {{ color: var(--accent); }}
    .text-success {{ color: var(--success); }}
    .text-warning {{ color: var(--warning); }}
    .text-danger {{ color: var(--danger); }}
    .text-muted {{ color: var(--text-muted); }}

    .modal-overlay {{
      position: fixed;
      inset: 0;
      background-color: rgba(0, 0, 0, 0.8);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      padding: 20px;
      backdrop-filter: blur(6px);
    }}
    .modal-overlay.hidden {{ display: none; }}
    .modal-card {{
      background-color: rgba(17, 24, 39, 0.92);
      backdrop-filter: blur(20px);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-lg);
      padding: 28px;
      max-width: 440px;
      width: 100%;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.7);
      text-align: center;
    }}
    .modal-title {{ font-size: 1.2rem; font-weight: 700; margin-bottom: 12px; color: var(--text-primary); }}
    .modal-text {{ font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 24px; line-height: 1.5; }}
    .modal-actions {{ display: flex; justify-content: flex-end; gap: 12px; }}

    .spinner {{
      width: 42px;
      height: 42px;
      border: 4px solid rgba(255,255,255,0.1);
      border-top-color: var(--accent);
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 16px;
    }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    .reboot-countdown {{ font-family: var(--font-mono); font-size: 1.6rem; font-weight: 700; color: var(--accent); margin-top: 10px; }}
    .hidden {{ display: none !important; }}

    .dashboard-footer {{
      margin-top: auto;
      text-align: center;
      color: var(--text-muted);
      font-size: 0.8rem;
      padding-top: 20px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      text-shadow: 0 1px 3px rgba(0,0,0,0.7);
    }}
    .footer-sub {{ font-size: 0.72rem; margin-top: 4px; color: var(--text-secondary); }}

    @media (max-width: 900px) {{ .details-layout {{ grid-template-columns: 1fr; }} }}
    @media (max-width: 650px) {{
      .dashboard-header {{ flex-direction: column; align-items: flex-start; gap: 14px; }}
      .header-controls {{ width: 100%; justify-content: space-between; }}
      .header-status {{ text-align: left; align-items: flex-start; }}
      .metrics-grid {{ grid-template-columns: 1fr 1fr; }}
    }}
    @media (max-width: 400px) {{ .metrics-grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body class=\"theme-1\">
  <div class=\"app-container\">
    
    <header class=\"dashboard-header\">
      <div class=\"header-brand\">
        <div class=\"brand-icon\">
          <svg viewBox=\"0 0 24 24\" width=\"24\" height=\"24\" stroke=\"currentColor\" stroke-width=\"2\" fill=\"none\" stroke-linecap=\"round\" stroke-linejoin=\"round\">
            <rect x=\"4\" y=\"4\" width=\"16\" height=\"16\" rx=\"2\" ry=\"2\"></rect>
            <rect x=\"9\" y=\"9\" width=\"6\" height=\"6\"></rect>
            <line x1=\"9\" y1=\"1\" x2=\"9\" y2=\"4\"></line>
            <line x1=\"15\" y1=\"1\" x2=\"15\" y2=\"4\"></line>
            <line x1=\"9\" y1=\"20\" x2=\"9\" y2=\"23\"></line>
            <line x1=\"15\" y1=\"20\" x2=\"15\" y2=\"23\"></line>
            <line x1=\"20\" y1=\"9\" x2=\"23\" y2=\"9\"></line>
            <line x1=\"20\" y1=\"14\" x2=\"23\" y2=\"14\"></line>
            <line x1=\"1\" y1=\"9\" x2=\"4\" y1=\"9\"></line>
            <line x1=\"1\" y1=\"14\" x2=\"4\" y1=\"14\"></line>
          </svg>
        </div>
        <div>
          <h1 class=\"header-title\">ESP32 Dashboard</h1>
          <p class=\"header-subtitle\">ESP32 Web Monitor &amp; Control</p>
        </div>
      </div>

      <div class=\"header-controls\">
        <button id=\"btn-switch-bg\" class=\"btn btn-sm btn-theme\" title=\"Toggle Wallpaper\">
          <svg viewBox=\"0 0 24 24\" width=\"14\" height=\"14\" stroke=\"currentColor\" stroke-width=\"2\" fill=\"none\">
            <rect x=\"3\" y=\"3\" width=\"18\" height=\"18\" rx=\"2\" ry=\"2\"></rect>
            <circle cx=\"8.5\" cy=\"8.5\" r=\"1.5\"></circle>
            <polyline points=\"21 15 16 10 5 21\"></polyline>
          </svg>
          <span id=\"bg-toggle-text\">Close-up</span>
        </button>

        <div class=\"header-status\">
          <div id=\"connection-badge\" class=\"status-badge badge-connecting\">
            <span class=\"status-dot\"></span>
            <span id=\"connection-text\">CONNECTING</span>
          </div>
          <div id=\"last-updated-text\" class=\"last-updated\">Connecting to ESP32...</div>
        </div>
      </div>
    </header>

    <main class=\"dashboard-main\">
      <section class=\"metrics-grid\">
        <div class=\"card metric-card\">
          <div class=\"metric-label\">STATUS</div>
          <div class=\"metric-value-row\">
            <span id=\"metric-status\" class=\"metric-value text-muted\">--</span>
          </div>
          <div class=\"metric-footer\" id=\"metric-status-sub\">Checking node health</div>
        </div>

        <div class=\"card metric-card\">
          <div class=\"metric-label\">UPTIME</div>
          <div class=\"metric-value-row\">
            <span id=\"metric-uptime\" class=\"metric-value\">--</span>
          </div>
          <div class=\"metric-footer\" id=\"metric-uptime-raw\">System active time</div>
        </div>

        <div class=\"card metric-card\">
          <div class=\"metric-label\">FREE HEAP</div>
          <div class=\"metric-value-row\">
            <span id=\"metric-free-heap\" class=\"metric-value\">--</span>
          </div>
          <div class=\"progress-bar-container\">
            <div id=\"heap-progress-bar\" class=\"progress-bar\" style=\"width: 0%;\"></div>
          </div>
          <div class=\"metric-footer\" id=\"metric-heap-percentage\">Calculating usage...</div>
        </div>

        <div class=\"card metric-card\">
          <div class=\"metric-label\">WIFI SIGNAL</div>
          <div class=\"metric-value-row\">
            <span id=\"metric-rssi\" class=\"metric-value\">--</span>
            <span id=\"rssi-rating-badge\" class=\"badge-sub\">--</span>
          </div>
          <div class=\"signal-bars\" id=\"signal-bars\">
            <span class=\"bar bar-1\"></span>
            <span class=\"bar bar-2\"></span>
            <span class=\"bar bar-3\"></span>
            <span class=\"bar bar-4\"></span>
          </div>
          <div class=\"metric-footer\" id=\"metric-rssi-sub\">RSSI Signal strength</div>
        </div>

        <div class=\"card metric-card\">
          <div class=\"metric-label\">CPU FREQUENCY</div>
          <div class=\"metric-value-row\">
            <span id=\"metric-cpu\" class=\"metric-value\">--</span>
          </div>
          <div class=\"metric-footer\" id=\"metric-cpu-cores\">Dual Core Xtensa LX6</div>
        </div>

        <div class=\"card metric-card\">
          <div class=\"metric-label\">IP ADDRESS</div>
          <div class=\"metric-value-row\">
            <span id=\"metric-ip\" class=\"metric-value text-accent\">--</span>
          </div>
          <div class=\"metric-footer\" id=\"metric-mac\">MAC: --:--:--:--:--:--</div>
        </div>
      </section>

      <div class=\"details-layout\">
        <section class=\"card detail-card\">
          <div class=\"card-header\">
            <div class=\"card-header-left\">
              <svg viewBox=\"0 0 24 24\" width=\"20\" height=\"20\" stroke=\"currentColor\" stroke-width=\"2\" fill=\"none\">
                <rect x=\"2\" y=\"2\" width=\"20\" height=\"8\" rx=\"2\" ry=\"2\"></rect>
                <rect x=\"2\" y=\"14\" width=\"20\" height=\"8\" rx=\"2\" ry=\"2\"></rect>
                <line x1=\"6\" y1=\"6\" x2=\"6.01\" y2=\"6\"></line>
                <line x1=\"6\" y1=\"18\" x2=\"6.01\" y2=\"18\"></line>
              </svg>
              <h2 class=\"card-title\">System Information</h2>
            </div>
            <button class=\"btn btn-secondary btn-sm\" id=\"btn-refresh-system\" title=\"Refresh System Info\">Refresh</button>
          </div>
          
          <div class=\"info-table\">
            <div class=\"info-row\"><span class=\"info-key\">Chip Model</span><span class=\"info-val\" id=\"sys-chip-model\">--</span></div>
            <div class=\"info-row\"><span class=\"info-key\">Chip Revision</span><span class=\"info-val\" id=\"sys-chip-rev\">--</span></div>
            <div class=\"info-row\"><span class=\"info-key\">CPU Cores</span><span class=\"info-val\" id=\"sys-cpu-cores\">--</span></div>
            <div class=\"info-row\"><span class=\"info-key\">CPU Clock Speed</span><span class=\"info-val\" id=\"sys-cpu-freq\">--</span></div>
            <div class=\"info-row\"><span class=\"info-key\">Total Heap RAM</span><span class=\"info-val\" id=\"sys-total-heap\">--</span></div>
            <div class=\"info-row\"><span class=\"info-key\">Free Heap RAM</span><span class=\"info-val\" id=\"sys-free-heap\">--</span></div>
            <div class=\"info-row\"><span class=\"info-key\">Min Free Heap (Watermark)</span><span class=\"info-val\" id=\"sys-min-heap\">--</span></div>
            <div class=\"info-row\"><span class=\"info-key\">Max Allocatable Heap Block</span><span class=\"info-val\" id=\"sys-max-alloc\">--</span></div>
            <div class=\"info-row\"><span class=\"info-key\">Flash Memory Size</span><span class=\"info-val\" id=\"sys-flash-size\">--</span></div>
            <div class=\"info-row\"><span class=\"info-key\">Flash Memory Speed</span><span class=\"info-val\" id=\"sys-flash-speed\">--</span></div>
            <div class=\"info-row\"><span class=\"info-key\">Firmware Sketch Size</span><span class=\"info-val\" id=\"sys-sketch-size\">--</span></div>
            <div class=\"info-row\"><span class=\"info-key\">Free Flash Space for Sketch</span><span class=\"info-val\" id=\"sys-free-sketch\">--</span></div>
            <div class=\"info-row\"><span class=\"info-key\">Reset Reason</span><span class=\"info-val\" id=\"sys-reset-reason\">--</span></div>
            <div class=\"info-row\"><span class=\"info-key\">ESP-IDF SDK Version</span><span class=\"info-val\" id=\"sys-sdk-ver\">--</span></div>
          </div>
        </section>

        <div class=\"right-stack\">
          <section class=\"card detail-card\">
            <div class=\"card-header\">
              <div class=\"card-header-left\">
                <svg viewBox=\"0 0 24 24\" width=\"20\" height=\"20\" stroke=\"currentColor\" stroke-width=\"2\" fill=\"none\">
                  <path d=\"M5 12.55a11 11 0 0 1 14.08 0\"></path>
                  <path d=\"M1.42 9a16 16 0 0 1 21.16 0\"></path>
                  <path d=\"M8.53 16.11a6 6 0 0 1 6.95 0\"></path>
                  <line x1=\"12\" y1=\"20\" x2=\"12.01\" y2=\"20\"></line>
                </svg>
                <h2 class=\"card-title\">Network Information</h2>
              </div>
              <button class=\"btn btn-secondary btn-sm\" id=\"btn-refresh-wifi\" title=\"Refresh WiFi Info\">Refresh</button>
            </div>
            
            <div class=\"info-table\">
              <div class=\"info-row\"><span class=\"info-key\">Wi-Fi Status</span><span class=\"info-val\" id=\"net-status\">--</span></div>
              <div class=\"info-row\"><span class=\"info-key\">SSID</span><span class=\"info-val text-accent\" id=\"net-ssid\">--</span></div>
              <div class=\"info-row\"><span class=\"info-key\">IP Address</span><span class=\"info-val\" id=\"net-ip\">--</span></div>
              <div class=\"info-row\"><span class=\"info-key\">Gateway IP</span><span class=\"info-val\" id=\"net-gateway\">--</span></div>
              <div class=\"info-row\"><span class=\"info-key\">Subnet Mask</span><span class=\"info-val\" id=\"net-subnet\">--</span></div>
              <div class=\"info-row\"><span class=\"info-key\">MAC Address</span><span class=\"info-val\" id=\"net-mac\">--</span></div>
              <div class=\"info-row\"><span class=\"info-key\">Wi-Fi RSSI</span><span class=\"info-val\" id=\"net-rssi\">--</span></div>
              <div class=\"info-row\"><span class=\"info-key\">Wi-Fi Channel</span><span class=\"info-val\" id=\"net-channel\">--</span></div>
              <div class=\"info-row\"><span class=\"info-key\">BSSID (AP MAC)</span><span class=\"info-val\" id=\"net-bssid\">--</span></div>
            </div>
          </section>

          <section class=\"card detail-card action-card\">
            <div class=\"card-header\">
              <div class=\"card-header-left\">
                <svg viewBox=\"0 0 24 24\" width=\"20\" height=\"20\" stroke=\"currentColor\" stroke-width=\"2\" fill=\"none\">
                  <circle cx=\"12\" cy=\"12\" r=\"3\"></circle>
                  <path d=\"M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z\"></path>
                </svg>
                <h2 class=\"card-title\">System Actions</h2>
              </div>
            </div>
            
            <p class=\"action-desc\">
              Trigger a software restart of the microcontroller. The web server will momentarily go offline and reconnect automatically.
            </p>

            <div class=\"action-btn-group\">
              <button id=\"btn-restart\" class=\"btn btn-danger\">RESTART ESP32</button>
            </div>
          </section>
        </div>
      </div>
    </main>

    <footer class=\"dashboard-footer\">
      <div>ESP32 Web Dashboard &bull; Lightweight Standalone Monitor</div>
      <div class=\"footer-sub\">Pure Vanilla JS / CSS &bull; Zero External CDN Dependencies</div>
    </footer>
  </div>

  <div id=\"modal-overlay\" class=\"modal-overlay hidden\">
    <div class=\"modal-card\">
      <div id=\"modal-confirm-view\">
        <h3 class=\"modal-title\">Restart Confirmation</h3>
        <p class=\"modal-text\">Are you sure you want to restart the ESP32 microcontroller?</p>
        <div class=\"modal-actions\">
          <button id=\"modal-cancel-btn\" class=\"btn btn-secondary\">Cancel</button>
          <button id=\"modal-proceed-btn\" class=\"btn btn-danger\">Yes, Restart Now</button>
        </div>
      </div>
      
      <div id=\"modal-progress-view\" class=\"hidden\">
        <div class=\"spinner\"></div>
        <h3 class=\"modal-title\">Restarting ESP32...</h3>
        <p class=\"modal-text\">Please wait while the device reboots and reconnects to Wi-Fi.</p>
        <div class=\"reboot-countdown\" id=\"reboot-countdown\">8s</div>
      </div>
    </div>
  </div>

  <script>
    const state = {{
      isOnline: false,
      lastSuccessfulUpdate: null,
      totalHeap: 320000,
      pollingInterval: 1000,
      isRebooting: false,
      currentTheme: localStorage.getItem('esp32_theme') || 'theme-1'
    }};

    const elements = {{
      connectionBadge: document.getElementById('connection-badge'),
      connectionText: document.getElementById('connection-text'),
      lastUpdatedText: document.getElementById('last-updated-text'),
      metricStatus: document.getElementById('metric-status'),
      metricStatusSub: document.getElementById('metric-status-sub'),
      metricUptime: document.getElementById('metric-uptime'),
      metricUptimeRaw: document.getElementById('metric-uptime-raw'),
      metricFreeHeap: document.getElementById('metric-free-heap'),
      heapProgressBar: document.getElementById('heap-progress-bar'),
      metricHeapPercentage: document.getElementById('metric-heap-percentage'),
      metricRssi: document.getElementById('metric-rssi'),
      rssiRatingBadge: document.getElementById('rssi-rating-badge'),
      signalBars: document.getElementById('signal-bars'),
      metricRssiSub: document.getElementById('metric-rssi-sub'),
      metricCpu: document.getElementById('metric-cpu'),
      metricCpuCores: document.getElementById('metric-cpu-cores'),
      metricIp: document.getElementById('metric-ip'),
      metricMac: document.getElementById('metric-mac'),
      sysChipModel: document.getElementById('sys-chip-model'),
      sysChipRev: document.getElementById('sys-chip-rev'),
      sysCpuCores: document.getElementById('sys-cpu-cores'),
      sysCpuFreq: document.getElementById('sys-cpu-freq'),
      sysTotalHeap: document.getElementById('sys-total-heap'),
      sysFreeHeap: document.getElementById('sys-free-heap'),
      sysMinHeap: document.getElementById('sys-min-heap'),
      sysMaxAlloc: document.getElementById('sys-max-alloc'),
      sysFlashSize: document.getElementById('sys-flash-size'),
      sysFlashSpeed: document.getElementById('sys-flash-speed'),
      sysSketchSize: document.getElementById('sys-sketch-size'),
      sysFreeSketch: document.getElementById('sys-free-sketch'),
      sysResetReason: document.getElementById('sys-reset-reason'),
      sysSdkVer: document.getElementById('sys-sdk-ver'),
      netStatus: document.getElementById('net-status'),
      netSsid: document.getElementById('net-ssid'),
      netIp: document.getElementById('net-ip'),
      netGateway: document.getElementById('net-gateway'),
      netSubnet: document.getElementById('net-subnet'),
      netMac: document.getElementById('net-mac'),
      netRssi: document.getElementById('net-rssi'),
      netChannel: document.getElementById('net-channel'),
      netBssid: document.getElementById('net-bssid'),
      btnRefreshSystem: document.getElementById('btn-refresh-system'),
      btnRefreshWifi: document.getElementById('btn-refresh-wifi'),
      btnRestart: document.getElementById('btn-restart'),
      btnSwitchBg: document.getElementById('btn-switch-bg'),
      bgToggleText: document.getElementById('bg-toggle-text'),
      modalOverlay: document.getElementById('modal-overlay'),
      modalConfirmView: document.getElementById('modal-confirm-view'),
      modalProgressView: document.getElementById('modal-progress-view'),
      modalCancelBtn: document.getElementById('modal-cancel-btn'),
      modalProceedBtn: document.getElementById('modal-proceed-btn'),
      rebootCountdown: document.getElementById('reboot-countdown')
    }};

    function applyTheme(themeName) {{
      state.currentTheme = themeName;
      document.body.className = themeName;
      localStorage.setItem('esp32_theme', themeName);
      elements.bgToggleText.textContent = themeName === 'theme-1' ? 'Close-up' : 'City Hood';
    }}

    function toggleTheme() {{
      const nextTheme = state.currentTheme === 'theme-1' ? 'theme-2' : 'theme-1';
      applyTheme(nextTheme);
    }}

    function formatUptime(seconds) {{
      if (seconds === undefined || seconds === null || isNaN(seconds)) return '--';
      const sec = Math.floor(seconds % 60);
      const min = Math.floor((seconds / 60) % 60);
      const hrs = Math.floor((seconds / 3600) % 24);
      const days = Math.floor(seconds / 86400);
      const pad = (n) => String(n).padStart(2, '0');
      if (days > 0) return `${{days}}d ${{pad(hrs)}}h ${{pad(min)}}m ${{pad(sec)}}s`;
      return `${{pad(hrs)}}h ${{pad(min)}}m ${{pad(sec)}}s`;
    }}

    function formatBytes(bytes, decimals = 1) {{
      if (bytes === undefined || bytes === null || isNaN(bytes)) return 'N/A';
      if (bytes === 0) return '0 B';
      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ['B', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }}

    function evaluateRssi(rssi) {{
      if (!rssi || isNaN(rssi)) return {{ label: 'Unknown', level: 0, class: 'text-muted' }};
      if (rssi >= -55) return {{ label: 'Excellent', level: 4, class: 'text-success' }};
      if (rssi >= -67) return {{ label: 'Good', level: 3, class: 'text-success' }};
      if (rssi >= -78) return {{ label: 'Fair', level: 2, class: 'text-warning' }};
      return {{ label: 'Weak', level: 1, class: 'text-danger' }};
    }}

    function setConnectionState(isOnline) {{
      state.isOnline = isOnline;
      if (isOnline) {{
        elements.connectionBadge.className = 'status-badge badge-online';
        elements.connectionText.textContent = 'ONLINE';
        elements.metricStatus.textContent = 'ONLINE';
        elements.metricStatus.className = 'metric-value text-success';
        elements.metricStatusSub.textContent = 'ESP32 responding';
      }} else {{
        elements.connectionBadge.className = 'status-badge badge-offline';
        elements.connectionText.textContent = 'OFFLINE';
        elements.metricStatus.textContent = 'OFFLINE';
        elements.metricStatus.className = 'metric-value text-danger';
        elements.metricStatusSub.textContent = 'Connection lost';
        elements.lastUpdatedText.textContent = 'Connection lost';
      }}
    }}

    function updateTimeAgo() {{
      if (!state.isOnline || !state.lastSuccessfulUpdate) return;
      const diffSec = Math.floor((Date.now() - state.lastSuccessfulUpdate) / 1000);
      elements.lastUpdatedText.textContent = diffSec <= 1 ? 'Last updated: just now' : `Last updated: ${{diffSec}}s ago`;
    }}

    function renderStatus(data) {{
      elements.metricUptime.textContent = formatUptime(data.uptime);
      elements.metricUptimeRaw.textContent = `Raw: ${{data.uptime || 0}}s`;
      const freeHeap = data.freeHeap || 0;
      const totalHeap = data.heapSize || state.totalHeap;
      state.totalHeap = totalHeap;
      elements.metricFreeHeap.textContent = formatBytes(freeHeap);
      const freePct = Math.min(100, Math.max(0, Math.round((freeHeap / totalHeap) * 100)));
      elements.heapProgressBar.style.width = `${{freePct}}%`;
      elements.metricHeapPercentage.textContent = `${{freePct}}% free of ${{formatBytes(totalHeap, 0)}}`;
      const rssi = data.wifiRSSI;
      const evalSignal = evaluateRssi(rssi);
      elements.metricRssi.textContent = `${{rssi}} dBm`;
      elements.rssiRatingBadge.textContent = evalSignal.label;
      elements.rssiRatingBadge.className = `badge-sub ${{evalSignal.class}}`;
      elements.signalBars.className = `signal-bars level-${{evalSignal.level}}`;
      elements.metricCpu.textContent = `${{data.cpuFrequency || 240}} MHz`;
      if (data.ip) elements.metricIp.textContent = data.ip;
    }}

    function renderSystem(data) {{
      elements.sysChipModel.textContent = data.chipModel || 'ESP32';
      elements.sysChipRev.textContent = `Rev ${{data.chipRevision ?? '0'}}`;
      elements.sysCpuCores.textContent = `${{data.cpuCores || 2}} Core(s)`;
      elements.sysCpuFreq.textContent = `${{data.cpuFrequency || 240}} MHz`;
      if (data.heapSize) {{
        state.totalHeap = data.heapSize;
        elements.sysTotalHeap.textContent = formatBytes(data.heapSize);
      }}
      elements.sysFreeHeap.textContent = formatBytes(data.freeHeap);
      elements.sysMinHeap.textContent = formatBytes(data.minFreeHeap);
      elements.sysMaxAlloc.textContent = formatBytes(data.maxAllocHeap);
      elements.sysFlashSize.textContent = formatBytes(data.flashSize, 0);
      elements.sysFlashSpeed.textContent = data.flashSpeed ? `${{(data.flashSpeed / 1000000).toFixed(0)}} MHz` : 'N/A';
      elements.sysSketchSize.textContent = formatBytes(data.sketchSize);
      elements.sysFreeSketch.textContent = formatBytes(data.freeSketchSpace);
      elements.sysResetReason.textContent = data.resetReason || 'Power-on';
      elements.sysSdkVer.textContent = data.sdkVersion || 'N/A';
    }}

    function renderWifi(data) {{
      elements.netStatus.textContent = data.status || 'Connected';
      elements.netSsid.textContent = data.ssid || 'N/A';
      elements.netIp.textContent = data.ip || 'N/A';
      elements.netGateway.textContent = data.gateway || 'N/A';
      elements.netSubnet.textContent = data.subnetMask || 'N/A';
      elements.netMac.textContent = data.mac || 'N/A';
      elements.metricMac.textContent = `MAC: ${{data.mac || '--:--:--:--:--:--'}}`;
      elements.netRssi.textContent = `${{data.rssi || 0}} dBm (${{evaluateRssi(data.rssi).label}})`;
      elements.netChannel.textContent = data.channel ? `Channel ${{data.channel}}` : 'N/A';
      elements.netBssid.textContent = data.bssid || 'N/A';
    }}

    async function fetchStatus() {{
      if (state.isRebooting) return;
      try {{
        const response = await fetch('/api/status');
        if (!response.ok) throw new Error();
        const data = await response.json();
        renderStatus(data);
        state.lastSuccessfulUpdate = Date.now();
        if (!state.isOnline) setConnectionState(true);
      }} catch (err) {{
        setConnectionState(false);
      }}
    }}

    async function fetchSystem() {{
      try {{
        const response = await fetch('/api/system');
        if (response.ok) renderSystem(await response.json());
      }} catch (e) {{}}
    }}

    async function fetchWifi() {{
      try {{
        const response = await fetch('/api/wifi');
        if (response.ok) renderWifi(await response.json());
      }} catch (e) {{}}
    }}

    async function triggerRestart() {{
      elements.modalConfirmView.classList.add('hidden');
      elements.modalProgressView.classList.remove('hidden');
      state.isRebooting = true;
      setConnectionState(false);

      try {{
        await fetch('/api/restart', {{ method: 'POST' }});
      }} catch (e) {{}}

      let secondsRemaining = 8;
      elements.rebootCountdown.textContent = `${{secondsRemaining}}s`;

      const countdownInterval = setInterval(() => {{
        secondsRemaining--;
        if (secondsRemaining > 0) {{
          elements.rebootCountdown.textContent = `${{secondsRemaining}}s`;
        }} else {{
          clearInterval(countdownInterval);
          elements.rebootCountdown.textContent = 'Connecting...';
          pollReconnection();
        }}
      }}, 1000);
    }}

    async function pollReconnection() {{
      const retryTimer = setInterval(async () => {{
        try {{
          const res = await fetch('/api/status');
          if (res.ok) {{
            clearInterval(retryTimer);
            state.isRebooting = false;
            elements.modalOverlay.classList.add('hidden');
            elements.modalProgressView.classList.add('hidden');
            elements.modalConfirmView.classList.remove('hidden');
            setConnectionState(true);
            fetchStatus(); fetchSystem(); fetchWifi();
          }}
        }} catch (e) {{}}
      }}, 1500);
    }}

    document.addEventListener('DOMContentLoaded', () => {{
      applyTheme(state.currentTheme);

      elements.btnSwitchBg.addEventListener('click', toggleTheme);
      elements.btnRefreshSystem.addEventListener('click', fetchSystem);
      elements.btnRefreshWifi.addEventListener('click', fetchWifi);
      elements.btnRestart.addEventListener('click', () => {{
        elements.modalConfirmView.classList.remove('hidden');
        elements.modalProgressView.classList.add('hidden');
        elements.modalOverlay.classList.remove('hidden');
      }});
      elements.modalCancelBtn.addEventListener('click', () => elements.modalOverlay.classList.add('hidden'));
      elements.modalProceedBtn.addEventListener('click', triggerRestart);
      elements.modalOverlay.addEventListener('click', (e) => {{
        if (e.target === elements.modalOverlay && !state.isRebooting) elements.modalOverlay.classList.add('hidden');
      }});

      fetchStatus();
      fetchSystem();
      fetchWifi();

      setInterval(fetchStatus, state.pollingInterval);
      setInterval(updateTimeAgo, 1000);
      setInterval(() => {{
        if (state.isOnline && !state.isRebooting) {{ fetchSystem(); fetchWifi(); }}
      }}, 10000);
    }});
  </script>
</body>
</html>)rawliteral\";

#endif // DASHBOARD_UI_H
"""

# Write to both root and ESP32-Web-Dashboard directory
paths = [
    r"C:\Kuliahhh\piranticerdas\esp32 web\dashboard_ui.h",
    r"C:\Kuliahhh\piranticerdas\esp32 web\ESP32-Web-Dashboard\dashboard_ui.h"
]

for p in paths:
    with open(p, "w", encoding="utf-8") as f:
        f.write(header_code)
    print(f"Written: {p}")

print("Done generating dashboard_ui.h with Mr. Robot backgrounds!")
