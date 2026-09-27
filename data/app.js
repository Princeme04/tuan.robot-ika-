/**
 * ESP32 Web Dashboard - Vanilla Frontend Logic
 * Handles real-time polling, DOM updates, status badges, and ESP32 restart flow.
 */

// Application State
const state = {
  isOnline: false,
  lastSuccessfulUpdate: null,
  totalHeap: 320000, // Dynamic, updated from system API
  pollingInterval: 1000,
  pollTimer: null,
  timeAgoTimer: null,
  isRebooting: false
};

// DOM Element References
const elements = {
  connectionBadge: document.getElementById('connection-badge'),
  connectionText: document.getElementById('connection-text'),
  lastUpdatedText: document.getElementById('last-updated-text'),
  
  // Metric Overview Cards
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

  // System Information Table
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

  // Network Information Table
  netStatus: document.getElementById('net-status'),
  netSsid: document.getElementById('net-ssid'),
  netIp: document.getElementById('net-ip'),
  netGateway: document.getElementById('net-gateway'),
  netSubnet: document.getElementById('net-subnet'),
  netMac: document.getElementById('net-mac'),
  netRssi: document.getElementById('net-rssi'),
  netChannel: document.getElementById('net-channel'),
  netBssid: document.getElementById('net-bssid'),

  // Buttons & Modals
  btnRefreshSystem: document.getElementById('btn-refresh-system'),
  btnRefreshWifi: document.getElementById('btn-refresh-wifi'),
  btnRestart: document.getElementById('btn-restart'),
  modalOverlay: document.getElementById('modal-overlay'),
  modalConfirmView: document.getElementById('modal-confirm-view'),
  modalProgressView: document.getElementById('modal-progress-view'),
  modalCancelBtn: document.getElementById('modal-cancel-btn'),
  modalProceedBtn: document.getElementById('modal-proceed-btn'),
  rebootCountdown: document.getElementById('reboot-countdown')
};

// ============================================================================
// Formatting Helpers
// ============================================================================

/**
 * Formats seconds into human-readable Uptime string (e.g. 2d 4h 21m 10s or 02h 31m 45s)
 */
function formatUptime(seconds) {
  if (seconds === undefined || seconds === null || isNaN(seconds)) return '--';
  
  const sec = Math.floor(seconds % 60);
  const min = Math.floor((seconds / 60) % 60);
  const hrs = Math.floor((seconds / 3600) % 24);
  const days = Math.floor(seconds / 86400);

  const pad = (n) => String(n).padStart(2, '0');

  if (days > 0) {
    return `${days}d ${pad(hrs)}h ${pad(min)}m ${pad(sec)}s`;
  }
  return `${pad(hrs)}h ${pad(min)}m ${pad(sec)}s`;
}

/**
 * Formats bytes into KB or MB with clean units
 */
function formatBytes(bytes, decimals = 1) {
  if (bytes === undefined || bytes === null || isNaN(bytes)) return 'N/A';
  if (bytes === 0) return '0 B';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

/**
 * Calculates Wi-Fi Signal Quality & Bar Level from RSSI dBm
 */
function evaluateRssi(rssi) {
  if (!rssi || isNaN(rssi)) return { label: 'Unknown', level: 0, class: 'text-muted' };
  
  if (rssi >= -55) {
    return { label: 'Excellent', level: 4, class: 'text-success' };
  } else if (rssi >= -67) {
    return { label: 'Good', level: 3, class: 'text-success' };
  } else if (rssi >= -78) {
    return { label: 'Fair', level: 2, class: 'text-warning' };
  } else {
    return { label: 'Weak', level: 1, class: 'text-danger' };
  }
}

// ============================================================================
// UI Update Functions
// ============================================================================

/**
 * Updates the global Online / Offline badge and UI status
 */
function setConnectionState(isOnline) {
  state.isOnline = isOnline;
  
  if (isOnline) {
    elements.connectionBadge.className = 'status-badge badge-online';
    elements.connectionText.textContent = 'ONLINE';
    elements.metricStatus.textContent = 'ONLINE';
    elements.metricStatus.className = 'metric-value text-success';
    elements.metricStatusSub.textContent = 'ESP32 responding';
  } else {
    elements.connectionBadge.className = 'status-badge badge-offline';
    elements.connectionText.textContent = 'OFFLINE';
    elements.metricStatus.textContent = 'OFFLINE';
    elements.metricStatus.className = 'metric-value text-danger';
    elements.metricStatusSub.textContent = 'Connection lost';
    elements.lastUpdatedText.textContent = 'Connection lost';
  }
}

/**
 * Updates the "Last updated X seconds ago" indicator
 */
function updateTimeAgo() {
  if (!state.isOnline || !state.lastSuccessfulUpdate) return;
  const diffSec = Math.floor((Date.now() - state.lastSuccessfulUpdate) / 1000);
  
  if (diffSec <= 1) {
    elements.lastUpdatedText.textContent = 'Last updated: just now';
  } else {
    elements.lastUpdatedText.textContent = `Last updated: ${diffSec}s ago`;
  }
}

/**
 * Renders live `/api/status` data into the overview cards
 */
function renderStatus(data) {
  // 1. Status & Uptime
  elements.metricUptime.textContent = formatUptime(data.uptime);
  elements.metricUptimeRaw.textContent = `Raw: ${data.uptime || 0}s`;

  // 2. Free Heap & Progress Bar
  const freeHeap = data.freeHeap || 0;
  const totalHeap = data.heapSize || state.totalHeap;
  state.totalHeap = totalHeap;
  
  elements.metricFreeHeap.textContent = formatBytes(freeHeap);
  const freePct = Math.min(100, Math.max(0, Math.round((freeHeap / totalHeap) * 100)));
  elements.heapProgressBar.style.width = `${freePct}%`;
  elements.metricHeapPercentage.textContent = `${freePct}% free of ${formatBytes(totalHeap, 0)}`;

  // 3. Wi-Fi Signal & RSSI
  const rssi = data.wifiRSSI;
  const evalSignal = evaluateRssi(rssi);
  elements.metricRssi.textContent = `${rssi} dBm`;
  elements.rssiRatingBadge.textContent = evalSignal.label;
  elements.rssiRatingBadge.className = `badge-sub ${evalSignal.class}`;
  
  // Set Wi-Fi level bars
  elements.signalBars.className = `signal-bars level-${evalSignal.level}`;

  // 4. CPU Frequency
  elements.metricCpu.textContent = `${data.cpuFrequency || 240} MHz`;

  // 5. IP Address
  if (data.ip) {
    elements.metricIp.textContent = data.ip;
  }
}

/**
 * Renders `/api/system` data into the System Information table
 */
function renderSystem(data) {
  elements.sysChipModel.textContent = data.chipModel || 'ESP32';
  elements.sysChipRev.textContent = `Rev ${data.chipRevision ?? '0'}`;
  elements.sysCpuCores.textContent = `${data.cpuCores || 2} Core(s)`;
  elements.sysCpuFreq.textContent = `${data.cpuFrequency || 240} MHz`;
  
  if (data.heapSize) {
    state.totalHeap = data.heapSize;
    elements.sysTotalHeap.textContent = formatBytes(data.heapSize);
  }
  elements.sysFreeHeap.textContent = formatBytes(data.freeHeap);
  elements.sysMinHeap.textContent = formatBytes(data.minFreeHeap);
  elements.sysMaxAlloc.textContent = formatBytes(data.maxAllocHeap);
  
  elements.sysFlashSize.textContent = formatBytes(data.flashSize, 0);
  elements.sysFlashSpeed.textContent = data.flashSpeed ? `${(data.flashSpeed / 1000000).toFixed(0)} MHz` : 'N/A';
  elements.sysSketchSize.textContent = formatBytes(data.sketchSize);
  elements.sysFreeSketch.textContent = formatBytes(data.freeSketchSpace);
  elements.sysResetReason.textContent = data.resetReason || 'Power-on / SW Reset';
  elements.sysSdkVer.textContent = data.sdkVersion || 'N/A';
}

/**
 * Renders `/api/wifi` data into the Network Information table
 */
function renderWifi(data) {
  elements.netStatus.textContent = data.status || 'Connected';
  elements.netSsid.textContent = data.ssid || 'N/A';
  elements.netIp.textContent = data.ip || 'N/A';
  elements.netGateway.textContent = data.gateway || 'N/A';
  elements.netSubnet.textContent = data.subnetMask || 'N/A';
  elements.netMac.textContent = data.mac || 'N/A';
  elements.metricMac.textContent = `MAC: ${data.mac || '--:--:--:--:--:--'}`;
  elements.netRssi.textContent = `${data.rssi || 0} dBm (${evaluateRssi(data.rssi).label})`;
  elements.netChannel.textContent = data.channel ? `Channel ${data.channel}` : 'N/A';
  elements.netBssid.textContent = data.bssid || 'N/A';
}

// ============================================================================
// API Fetching Methods
// ============================================================================

/**
 * Fetch `/api/status` periodically (every 1 second)
 */
async function fetchStatus() {
  if (state.isRebooting) return;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 2000);

  try {
    const response = await fetch('/api/status', {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);

    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    
    const data = await response.json();
    renderStatus(data);
    
    state.lastSuccessfulUpdate = Date.now();
    if (!state.isOnline) {
      setConnectionState(true);
    }
  } catch (err) {
    clearTimeout(timeoutId);
    setConnectionState(false);
  }
}

/**
 * Fetch full `/api/system` payload
 */
async function fetchSystem() {
  try {
    const response = await fetch('/api/system');
    if (response.ok) {
      const data = await response.json();
      renderSystem(data);
    }
  } catch (err) {
    console.error('Failed to fetch system info:', err);
  }
}

/**
 * Fetch full `/api/wifi` payload
 */
async function fetchWifi() {
  try {
    const response = await fetch('/api/wifi');
    if (response.ok) {
      const data = await response.json();
      renderWifi(data);
    }
  } catch (err) {
    console.error('Failed to fetch wifi info:', err);
  }
}

// ============================================================================
// Restart & Reconnection Workflow
// ============================================================================

/**
 * Triggers the restart flow via POST /api/restart
 */
async function triggerRestart() {
  elements.modalConfirmView.classList.add('hidden');
  elements.modalProgressView.classList.remove('hidden');
  state.isRebooting = true;
  setConnectionState(false);

  try {
    await fetch('/api/restart', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (err) {
    // A connection drop during restart is expected
  }

  // Start 10-second countdown before attempting reconnection
  let secondsRemaining = 8;
  elements.rebootCountdown.textContent = `${secondsRemaining}s`;

  const countdownInterval = setInterval(() => {
    secondsRemaining--;
    if (secondsRemaining > 0) {
      elements.rebootCountdown.textContent = `${secondsRemaining}s`;
    } else {
      clearInterval(countdownInterval);
      elements.rebootCountdown.textContent = 'Connecting...';
      pollReconnection();
    }
  }, 1000);
}

/**
 * Attempts to poll the ESP32 until it comes back online after a restart
 */
async function pollReconnection() {
  let attempts = 0;
  const maxAttempts = 30;

  const retryTimer = setInterval(async () => {
    attempts++;
    try {
      const response = await fetch('/api/status', { method: 'GET' });
      if (response.ok) {
        clearInterval(retryTimer);
        state.isRebooting = false;
        
        // Hide modal and refresh everything
        elements.modalOverlay.classList.add('hidden');
        elements.modalProgressView.classList.add('hidden');
        elements.modalConfirmView.classList.remove('hidden');

        setConnectionState(true);
        fetchStatus();
        fetchSystem();
        fetchWifi();
      }
    } catch (e) {
      if (attempts >= maxAttempts) {
        clearInterval(retryTimer);
        elements.rebootCountdown.textContent = 'Please refresh the page manually.';
      }
    }
  }, 1500);
}

// ============================================================================
// Event Listeners & Initialization
// ============================================================================

function initEventListeners() {
  // Refresh buttons
  elements.btnRefreshSystem.addEventListener('click', () => {
    fetchSystem();
  });

  elements.btnRefreshWifi.addEventListener('click', () => {
    fetchWifi();
  });

  // Modal controls
  elements.btnRestart.addEventListener('click', () => {
    elements.modalConfirmView.classList.remove('hidden');
    elements.modalProgressView.classList.add('hidden');
    elements.modalOverlay.classList.remove('hidden');
  });

  elements.modalCancelBtn.addEventListener('click', () => {
    elements.modalOverlay.classList.add('hidden');
  });

  elements.modalProceedBtn.addEventListener('click', () => {
    triggerRestart();
  });

  // Close modal when clicking outside
  elements.modalOverlay.addEventListener('click', (e) => {
    if (e.target === elements.modalOverlay && !state.isRebooting) {
      elements.modalOverlay.classList.add('hidden');
    }
  });
}

/**
 * Application Bootstrap
 */
function init() {
  initEventListeners();

  // Initial fetch of all endpoints
  fetchStatus();
  fetchSystem();
  fetchWifi();

  // Start live polling loop
  state.pollTimer = setInterval(fetchStatus, state.pollingInterval);
  state.timeAgoTimer = setInterval(updateTimeAgo, 1000);

  // Periodic slow refresh of system details (every 10s)
  setInterval(() => {
    if (state.isOnline && !state.isRebooting) {
      fetchSystem();
      fetchWifi();
    }
  }, 10000);
}

// Run when DOM is loaded
document.addEventListener('DOMContentLoaded', init);
