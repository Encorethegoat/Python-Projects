import os
import json
import uuid
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)
BASE_URL = "https://unitrack.social"
SESSIONS_FILE = "sessions_pool.json"

DEFAULT_TOKEN = "eyJhbGciOiJkaXIiLCJlbW1iOiJBMjU2Q0JDLUhTNTEyIiwia2lkaSIiTddBRm0wNUYtbVVuMkpoTi01dU1N1U5S1VyeUJudTV0Zk1CVU13UVk0Q3BHcVBtR3plTHo0MktkMDNUelpRRHpiVDVUU04UVpYbm9sOFVLLVJGCWcifQ..GGvM6ilanTat-T1P-CTOqA.N4D1S0fQe1kbAAfV8eH8dchydAJkdQNbKbD9W-XH9IxI05dB34Y6NIpMNJku_48-rWABf2GMOI_j1qYvNNsD1728vVNEEm7mxfe-timsDotC0tS8C6eJ7S1ihr_n-uwgyoBqbGUM3DzMD8xMng-Lfwc7RQg_j3M37wHnjDWBzUD12iDy-jUEaD111N-MwS8pMtWutEhtowX1eCCLT8htVsm9U72enjzqqWghIq5_3T3gymfJrL02n0Ly05qavAnir_EpzomSTpqFXOvA2BY3eJoJDk0LWkR_R8BMI9vAmQp9QDEBayMABWvYNpiJ2n-gxyI76uXVDX4Z7OccGqJvbf6DUV1zJir3Q2H1tcNF6ns.Ose1E-joxdD7Fm_KrArILiPOXoNAisHsf4mhXWuonU"

def load_pool():
    if os.path.exists(SESSIONS_FILE):
        try:
            with open(SESSIONS_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    initial = [{
        "id": "cluster_main",
        "label": "Soham Chaudhari // Alpha Node",
        "prn": "26013030053",
        "token": DEFAULT_TOKEN
    }]
    save_pool(initial)
    return initial

def save_pool(pool):
    with open(SESSIONS_FILE, "w") as f:
        json.dump(pool, f, indent=2)

def get_headers(token):
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": BASE_URL,
        "Referer": f"{BASE_URL}/attendance",
        "Cookie": f"__Secure-authjs.session-token={token}"
    }

def juno_login_get_token(username, password, provider="juno"):
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0.0.0 Safari/537.36",
        "Origin": BASE_URL,
        "Referer": f"{BASE_URL}/login"
    })
    csrf_res = s.get(f"{BASE_URL}/api/auth/csrf")
    csrf_token = csrf_res.json().get("csrfToken")

    payload = {
        "csrfToken": csrf_token,
        "username": username,
        "prn": username,
        "email": username,
        "password": password,
        "redirect": "false",
        "json": "true",
        "callbackUrl": f"{BASE_URL}/attendance"
    }
    s.post(f"{BASE_URL}/api/auth/callback/{provider}", data=payload)
    return s.cookies.get("__Secure-authjs.session-token") or s.cookies.get("authjs.session-token")

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS // UniTrack Quantum Controller</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/html5-qrcode"></script>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Space Grotesk', sans-serif;
            background-color: #030407;
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(16, 185, 129, 0.08) 0%, transparent 35%),
                radial-gradient(circle at 85% 80%, rgba(99, 102, 241, 0.08) 0%, transparent 35%),
                linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
            background-size: 100% 100%, 100% 100%, 32px 32px, 32px 32px;
        }
        .mono { font-family: 'JetBrains Mono', monospace; }
        .glass {
            background: rgba(11, 14, 20, 0.78);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.06);
        }
        .neon-border:hover {
            border-color: rgba(16, 185, 129, 0.4);
            box-shadow: 0 0 25px rgba(16, 185, 129, 0.12);
        }
        @keyframes scanBeam {
            0% { top: 6%; opacity: 0.8; }
            50% { top: 90%; opacity: 1; }
            100% { top: 6%; opacity: 0.8; }
        }
        .laser-line {
            position: absolute;
            left: 6%;
            right: 6%;
            height: 2px;
            background: linear-gradient(90deg, transparent, #00f5a0, #00d9f5, #00f5a0, transparent);
            box-shadow: 0 0 18px 3px rgba(0, 245, 160, 0.75);
            animation: scanBeam 2.2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
            pointer-events: none;
            z-index: 20;
        }
        #reader video {
            border-radius: 1rem;
            object-fit: cover;
            transition: transform 0.15s ease-out;
        }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #06080E; }
        ::-webkit-scrollbar-thumb { background: #1E2433; border-radius: 9999px; }
        ::-webkit-scrollbar-thumb:hover { background: #10B981; }
    </style>
</head>
<body class="text-slate-100 min-h-screen selection:bg-emerald-400 selection:text-black">

    <div class="max-w-7xl mx-auto p-4 md:p-6 space-y-6">
        
        <!-- Futuristic Top Command Bar -->
        <header class="glass rounded-2xl px-6 py-4 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
            <div class="flex items-center gap-4">
                <div class="relative w-12 h-12 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-cyan-500/20 border border-emerald-400/40 flex items-center justify-center shadow-lg shadow-emerald-500/10">
                    <span class="mono font-bold text-emerald-400 text-lg tracking-tighter">NX</span>
                    <span class="absolute -top-1 -right-1 w-3 h-3 bg-emerald-400 rounded-full animate-ping"></span>
                    <span class="absolute -top-1 -right-1 w-3 h-3 bg-emerald-400 rounded-full"></span>
                </div>
                <div>
                    <div class="flex flex-wrap items-center gap-2.5">
                        <h1 class="text-xl md:text-2xl font-bold tracking-tight text-white">UNITRACK <span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">// NEXUS OS</span></h1>
                        <span id="poolBadge" class="mono text-[10px] uppercase tracking-widest px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-semibold">INITIALIZING</span>
                    </div>
                    <p class="text-xs text-slate-400 mt-0.5 mono">MULTI-NODE ERP MATRIX • <span class="text-cyan-400">CTRL+V</span> SCREENSHOT INTERCEPT READY</p>
                </div>
            </div>

            <div class="flex flex-wrap items-center gap-2.5 w-full lg:w-auto">
                <!-- Dry Run / Test Mode Switch -->
                <label class="flex items-center gap-2 bg-white/[0.03] border border-white/10 px-3.5 py-2 rounded-xl text-xs cursor-pointer hover:border-amber-400/40 transition">
                    <input type="checkbox" id="testModeToggle" class="accent-amber-400 rounded">
                    <span class="mono text-[11px] text-amber-300 font-semibold">SIMULATION MODE</span>
                </label>

                <button onclick="openModal('mainAccountModal')" class="flex-1 sm:flex-none bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-slate-950 font-bold px-4 py-2.5 rounded-xl text-xs tracking-wide uppercase transition shadow-lg shadow-emerald-500/20">
                    + Add Main Account
                </button>

                <button onclick="loadAllAccounts()" class="bg-white/5 hover:bg-white/10 border border-white/10 text-slate-200 px-3.5 py-2.5 rounded-xl text-xs mono font-semibold transition">
                    ⟳ SYNC
                </button>
            </div>
        </header>

        <!-- Telemetry HUD Bar -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="glass rounded-2xl p-4 border-l-2 border-l-emerald-400 flex justify-between items-center">
                <div>
                    <p class="mono text-[10px] uppercase tracking-widest text-slate-400">Main Clusters</p>
                    <p id="statClusters" class="text-2xl font-bold text-white mono mt-1">0</p>
                </div>
                <span class="text-xs mono px-2 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">NODES</span>
            </div>
            <div class="glass rounded-2xl p-4 border-l-2 border-l-cyan-400 flex justify-between items-center">
                <div>
                    <p class="mono text-[10px] uppercase tracking-widest text-slate-400">Total Student Identities</p>
                    <p id="statTotalAccounts" class="text-2xl font-bold text-cyan-400 mono mt-1">0</p>
                </div>
                <span class="text-xs mono px-2 py-1 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">POOL</span>
            </div>
            <div class="glass rounded-2xl p-4 border-l-2 border-l-indigo-400 flex justify-between items-center">
                <div>
                    <p class="mono text-[10px] uppercase tracking-widest text-slate-400">Armed Targets</p>
                    <p id="statArmed" class="text-2xl font-bold text-indigo-400 mono mt-1">0</p>
                </div>
                <span class="text-xs mono px-2 py-1 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">LOCKED</span>
            </div>
            <div class="glass rounded-2xl p-4 border-l-2 border-l-amber-400 flex justify-between items-center">
                <div>
                    <p class="mono text-[10px] uppercase tracking-widest text-slate-400">Optical Sensor</p>
                    <p id="statScanner" class="text-sm font-bold text-amber-400 mono mt-2">STANDBY</p>
                </div>
                <span class="text-xs mono px-2 py-1 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">20 FPS</span>
            </div>
        </div>

        <!-- Main Tactical Grid -->
        <div class="grid lg:grid-cols-12 gap-6">
            
            <!-- Left Column (5 Cols): Optical QR HUD -->
            <div class="lg:col-span-5 space-y-5">
                <div class="glass rounded-2xl p-5 space-y-4">
                    <div class="flex justify-between items-center">
                        <div class="flex items-center gap-2.5">
                            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                            <h2 class="mono text-xs font-bold uppercase tracking-widest text-slate-200">Optical Target Acquisition</h2>
                        </div>
                        <label class="flex items-center gap-2 text-xs text-emerald-300 mono cursor-pointer bg-emerald-500/10 border border-emerald-500/30 px-3 py-1 rounded-full">
                            <input type="checkbox" id="autoFire" checked class="accent-emerald-400 rounded">
                            AUTO-EXECUTE
                        </label>
                    </div>

                    <!-- Camera Source Switcher -->
                    <div class="flex gap-2">
                        <select id="cameraSelect" onchange="switchCamera(this.value)" class="flex-1 bg-[#05070B] border border-white/10 rounded-xl px-3 py-2 text-xs mono text-slate-300 focus:outline-none focus:border-emerald-400">
                            <option value="">Scanning video feeds (Webcam / OBS)...</option>
                        </select>
                        <button id="camToggleBtn" onclick="toggleCamera()" class="bg-white/5 hover:bg-white/10 border border-white/10 px-4 py-2 rounded-xl text-xs mono font-semibold transition">
                            PAUSE
                        </button>
                    </div>

                    <!-- Cyber Reticle Viewport -->
                    <div class="relative w-full aspect-square max-h-[330px] mx-auto bg-[#040609] rounded-2xl overflow-hidden border border-white/10 flex items-center justify-center shadow-inner">
                        <div id="reader" class="w-full h-full"></div>
                        <div id="laserLine" class="laser-line"></div>
                        
                        <!-- Futuristic Reticle Overlay -->
                        <div class="absolute inset-5 pointer-events-none">
                            <div class="absolute top-0 left-0 w-7 h-7 border-t-2 border-l-2 border-emerald-400 rounded-tl-lg"></div>
                            <div class="absolute top-0 right-0 w-7 h-7 border-t-2 border-r-2 border-emerald-400 rounded-tr-lg"></div>
                            <div class="absolute bottom-0 left-0 w-7 h-7 border-b-2 border-l-2 border-emerald-400 rounded-bl-lg"></div>
                            <div class="absolute bottom-0 right-0 w-7 h-7 border-b-2 border-r-2 border-emerald-400 rounded-br-lg"></div>
                            <div class="absolute bottom-2 left-3 mono text-[9px] text-emerald-400/70 tracking-widest">TARGETING // JUNO-ERP</div>
                        </div>
                    </div>

                    <!-- Optical Zoom Control -->
                    <div class="bg-[#05070B] border border-white/10 px-4 py-2.5 rounded-xl flex items-center gap-3">
                        <span class="mono text-[11px] text-slate-400 uppercase shrink-0">Magnification</span>
                        <input id="zoomSlider" type="range" min="1" max="4" step="0.1" value="1" oninput="applyZoom(this.value)" class="w-full accent-emerald-400 cursor-pointer">
                        <span id="zoomValue" class="mono text-xs text-emerald-400 font-bold w-10 text-right">1.0x</span>
                    </div>

                    <!-- Screenshot Dropzone -->
                    <label class="block border border-dashed border-emerald-500/30 hover:border-emerald-400 bg-emerald-500/[0.02] hover:bg-emerald-500/[0.05] rounded-xl p-3.5 text-center cursor-pointer transition">
                        <input type="file" accept="image/*" onchange="scanImageFile(this.files[0])" class="hidden">
                        <p class="text-xs font-semibold text-emerald-300 mono">📥 DROP QR IMAGE OR PRESS [CTRL+V]</p>
                        <p class="text-[11px] text-slate-400 mt-0.5">Instant decode from WhatsApp / Discord / Snipping Tool</p>
                    </label>
                </div>
            </div>

            <!-- Right Column (7 Cols): Main Account Nodes + Execution Console -->
            <div class="lg:col-span-7 space-y-5">
                
                <!-- Main Account Clusters Matrix -->
                <div class="glass rounded-2xl p-5 space-y-4">
                    <div class="flex flex-wrap justify-between items-center gap-2 border-b border-white/10 pb-3">
                        <div>
                            <h2 class="mono text-xs font-bold uppercase tracking-widest text-slate-200">Main Account Nodes & Parked Proxies</h2>
                            <p class="text-xs text-slate-400 mt-0.5">Add, manage, or remove main accounts • Each main node supports 1 Primary + 3 Parked slots</p>
                        </div>
                        <div class="flex gap-2">
                            <button onclick="selectAll(true)" class="bg-white/5 hover:bg-white/10 border border-white/10 px-3 py-1.5 rounded-lg text-xs mono transition">ALL</button>
                            <button onclick="selectAll(false)" class="bg-white/5 hover:bg-white/10 border border-white/10 px-3 py-1.5 rounded-lg text-xs mono transition">NONE</button>
                            <button onclick="openModal('mainAccountModal')" class="bg-emerald-500/15 hover:bg-emerald-500/25 text-emerald-300 border border-emerald-500/30 px-3 py-1.5 rounded-lg text-xs mono font-semibold transition">+ NEW NODE</button>
                        </div>
                    </div>

                    <!-- Clusters List -->
                    <div id="clustersContainer" class="space-y-4 max-h-[400px] overflow-y-auto pr-1">
                        <p class="text-xs text-slate-500 mono">Loading account nodes...</p>
                    </div>
                </div>

                <!-- Quantum Execution Feed -->
                <div class="glass rounded-2xl p-5 space-y-4">
                    <div class="flex justify-between items-center">
                        <h2 class="mono text-xs font-bold uppercase tracking-widest text-slate-200">Payload Transmission Console</h2>
                        <span id="lastScanTimeBadge" class="mono text-[11px] text-cyan-400">READY FOR PAYLOAD</span>
                    </div>

                    <div class="flex flex-col sm:flex-row gap-2.5">
                        <input id="qrPayload" type="text" placeholder="Decoded QR payload or manual test string..."
                            class="flex-1 bg-[#05070B] border border-white/10 rounded-xl px-4 py-3 text-xs mono text-emerald-300 focus:outline-none focus:border-emerald-400">
                        <button id="fireBtn" onclick="fireAllSelected()" class="bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-slate-950 font-extrabold px-6 py-3 rounded-xl text-xs mono tracking-wider uppercase transition shadow-lg shadow-emerald-500/20 shrink-0">
                            ⚡ TRANSMIT MARK
                        </button>
                    </div>

                    <!-- Live Per-Node Telemetry Cards -->
                    <div id="visualResults" class="space-y-2 hidden"></div>

                    <!-- Raw Server Telemetry -->
                    <details class="bg-[#05070B] border border-white/10 rounded-xl px-4 py-2.5">
                        <summary class="text-[11px] mono text-slate-400 cursor-pointer select-none">RAW TELEMETRY LOG (/api/juno/mark)</summary>
                        <pre id="markResult" class="mt-2 text-[11px] mono text-emerald-300/90 overflow-x-auto max-h-48">Awaiting execution...</pre>
                    </details>
                </div>

            </div>
        </div>
    </div>

    <!-- MODAL 1: Add / Manage Main Account Node -->
    <div id="mainAccountModal" class="fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
        <div class="glass rounded-2xl max-w-lg w-full p-6 space-y-5 border border-emerald-500/30">
            <div class="flex justify-between items-center border-b border-white/10 pb-3">
                <div>
                    <h3 class="text-base font-bold text-white mono uppercase tracking-wide">Deploy New Main Account Node</h3>
                    <p class="text-xs text-slate-400">Each main account acts as an independent cluster (1 Primary + 3 Parked)</p>
                </div>
                <button onclick="closeModal('mainAccountModal')" class="text-slate-400 hover:text-white text-sm mono">✕</button>
            </div>

            <!-- Method A: Direct PRN + ERP Password Login -->
            <div class="space-y-3">
                <p class="mono text-[11px] uppercase tracking-wider text-emerald-400 font-bold">// Method A: Direct ERP Authentication</p>
                <input id="mainPrn" type="text" placeholder="Main Account PRN (e.g. 26013030053)" class="w-full bg-[#05070B] border border-white/10 rounded-xl px-3.5 py-2.5 text-xs mono focus:outline-none focus:border-emerald-400">
                <input id="mainPass" type="password" placeholder="DYPIU ERP Password" class="w-full bg-[#05070B] border border-white/10 rounded-xl px-3.5 py-2.5 text-xs mono focus:outline-none focus:border-emerald-400">
                <input id="mainLabel" type="text" placeholder="Cluster Alias (e.g. Soham Main / Node 2)" class="w-full bg-[#05070B] border border-white/10 rounded-xl px-3.5 py-2.5 text-xs focus:outline-none focus:border-emerald-400">
                <button onclick="addIndependentSession()" class="w-full bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-slate-950 py-2.5 rounded-xl text-xs font-extrabold mono uppercase tracking-wider transition">
                    🚀 Authenticate & Add Main Node
                </button>
            </div>

            <!-- Method B: Raw Session Token Injection -->
            <div class="border-t border-white/10 pt-4 space-y-3">
                <p class="mono text-[11px] uppercase tracking-wider text-cyan-400 font-bold">// Method B: Inject Session Cookie (__Secure-authjs.session-token)</p>
                <input id="rawTokenLabel" type="text" placeholder="Cluster Label (e.g. Backup Main Account)" class="w-full bg-[#05070B] border border-white/10 rounded-xl px-3.5 py-2.5 text-xs">
                <input id="rawTokenValue" type="password" placeholder="Paste __Secure-authjs.session-token value..." class="w-full bg-[#05070B] border border-white/10 rounded-xl px-3.5 py-2.5 text-xs mono">
                <button onclick="addRawTokenSession()" class="w-full bg-white/10 hover:bg-white/15 border border-white/15 text-white py-2.5 rounded-xl text-xs font-bold mono uppercase tracking-wider transition">
                    ⚡ Inject Token Node
                </button>
            </div>

            <p id="addMainStatus" class="text-xs mono hidden"></p>
        </div>
    </div>

    <!-- MODAL 2: Park Proxy Student Inside a Specific Main Account -->
    <div id="parkModal" class="fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
        <div class="glass rounded-2xl max-w-md w-full p-6 space-y-4 border border-cyan-500/30">
            <div class="flex justify-between items-center border-b border-white/10 pb-3">
                <div>
                    <h3 class="text-sm font-bold text-white mono uppercase">Park Proxy Account in Node</h3>
                    <p id="parkTargetTitle" class="text-xs text-cyan-400 mono mt-0.5"></p>
                </div>
                <button onclick="closeModal('parkModal')" class="text-slate-400 hover:text-white text-sm mono">✕</button>
            </div>
            <input type="hidden" id="parkSessionId">
            <input id="parkPrn" type="text" placeholder="Friend's Roll No / PRN (26013...)" class="w-full bg-[#05070B] border border-white/10 rounded-xl px-3.5 py-2.5 text-xs mono">
            <input id="parkPass" type="password" placeholder="Friend's ERP Password" class="w-full bg-[#05070B] border border-white/10 rounded-xl px-3.5 py-2.5 text-xs mono">
            <input id="parkLabel" type="text" placeholder="Friend's Name / Label" class="w-full bg-[#05070B] border border-white/10 rounded-xl px-3.5 py-2.5 text-xs">
            <button onclick="submitParkAccount()" class="w-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-extrabold py-2.5 rounded-xl text-xs mono uppercase transition">
                🅿️ Park Student in This Cluster
            </button>
            <p id="parkStatus" class="text-xs mono hidden"></p>
        </div>
    </div>

    <script>
        let html5QrCode = null;
        let isScanning = false;
        let lastScannedCode = "";
        let lastScanTime = 0;

        function playBeep(success = true) {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.type = "triangle";
                osc.frequency.setValueAtTime(success ? 960 : 260, ctx.currentTime);
                gain.gain.setValueAtTime(0.15, ctx.currentTime);
                osc.start();
                osc.stop(ctx.currentTime + 0.14);
            } catch (e) {}
        }

        function openModal(id) { document.getElementById(id).classList.remove('hidden'); }
        function closeModal(id) { document.getElementById(id).classList.add('hidden'); }

        function openParkModal(sessionId, clusterLabel) {
            document.getElementById('parkSessionId').value = sessionId;
            document.getElementById('parkTargetTitle').textContent = `Target Node: ${clusterLabel}`;
            document.getElementById('parkStatus').classList.add('hidden');
            openModal('parkModal');
        }

        function applyZoom(val) {
            document.getElementById('zoomValue').textContent = parseFloat(val).toFixed(1) + 'x';
            const video = document.querySelector('#reader video');
            if (video) video.style.transform = `scale(${val})`;
        }

        async function initScanner() {
            html5QrCode = new Html5Qrcode("reader");
            try {
                const devices = await Html5Qrcode.getCameras();
                const select = document.getElementById('cameraSelect');
                select.innerHTML = '';
                if (devices && devices.length) {
                    devices.forEach((d, i) => {
                        const opt = document.createElement('option');
                        opt.value = d.id;
                        opt.textContent = d.label || `Optical Feed ${i + 1}`;
                        select.appendChild(opt);
                    });
                    startCamera(devices[0].id);
                } else {
                    document.getElementById('statScanner').textContent = "NO FEED";
                }
            } catch (err) {
                document.getElementById('statScanner').textContent = "LOCKED";
            }
        }

        async function startCamera(cameraId) {
            if (!html5QrCode) return;
            try {
                if (isScanning) await html5QrCode.stop();
                await html5QrCode.start(
                    cameraId,
                    { fps: 20, qrbox: { width: 230, height: 230 } },
                    onScanSuccess
                );
                isScanning = true;
                document.getElementById('statScanner').textContent = "ONLINE";
                document.getElementById('statScanner').className = "text-sm font-bold text-emerald-400 mono mt-2";
                document.getElementById('camToggleBtn').textContent = "PAUSE";
                document.getElementById('laserLine').style.display = "block";
            } catch (err) {
                console.error(err);
            }
        }

        async function switchCamera(cameraId) {
            if (cameraId) await startCamera(cameraId);
        }

        async function toggleCamera() {
            if (!html5QrCode) return;
            if (isScanning) {
                await html5QrCode.stop();
                isScanning = false;
                document.getElementById('statScanner').textContent = "PAUSED";
                document.getElementById('statScanner').className = "text-sm font-bold text-amber-400 mono mt-2";
                document.getElementById('camToggleBtn').textContent = "RESUME";
                document.getElementById('laserLine').style.display = "none";
            } else {
                const camId = document.getElementById('cameraSelect').value;
                if (camId) await startCamera(camId);
            }
        }

        async function loadAllAccounts() {
            const container = document.getElementById('clustersContainer');
            const res = await fetch('/api/pool/status');
            const clusters = await res.json();

            document.getElementById('statClusters').textContent = clusters.length;
            document.getElementById('poolBadge').textContent = `${clusters.length} MAIN NODE(S) ACTIVE`;
            container.innerHTML = '';

            if (clusters.length === 0) {
                container.innerHTML = `
                    <div class="text-center py-10 border border-dashed border-white/10 rounded-2xl">
                        <p class="mono text-xs text-slate-400">No Main Account Nodes configured.</p>
                        <button onclick="openModal('mainAccountModal')" class="mt-3 bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-4 py-2 rounded-xl text-xs mono font-bold">+ Deploy First Main Account</button>
                    </div>
                `;
                document.getElementById('statTotalAccounts').textContent = 0;
                updateSelectedCount();
                return;
            }

            let totalAcc = 0;

            clusters.forEach((c, idx) => {
                const credits = c.proxyStatus?.proxyCredits ?? '?';
                const section = c.proxyStatus?.section ?? 'DYPIU';
                const isOnline = c.accounts && c.accounts.length > 0;

                let cardsHtml = '';
                c.accounts.forEach(acc => {
                    totalAcc++;
                    cardsHtml += `
                        <label class="flex items-center justify-between bg-[#05070B] border border-white/10 px-3.5 py-2.5 rounded-xl cursor-pointer neon-border transition">
                            <div class="flex items-center gap-3">
                                <input type="checkbox" data-session-id="${c.id}" value="${acc.username}" ${acc.usable ? 'checked' : ''} onchange="updateSelectedCount()" class="pool-cb w-4 h-4 accent-emerald-400 rounded">
                                <div>
                                    <div class="flex items-center gap-2">
                                        <p class="text-xs font-bold text-white">${acc.label || acc.username}</p>
                                        ${acc.isPrimary 
                                            ? '<span class="mono text-[9px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-1.5 py-0.5 rounded">MAIN</span>' 
                                            : '<span class="mono text-[9px] bg-cyan-500/15 text-cyan-300 border border-cyan-500/20 px-1.5 py-0.5 rounded">PROXY</span>'}
                                    </div>
                                    <p class="text-[11px] text-slate-400 mono mt-0.5">PRN: ${acc.username}</p>
                                </div>
                            </div>
                            <span id="status-${c.id}-${acc.username}" class="mono text-[10px] px-2 py-0.5 rounded-full font-semibold ${acc.usable ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-400'}">
                                ${acc.usable ? 'ARMED' : 'OFF'}
                            </span>
                        </label>
                    `;
                });

                if (!isOnline) {
                    cardsHtml = `<p class="text-xs text-rose-400 mono col-span-2 py-2">⚠ Session token expired or invalid. Remove node or re-authenticate.</p>`;
                }

                const box = document.createElement('div');
                box.className = 'bg-white/[0.02] border border-white/10 rounded-2xl p-4 space-y-3 transition hover:border-white/20';
                box.innerHTML = `
                    <div class="flex flex-wrap justify-between items-center gap-2 border-b border-white/10 pb-2.5">
                        <div class="flex items-center gap-2.5">
                            <span class="w-2 h-2 rounded-full ${isOnline ? 'bg-emerald-400' : 'bg-rose-500'}"></span>
                            <span class="mono text-xs font-bold text-white">${c.label}</span>
                            <span class="mono text-[10px] text-slate-400 bg-white/5 px-2 py-0.5 rounded">${section}</span>
                            <span class="mono text-[10px] text-amber-300 bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded">CREDITS: ${credits}</span>
                        </div>
                        <div class="flex items-center gap-1.5">
                            <button onclick="openParkModal('${c.id}', '${c.label.replace(/'/g, "")}')" class="bg-cyan-500/15 hover:bg-cyan-500/25 text-cyan-300 border border-cyan-500/30 px-2.5 py-1 rounded-lg text-[10px] mono font-bold transition">
                                + PARK PROXY
                            </button>
                            <button onclick="removeMainCluster('${c.id}', '${c.label.replace(/'/g, "")}')" class="bg-rose-500/15 hover:bg-rose-500/30 text-rose-300 border border-rose-500/30 px-2.5 py-1 rounded-lg text-[10px] mono font-bold transition" title="Remove this Main Account Cluster">
                                ✕ REMOVE MAIN
                            </button>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">${cardsHtml}</div>
                `;
                container.appendChild(box);
            });

            document.getElementById('statTotalAccounts').textContent = totalAcc;
            updateSelectedCount();
        }

        async function removeMainCluster(sessionId, label) {
            if (!confirm(`Remove Main Account Cluster "${label}" and its parked list from NEXUS?`)) return;
            await fetch(`/api/pool/remove/${sessionId}`, { method: 'DELETE' });
            loadAllAccounts();
        }

        function selectAll(state) {
            document.querySelectorAll('.pool-cb').forEach(cb => cb.checked = state);
            updateSelectedCount();
        }

        function updateSelectedCount() {
            const count = document.querySelectorAll('.pool-cb:checked').length;
            document.getElementById('statArmed').textContent = count;
        }

        async function fireAllSelected(customQr) {
            const scanned = customQr || document.getElementById('qrPayload').value.trim();
            if (!scanned) return alert("Scan a QR code or enter a payload string first!");

            const grouped = {};
            const selectedTargets = [];
            document.querySelectorAll('.pool-cb:checked').forEach(cb => {
                const sid = cb.getAttribute('data-session-id');
                if (!grouped[sid]) grouped[sid] = [];
                grouped[sid].push(cb.value);
                selectedTargets.push({ sid, prn: cb.value });

                const badge = document.getElementById(`status-${sid}-${cb.value}`);
                if (badge) {
                    badge.textContent = "SENDING";
                    badge.className = "mono text-[10px] px-2 py-0.5 rounded-full font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30 animate-pulse";
                }
            });

            if (selectedTargets.length === 0) return alert("Select at least one student target!");

            // Check if Simulation Mode is enabled
            if (document.getElementById('testModeToggle').checked) {
                playBeep(true);
                const visualBox = document.getElementById('visualResults');
                visualBox.innerHTML = `<div class="p-3 rounded-xl border border-amber-400/40 bg-amber-500/10 text-amber-300 text-xs mono">[SIMULATION MODE] Decoded QR "${scanned.slice(0, 40)}..." for ${selectedTargets.length} student(s). Server was NOT contacted.</div>`;
                visualBox.classList.remove('hidden');
                selectedTargets.forEach(t => {
                    const badge = document.getElementById(`status-${t.sid}-${t.prn}`);
                    if (badge) {
                        badge.textContent = "SIM OK ✓";
                        badge.className = "mono text-[10px] px-2 py-0.5 rounded-full font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40";
                    }
                });
                return;
            }

            const fireBtn = document.getElementById('fireBtn');
            fireBtn.disabled = true;
            fireBtn.textContent = "⏳ TRANSMITTING...";
            document.getElementById('lastScanTimeBadge').textContent = `TX @ ${new Date().toLocaleTimeString()}`;

            try {
                const res = await fetch('/api/pool/mark-all', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ scanned, targets: grouped })
                });
                const data = await res.json();
                document.getElementById('markResult').textContent = JSON.stringify(data, null, 2);

                const visualBox = document.getElementById('visualResults');
                visualBox.innerHTML = '';
                visualBox.classList.remove('hidden');

                (data.parallel_results || []).forEach(bucketRes => {
                    const ok = bucketRes.status === 200 && (!bucketRes.data || bucketRes.data.error === undefined);
                    const summary = document.createElement('div');
                    summary.className = `p-3 rounded-xl border text-xs mono flex justify-between items-center ${ok ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' : 'bg-rose-500/10 border-rose-500/30 text-rose-300'}`;
                    summary.innerHTML = `
                        <span><strong>${bucketRes.bucket}</strong>: ${bucketRes.data?.message || (ok ? 'Batch Mark Confirmed' : (bucketRes.data?.error || 'Check Raw Telemetry'))}</span>
                        <span class="font-bold">HTTP ${bucketRes.status}</span>
                    `;
                    visualBox.appendChild(summary);
                });

                selectedTargets.forEach(t => {
                    const badge = document.getElementById(`status-${t.sid}-${t.prn}`);
                    if (badge) {
                        badge.textContent = "MARKED ✓";
                        badge.className = "mono text-[10px] px-2 py-0.5 rounded-full font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40";
                    }
                });
                playBeep(true);
            } catch (err) {
                playBeep(false);
                document.getElementById('markResult').textContent = "Transmission Error: " + err;
            } finally {
                fireBtn.disabled = false;
                fireBtn.textContent = "⚡ TRANSMIT MARK";
            }
        }

        function onScanSuccess(decodedText) {
            const now = Date.now();
            if (decodedText === lastScannedCode && (now - lastScanTime) < 8000) return;
            lastScannedCode = decodedText;
            lastScanTime = now;

            playBeep(true);
            document.getElementById('qrPayload').value = decodedText;
            if (document.getElementById('autoFire').checked) {
                fireAllSelected(decodedText);
            }
        }

        async function scanImageFile(imageFile) {
            if (!imageFile) return;
            const tempScanner = new Html5Qrcode("reader");
            try {
                const decodedText = await tempScanner.scanFile(imageFile, false);
                onScanSuccess(decodedText);
            } catch (err) {
                playBeep(false);
                alert("No clear QR code detected in image.");
            }
        }

        async function addIndependentSession() {
            const username = document.getElementById('mainPrn').value.trim();
            const password = document.getElementById('mainPass').value.trim();
            const label = document.getElementById('mainLabel').value.trim() || `Node // ${username}`;
            const status = document.getElementById('addMainStatus');

            if (!username || !password) return alert("Enter Main PRN and ERP Password!");
            status.classList.remove('hidden');
            status.className = "text-xs mono text-amber-400";
            status.textContent = "Authenticating Main Node via /api/auth/callback/juno...";

            const res = await fetch('/api/pool/add-session', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password, label })
            });
            const data = await res.json();
            if (res.ok && data.success) {
                status.className = "text-xs mono text-emerald-400";
                status.textContent = "Main Account Node deployed!";
                document.getElementById('mainPrn').value = '';
                document.getElementById('mainPass').value = '';
                document.getElementById('mainLabel').value = '';
                loadAllAccounts();
                setTimeout(() => closeModal('mainAccountModal'), 600);
            } else {
                status.className = "text-xs mono text-rose-400";
                status.textContent = data.error || "Login failed. Use Method B (Token Injection) instead.";
            }
        }

        async function addRawTokenSession() {
            const label = document.getElementById('rawTokenLabel').value.trim() || "Custom Main Node";
            const token = document.getElementById('rawTokenValue').value.trim();
            if (!token) return alert("Paste a __Secure-authjs.session-token value first!");

            await fetch('/api/pool/add-token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ label, token })
            });
            document.getElementById('rawTokenValue').value = '';
            document.getElementById('rawTokenLabel').value = '';
            closeModal('mainAccountModal');
            loadAllAccounts();
        }

        async function submitParkAccount() {
            const sessionId = document.getElementById('parkSessionId').value;
            const username = document.getElementById('parkPrn').value.trim();
            const password = document.getElementById('parkPass').value.trim();
            const label = document.getElementById('parkLabel').value.trim() || username;
            const status = document.getElementById('parkStatus');

            if (!username || !password) return alert("Enter Friend's PRN and ERP Password!");
            status.classList.remove('hidden');
            status.className = "text-xs mono text-amber-400";
            status.textContent = "Parking student into node...";

            const res = await fetch('/api/pool/park', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sessionId, username, password, label })
            });
            const data = await res.json();
            if (res.ok) {
                status.className = "text-xs mono text-emerald-400";
                status.textContent = "Parked successfully!";
                document.getElementById('parkPrn').value = '';
                document.getElementById('parkPass').value = '';
                document.getElementById('parkLabel').value = '';
                loadAllAccounts();
                setTimeout(() => closeModal('parkModal'), 600);
            } else {
                status.className = "text-xs mono text-rose-400";
                status.textContent = data.error || "Failed to park (Node may already have 3 parked accounts).";
            }
        }

        window.addEventListener('paste', (e) => {
            const items = (e.clipboardData || e.originalEvent.clipboardData).items;
            for (const item of items) {
                if (item.type.indexOf('image') === 0) {
                    scanImageFile(item.getAsFile());
                }
            }
        });

        window.addEventListener('DOMContentLoaded', () => {
            loadAllAccounts();
            initScanner();
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/api/pool/status")
def pool_status():
    pool = load_pool()
    results = []
    for entry in pool:
        headers = get_headers(entry["token"])
        try:
            acc_res = requests.get(f"{BASE_URL}/api/accounts", headers=headers, timeout=10)
            proxy_res = requests.get(f"{BASE_URL}/api/accounts/proxy-status", headers=headers, timeout=10)
        except Exception:
            acc_res = None
            proxy_res = None

        accounts_list = []
        if acc_res and acc_res.ok:
            data = acc_res.json()
            if data.get("active"):
                act = data["active"]
                accounts_list.append({
                    "username": act.get("username"),
                    "label": act.get("name") or act.get("username"),
                    "usable": True,
                    "isPrimary": True
                })
            for parked in data.get("accounts", []):
                if parked.get("username") != data.get("active", {}).get("username"):
                    accounts_list.append({
                        "username": parked.get("username"),
                        "label": parked.get("label") or parked.get("username"),
                        "usable": parked.get("usable", True),
                        "isPrimary": False
                    })

        results.append({
            "id": entry["id"],
            "label": entry["label"],
            "accounts": accounts_list,
            "proxyStatus": proxy_res.json() if (proxy_res and proxy_res.ok) else {}
        })
    return jsonify(results)

@app.route("/api/pool/remove/<session_id>", methods=["DELETE"])
def remove_session(session_id):
    pool = load_pool()
    updated = [p for p in pool if p["id"] != session_id]
    save_pool(updated)
    return jsonify({"success": True, "remaining": len(updated)})

@app.route("/api/pool/mark-all", methods=["POST"])
def mark_all():
    body = request.get_json()
    scanned = body.get("scanned")
    targets = body.get("targets", {})
    pool = {p["id"]: p for p in load_pool()}

    def fire_bucket(sid, usernames):
        token = pool[sid]["token"]
        r = requests.post(
            f"{BASE_URL}/api/juno/mark",
            headers=get_headers(token),
            json={"scanned": scanned, "enabledUsernames": usernames},
            timeout=45
        )
        try:
            return {"bucket": pool[sid]["label"], "status": r.status_code, "data": r.json()}
        except Exception:
            return {"bucket": pool[sid]["label"], "status": r.status_code, "raw": r.text}

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fire_bucket, sid, ulist) for sid, ulist in targets.items() if sid in pool]
        results = [f.result() for f in futures]

    return jsonify({"parallel_results": results})

@app.route("/api/pool/add-session", methods=["POST"])
def add_session():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    label = data.get("label", username).strip()

    token = juno_login_get_token(username, password, "juno")
    if not token:
        token = juno_login_get_token(username, password, "credentials")

    if token:
        pool = load_pool()
        pool.append({
            "id": f"node_{uuid.uuid4().hex[:6]}",
            "label": label,
            "prn": username,
            "token": token
        })
        save_pool(pool)
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Direct login failed — check password or inject session token."}), 400

@app.route("/api/pool/add-token", methods=["POST"])
def add_token():
    data = request.get_json()
    pool = load_pool()
    pool.append({
        "id": f"node_{uuid.uuid4().hex[:6]}",
        "label": data.get("label", "Custom Node"),
        "prn": "custom",
        "token": data.get("token", "").strip()
    })
    save_pool(pool)
    return jsonify({"success": True})

@app.route("/api/pool/park", methods=["POST"])
def park_account():
    data = request.get_json()
    session_id = data.get("sessionId")
    pool = load_pool()
    target = next((p for p in pool if p["id"] == session_id), pool[0] if pool else None)
    if not target:
        return jsonify({"error": "No target main account found"}), 400

    payload = {
        "username": data.get("username"),
        "password": data.get("password"),
        "label": data.get("label")
    }
    r = requests.post(f"{BASE_URL}/api/accounts", headers=get_headers(target["token"]), json=payload)
    return jsonify(r.json() if r.content else {}), r.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)