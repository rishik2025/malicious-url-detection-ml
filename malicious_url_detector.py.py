import tkinter as tk
from tkinter import filedialog, Scrollbar, Text, ttk
import webbrowser
import re
import smtplib
from email.message import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph
import tempfile
import os
from datetime import datetime
import requests
import threading
import math
import base64
import time

# =========================
# QR FEATURE IMPORTS
# =========================
import cv2
try:
    from pyzbar.pyzbar import decode as zbar_decode
    PYZBAR_AVAILABLE = True
except Exception:
    PYZBAR_AVAILABLE = False


# =========================
# ✅ SECRETS (USE YOUR OWN)
# =========================
# NOTE: For safety, DO NOT hardcode real keys/passwords in code you share.
VIRUSTOTAL_API_KEY = "12c31c6e53af5fec77612cc20729939efefd352bf1be3f53e1a5b9ecc21b5f13"   # <-- CHANGE
GMAIL_SENDER = "sanjai2004tn@gmail.com"                     # <-- CHANGE (optional)
GMAIL_APP_PASSWORD = "fjgb tqxa buho ipyf"            # <-- CHANGE (optional)

# =========================
# ✅ INFO BUTTON PATH
# =========================
INFO_HTML_PATH = r"C:\my project\INFO\INFO.html"        # <-- CHANGE if needed


# =========================
# ✅ SECURITY VENDORS LIST (ORDERED)
# =========================
SECURITY_VENDORS_ORDER = [
    "Cyble",
    "Abusix",
    "Acronis",
    "ADMINUSLabs",
    "AILabs (MONITORAPP)",
    "AlienVault",
    "alphaMountain.ai",
    "Antiy-AVL",
    "benkow.cc",
    "Bfore.Ai PreCrime",
    "BitDefender",
    "BlockList",
    "Blueliv",
    "Certego",
    "Chong Lua Dao",
    "CINS Army",
    "CMC Threat Intelligence",
    "CRDF",
    "Criminal IP",
    "CyRadar",
    "desenmascara.me",
    "DNS8",
    "Dr.Web",
    "EmergingThreats",
    "Emsisoft",
    "ESET",
    "ESTsecurity",
    "Forcepoint ThreatSeeker",
    "Fortinet",
    "G-Data",
    "Google Safebrowsing",
    "GreenSnow",
    "Heimdal Security",
    "IPsum",
    "Juniper Networks",
    "Kaspersky",
    "Lionic",
    "Malwared",
    "MalwarePatrol",
    "malwares.com URL checker",
    "OpenPhish",
    "Phishing Database",
    "Phishtank",
    "PREBYTES",
    "Quick Heal",
    "Quttera",
    "Rising",
    "Sangfor",
    "Scantitan",
    "SCUMWARE.org",
    "Seclookup",
    "securolytics",
    "Snort IP sample list",
    "SOCRadar",
    "Sophos",
    "Spam404",
    "StopForumSpam",
    "Sucuri SiteCheck",
    "ThreatHive",
    "Trustwave",
    "URLhaus",
    "URLQuery",
    "Viettel Threat Intelligence",
    "ViriBack",
    "VX Vault",
    "Webroot",
    "Xcitium Verdict Cloud",
    "Yandex Safebrowsing",
    "ZeroCERT",
    "0xSI_f33d",
    "AlphaSOC",
    "ArcSight Threat Intelligence",
    "AutoShun",
    "Bkav",
    "ChainPatrol",
    "Cluster25",
    "CSIS Security Group",
    "Cyan",
    "Ermes",
    "GCP Abuse Intelligence",
    "GreyNoise",
    "Gridinsoft",
    "Hunt.io Intelligence",
    "Lumu",
    "MalwareURL",
    "Mimecast",
    "Netcraft",
    "PhishFort",
    "PhishLabs",
    "PrecisionSec",
    "SafeToOpen",
    "Sansec eComscan",
    "VIPRE",
    "ZeroFox",
]

# =========================
# ✅ UNIQUE HTML TEMPLATES
# =========================

SAFE_HTML_TEMPLATE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Scan Report • SAFE</title>
<style>
:root{
  --bg1:#061016;
  --bg2:#071b13;
  --card:#0b1723cc;
  --line:#19364a;
  --good:#22c55e;
  --good2:#34d399;
  --text:#e5e7eb;
  --muted:#9ca3af;
}
*{box-sizing:border-box}
html,body{height:100%;margin:0;font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Arial}
body{
  color:var(--text);

  /* ✅ CHANGED: allow browser scroll when content is long */
  overflow:auto;

  background:
    radial-gradient(1200px 600px at 10% 10%, rgba(34,197,94,.25), transparent 60%),
    radial-gradient(900px 500px at 90% 20%, rgba(56,189,248,.18), transparent 60%),
    radial-gradient(700px 500px at 50% 90%, rgba(168,85,247,.12), transparent 60%),
    linear-gradient(160deg,var(--bg1),var(--bg2));
}
.aurora{
  position:fixed; inset:-20%;
  background:
    radial-gradient(circle at 20% 30%, rgba(34,197,94,.24), transparent 55%),
    radial-gradient(circle at 70% 35%, rgba(56,189,248,.20), transparent 55%),
    radial-gradient(circle at 50% 80%, rgba(168,85,247,.14), transparent 55%);
  filter: blur(40px);
  animation: drift 10s ease-in-out infinite alternate;
  pointer-events:none;
}
@keyframes drift{
  from{transform:translate3d(-2%, -1%,0) scale(1.05)}
  to{transform:translate3d(2%, 1.5%,0) scale(1.08)}
}
.wrap{
  position:relative;

  /* ✅ CHANGED: use min-height + align to top so scrolling feels natural */
  min-height:100%;
  display:grid;
  place-items:start center;

  padding:28px;
}
.card{
  width:min(980px, 96vw);
  border:1px solid rgba(25,54,74,.9);
  background:linear-gradient(180deg, rgba(11,23,35,.78), rgba(11,23,35,.55));
  border-radius:22px;
  box-shadow:
    0 30px 90px rgba(0,0,0,.55),
    0 0 0 1px rgba(34,197,94,.10),
    0 0 60px rgba(34,197,94,.10);
  overflow:hidden;
  transform: translateY(14px);
  opacity:0;
  animation: rise .7s ease forwards;
}
@keyframes rise{
  to{transform:translateY(0); opacity:1;}
}
.topbar{
  display:flex; align-items:center; justify-content:space-between;
  padding:18px 18px 12px 18px;
  border-bottom:1px solid rgba(25,54,74,.7);
}
.brand{
  display:flex; gap:12px; align-items:center;
}
.pulse{
  width:14px;height:14px;border-radius:50%;
  background:var(--good);
  box-shadow:0 0 18px rgba(34,197,94,.9);
  position:relative;
}
.pulse:after{
  content:""; position:absolute; inset:-10px;
  border-radius:50%;
  border:2px solid rgba(34,197,94,.35);
  animation: ping 1.4s ease-out infinite;
}
@keyframes ping{
  from{transform:scale(.2); opacity:.95}
  to{transform:scale(1.2); opacity:0}
}
.h1{
  font-weight:900;
  letter-spacing:.6px;
  font-size:20px;
}
.badge{
  font-weight:800;
  font-size:12px;
  padding:8px 12px;
  border-radius:999px;
  border:1px solid rgba(34,197,94,.55);
  background:rgba(34,197,94,.08);
  color:var(--good2);
  box-shadow:0 0 18px rgba(34,197,94,.18) inset;
}
.content{
  padding:18px;
  display:grid;
  gap:14px;
}
.hero{
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:16px;
  padding:16px;
  border:1px solid rgba(25,54,74,.65);
  background:rgba(2,6,23,.35);
  border-radius:18px;
  position:relative;
  overflow:hidden;
}
.shimmer{
  position:absolute; inset:-120px;
  background: linear-gradient(120deg, transparent 40%, rgba(34,197,94,.14) 50%, transparent 60%);
  transform: translateX(-30%);
  animation: shine 2.6s ease-in-out infinite;
}
@keyframes shine{
  0%{transform:translateX(-40%)}
  60%{transform:translateX(20%)}
  100%{transform:translateX(40%)}
}
.hero h2{
  margin:0;
  font-size:18px;
  font-weight:900;
}
.hero p{
  margin:8px 0 0 0;
  color:var(--muted);
  line-height:1.5;
}
.kv{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:12px;
}
.kv .box{
  border:1px solid rgba(25,54,74,.6);
  background:rgba(2,6,23,.35);
  border-radius:16px;
  padding:14px;
}
.k{
  color:var(--muted);
  font-size:12px;
  letter-spacing:.4px;
  text-transform:uppercase;
}
.v{
  margin-top:6px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size:13px;
  word-break:break-all;
}
.list{
  border:1px solid rgba(25,54,74,.6);
  background:rgba(2,6,23,.35);
  border-radius:16px;
  padding:14px;
}
.list h3{margin:0 0 10px 0;font-size:14px;letter-spacing:.4px;text-transform:uppercase;color:#c7d2fe}
ul{margin:0;padding-left:18px;color:var(--text)}
li{margin:8px 0;color:#d1fae5}

.vendors{
  border:1px solid rgba(25,54,74,.6);
  background:rgba(2,6,23,.35);
  border-radius:16px;
  padding:14px;
}
.vendors h3{margin:0 0 10px 0;font-size:14px;letter-spacing:.4px;text-transform:uppercase;color:#c7d2fe}
table{
  width:100%;
  border-collapse:collapse;
  font-size:13px;
}
th, td{
  text-align:left;
  padding:10px 10px;
  border-bottom:1px solid rgba(25,54,74,.55);
}
th{
  color:var(--muted);
  font-size:12px;
  letter-spacing:.35px;
  text-transform:uppercase;
}
.tag{
  display:inline-block;
  padding:4px 10px;
  border-radius:999px;
  font-weight:800;
  font-size:12px;
  border:1px solid rgba(25,54,74,.55);
  background:rgba(148,163,184,.08);
  color:#e5e7eb;
}
.tag.clean{border-color:rgba(34,197,94,.55);background:rgba(34,197,94,.10);color:#bbf7d0}
.tag.malware{border-color:rgba(239,68,68,.55);background:rgba(239,68,68,.12);color:#fecaca}
.tag.unrated{border-color:rgba(245,158,11,.55);background:rgba(245,158,11,.12);color:#fde68a}

.footer{
  display:flex;justify-content:space-between;align-items:center;
  padding:14px 18px;
  border-top:1px solid rgba(25,54,74,.7);
  color:var(--muted);
  font-size:12px;
}
button{
  cursor:pointer;
  border:none;
  padding:10px 12px;
  border-radius:12px;
  font-weight:800;
  background:rgba(34,197,94,.14);
  color:#d1fae5;
  border:1px solid rgba(34,197,94,.35);
}
button:hover{background:rgba(34,197,94,.18)}
.bubbles{
  position:fixed; inset:0;
  pointer-events:none;
  opacity:.55;
}
.bubbles span{
  position:absolute;
  border-radius:999px;
  background: radial-gradient(circle at 30% 30%, rgba(34,197,94,.28), rgba(56,189,248,.12), transparent 60%);
  filter: blur(1px);
  animation: float 9s linear infinite;
}
@keyframes float{
  from{transform:translateY(120vh) translateX(0) scale(.8); opacity:0}
  10%{opacity:.8}
  to{transform:translateY(-20vh) translateX(40px) scale(1.1); opacity:0}
}
</style>
</head>
<body>
<div class="aurora"></div>
<div class="bubbles" aria-hidden="true" id="bubbles"></div>

<div class="wrap">
  <div class="card">
    <div class="topbar">
      <div class="brand">
        <div class="pulse"></div>
        <div>
          <div class="h1">Scan Report</div>
          <div style="color:var(--muted);font-size:12px;margin-top:2px">Status: SAFE • VirusTotal result</div>
        </div>
      </div>
      <div class="badge">✅ SAFE</div>
    </div>

    <div class="content">
      <div class="hero">
        <div class="shimmer"></div>
        <div>
          <h2>No malicious detections found by VirusTotal.</h2>
          <p>Always verify destination domains and avoid entering credentials on unknown pages.</p>
        </div>
        <div style="min-width:220px;text-align:right">
          <div class="k">Scan time</div>
          <div class="v">{{scan_time}}</div>
          <div style="height:8px"></div>
          <div class="k">Tool</div>
          <div class="v">Malware Link Detection</div>
        </div>
      </div>

      <div class="kv">
        <div class="box">
          <div class="k">Input</div>
          <div class="v">{{input_value}}</div>
        </div>
        <div class="box">
          <div class="k">Top-level domain</div>
          <div class="v">{{tld}}</div>
        </div>
      </div>

      <div class="list">
        <h3>Details</h3>
        <ul>
          {{reasons_list}}
        </ul>
      </div>

      <div class="vendors">
        <h3>Security vendors' analysis</h3>
        {{vendors_table}}
      </div>
    </div>

    <div class="footer">
      <div>Generated locally • No data stored by this report</div>
      <div style="display:flex;gap:10px;align-items:center">
        <button onclick="window.print()">Print</button>
        <button onclick="navigator.clipboard.writeText('{{input_value}}')">Copy Input</button>
      </div>
    </div>
  </div>
</div>

<script>
(function(){
  const root = document.getElementById('bubbles');
  const n = 14;
  for(let i=0;i<n;i++){
    const s = document.createElement('span');
    const size = 90 + Math.random()*180;
    s.style.width = size+'px';
    s.style.height = size+'px';
    s.style.left = (Math.random()*100)+'vw';
    s.style.animationDuration = (7 + Math.random()*7)+'s';
    s.style.animationDelay = (-Math.random()*8)+'s';
    root.appendChild(s);
  }
})();
</script>
</body>
</html>
"""

MALICIOUS_HTML_TEMPLATE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Scan Report • MALICIOUS</title>
<style>
:root{
  --bg:#06060a;
  --card:#0b0b12cc;
  --line:#3b1b1b;
  --bad:#ef4444;
  --text:#f3f4f6;
  --muted:#9ca3af;
}
*{box-sizing:border-box}
html,body{height:100%;margin:0;font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Arial}
body{
  color:var(--text);

  /* ✅ CHANGED: allow browser scroll when content is long */
  overflow:auto;

  background:
    radial-gradient(1000px 600px at 18% 18%, rgba(239,68,68,.24), transparent 60%),
    radial-gradient(900px 600px at 80% 20%, rgba(168,85,247,.16), transparent 60%),
    radial-gradient(900px 500px at 50% 90%, rgba(14,165,233,.10), transparent 60%),
    linear-gradient(160deg,#04040a,#070712);
}
.grid{
  position:fixed; inset:0;
  background-image:
    linear-gradient(rgba(239,68,68,.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(239,68,68,.08) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(circle at 50% 30%, black 0%, transparent 70%);
  animation: drift 8s linear infinite;
  pointer-events:none;
}
@keyframes drift{
  from{transform:translateY(0)}
  to{transform:translateY(48px)}
}
.wrap{
  position:relative;

  /* ✅ CHANGED: use min-height + align to top so scrolling feels natural */
  min-height:100%;
  display:grid;
  place-items:start center;

  padding:28px;
}
.card{
  width:min(980px, 96vw);
  border:1px solid rgba(59,27,27,.9);
  background:linear-gradient(180deg, rgba(11,11,18,.86), rgba(11,11,18,.52));
  border-radius:22px;
  box-shadow:
    0 30px 90px rgba(0,0,0,.60),
    0 0 0 1px rgba(239,68,68,.10),
    0 0 70px rgba(239,68,68,.20);
  overflow:hidden;
  transform: translateY(16px);
  opacity:0;
  animation: enter .7s ease forwards;
}
@keyframes enter{
  to{transform:translateY(0); opacity:1;}
}
.topbar{
  display:flex; align-items:center; justify-content:space-between;
  padding:18px 18px 12px 18px;
  border-bottom:1px solid rgba(59,27,27,.75);
}
.brand{display:flex; gap:12px; align-items:center}
.siren{
  width:14px;height:14px;border-radius:50%;
  background:var(--bad);
  box-shadow:0 0 22px rgba(239,68,68,.95);
  position:relative;
}
.siren:after{
  content:""; position:absolute; inset:-12px;
  border-radius:50%;
  border:2px solid rgba(239,68,68,.30);
  animation: ping 1.2s ease-out infinite;
}
@keyframes ping{
  from{transform:scale(.15); opacity:.95}
  to{transform:scale(1.35); opacity:0}
}
.h1{font-weight:900;letter-spacing:.6px;font-size:20px;}
.badge{
  font-weight:900;
  font-size:12px;
  padding:8px 12px;
  border-radius:999px;
  border:1px solid rgba(239,68,68,.55);
  background:rgba(239,68,68,.10);
  color:#fecaca;
}
.content{padding:18px; display:grid; gap:14px;}
.hero{
  position:relative;
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:16px;
  padding:16px;
  border:1px solid rgba(59,27,27,.65);
  background:rgba(2,6,23,.40);
  border-radius:18px;
  overflow:hidden;
}
.hero h2{margin:0;font-size:18px;font-weight:950}
.hero p{margin:8px 0 0 0;color:var(--muted);line-height:1.5}
.kv{display:grid; grid-template-columns:1fr 1fr; gap:12px;}
.kv .box{
  border:1px solid rgba(59,27,27,.55);
  background:rgba(2,6,23,.40);
  border-radius:16px;
  padding:14px;
}
.k{
  color:var(--muted);
  font-size:12px;
  letter-spacing:.4px;
  text-transform:uppercase;
}
.v{
  margin-top:6px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size:13px;
  word-break:break-all;
}
.list{
  border:1px solid rgba(59,27,27,.55);
  background:rgba(2,6,23,.40);
  border-radius:16px;
  padding:14px;
}
.list h3{margin:0 0 10px 0;font-size:14px;letter-spacing:.4px;text-transform:uppercase;color:#fecaca}
ul{margin:0;padding-left:18px}
li{margin:8px 0;color:#fee2e2}

.vendors{
  border:1px solid rgba(59,27,27,.55);
  background:rgba(2,6,23,.40);
  border-radius:16px;
  padding:14px;
}
.vendors h3{margin:0 0 10px 0;font-size:14px;letter-spacing:.4px;text-transform:uppercase;color:#fecaca}
table{
  width:100%;
  border-collapse:collapse;
  font-size:13px;
}
th, td{
  text-align:left;
  padding:10px 10px;
  border-bottom:1px solid rgba(59,27,27,.55);
}
th{
  color:var(--muted);
  font-size:12px;
  letter-spacing:.35px;
  text-transform:uppercase;
}
.tag{
  display:inline-block;
  padding:4px 10px;
  border-radius:999px;
  font-weight:900;
  font-size:12px;
  border:1px solid rgba(59,27,27,.55);
  background:rgba(148,163,184,.08);
  color:#f3f4f6;
}
.tag.clean{border-color:rgba(34,197,94,.55);background:rgba(34,197,94,.10);color:#bbf7d0}
.tag.malware{border-color:rgba(239,68,68,.55);background:rgba(239,68,68,.12);color:#fecaca}
.tag.unrated{border-color:rgba(245,158,11,.55);background:rgba(245,158,11,.12);color:#fde68a}

.footer{
  display:flex;justify-content:space-between;align-items:center;
  padding:14px 18px;
  border-top:1px solid rgba(59,27,27,.75);
  color:var(--muted);
  font-size:12px;
}
button{
  cursor:pointer;
  border:none;
  padding:10px 12px;
  border-radius:12px;
  font-weight:900;
  background:rgba(239,68,68,.16);
  color:#ffe4e6;
  border:1px solid rgba(239,68,68,.35);
}
button:hover{background:rgba(239,68,68,.22)}
</style>
</head>
<body>
<div class="grid"></div>

<div class="wrap">
  <div class="card">
    <div class="topbar">
      <div class="brand">
        <div class="siren"></div>
        <div>
          <div class="h1">Scan Report</div>
          <div style="color:var(--muted);font-size:12px;margin-top:2px">Status: MALICIOUS • VirusTotal detections</div>
        </div>
      </div>
      <div class="badge">⚠ MALICIOUS</div>
    </div>

    <div class="content">
      <div class="hero">
        <div>
          <h2>DO NOT INTERACT</h2>
          <p>This destination triggered one or more VirusTotal detections. Avoid opening it.</p>
        </div>
        <div style="min-width:220px;text-align:right">
          <div class="k">Scan time</div>
          <div class="v">{{scan_time}}</div>
          <div style="height:8px"></div>
          <div class="k">Tool</div>
          <div class="v">Malware Link Detection</div>
        </div>
      </div>

      <div class="kv">
        <div class="box">
          <div class="k">Input</div>
          <div class="v">{{input_value}}</div>
        </div>
        <div class="box">
          <div class="k">Top-level domain</div>
          <div class="v">{{tld}}</div>
        </div>
      </div>

      <div class="list">
        <h3>Reasons</h3>
        <ul>
          {{reasons_list}}
        </ul>
      </div>

      <div class="vendors">
        <h3>Security vendors' analysis</h3>
        {{vendors_table}}
      </div>
    </div>

    <div class="footer">
      <div>High risk • Recommended: block domain & report incident</div>
      <div style="display:flex;gap:10px;align-items:center">
        <button onclick="window.print()">Print</button>
        <button onclick="navigator.clipboard.writeText('{{input_value}}')">Copy Input</button>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""

# =========================
# HTML helpers
# =========================
def _escape_html(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") \
                    .replace('"', "&quot;").replace("'", "&#39;")

def build_vendors_table_html(vendors_rows):
    """
    vendors_rows: list of (vendor_name, status_label) where status_label in {"Clean","Malware","Unrated"}
    """
    if not vendors_rows:
        return "<div style='color:#9ca3af'>No vendor analysis available.</div>"

    def tag_class(label):
        if label.lower() == "clean":
            return "clean"
        if label.lower() == "malware":
            return "malware"
        return "unrated"

    rows_html = []
    for v, s in vendors_rows:
        rows_html.append(
            "<tr>"
            f"<td>{_escape_html(v)}</td>"
            f"<td><span class='tag {tag_class(s)}'>{_escape_html(s)}</span></td>"
            "</tr>"
        )

    return (
        "<table>"
        "<thead><tr><th>Vendor</th><th>Verdict</th></tr></thead>"
        "<tbody>"
        + "\n".join(rows_html) +
        "</tbody></table>"
    )

def open_result_html_dynamic(is_threat: bool, input_value: str, reasons: list, tld: str, vendors_rows=None):
    scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    template = MALICIOUS_HTML_TEMPLATE if is_threat else SAFE_HTML_TEMPLATE

    if reasons:
        reasons_list_html = "".join(f"<li>{_escape_html(r)}</li>\n" for r in reasons)
    else:
        reasons_list_html = "<li>No details available.</li>"

    vendors_table = build_vendors_table_html(vendors_rows or [])

    html = (template
        .replace("{{scan_time}}", _escape_html(scan_time))
        .replace("{{input_value}}", _escape_html(input_value))
        .replace("{{tld}}", _escape_html(tld or "N/A"))
        .replace("{{reasons_list}}", reasons_list_html)
        .replace("{{vendors_table}}", vendors_table)
    )

    temp_dir = tempfile.gettempdir()
    name = f"scan_report_{'mal' if is_threat else 'safe'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    html_path = os.path.join(temp_dir, name)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    webbrowser.open_new_tab(f"file:///{html_path}")


# =========================
# VirusTotal helpers (URL submission + polling)
# =========================
def vt_url_id(url: str) -> str:
    return base64.urlsafe_b64encode(url.encode()).decode().strip("=")

def vt_headers():
    return {"x-apikey": VIRUSTOTAL_API_KEY, "Accept": "application/json"}

def submit_url_to_virustotal(url: str) -> (bool, str):
    """
    POST /urls to trigger analysis.
    """
    if not VIRUSTOTAL_API_KEY or VIRUSTOTAL_API_KEY == "PUT_YOUR_VIRUSTOTAL_API_KEY_HERE":
        return False, "VirusTotal API key is not configured."

    try:
        resp = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers={"x-apikey": VIRUSTOTAL_API_KEY, "Content-Type": "application/x-www-form-urlencoded"},
            data={"url": url},
            timeout=20
        )
        resp.raise_for_status()
        return True, "URL submitted to VirusTotal."
    except Exception as e:
        return False, f"VirusTotal submit error: {e}"

def fetch_url_report(url: str) -> (bool, int, dict, dict, str):
    """
    GET /urls/{id} to fetch analysis stats + per-vendor results.
    Returns: (ok, malicious_count, stats_dict, analysis_results_dict, message)
    """
    url_id = vt_url_id(url)
    vt_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"

    try:
        resp = requests.get(vt_url, headers=vt_headers(), timeout=20)
        if resp.status_code == 404:
            return False, 0, {}, {}, "VirusTotal: report not ready yet."
        resp.raise_for_status()
        data = resp.json()
        attrs = data.get("data", {}).get("attributes", {})
        stats = attrs.get("last_analysis_stats", {}) or {}
        results = attrs.get("last_analysis_results", {}) or {}
        malicious = int(stats.get("malicious", 0) or 0)
        return True, malicious, stats, results, "VirusTotal report fetched."
    except Exception as e:
        return False, 0, {}, {}, f"VirusTotal fetch error: {e}"

def normalize_vendor_status_from_vt(vt_entry: dict) -> str:
    """
    Convert VirusTotal engine result into: Clean / Malware / Unrated
    """
    if not isinstance(vt_entry, dict):
        return "Unrated"

    category = (vt_entry.get("category") or "").lower().strip()
    result = (vt_entry.get("result") or "").lower().strip()

    # Strong signals
    if category in ("malicious", "suspicious"):
        return "Malware"

    # Treat "harmless" and "undetected" as clean for this UI
    if category in ("harmless", "undetected"):
        return "Clean"

    # Sometimes engines put meaning in result text
    if "malware" in result or "phish" in result or "spam" in result or "suspicious" in result:
        return "Malware"

    # Timeout / unrated / unknown => Unrated
    return "Unrated"

def build_security_vendors_rows(vt_results: dict):
    """
    Build ordered vendor list: [(vendor, Clean/Malware/Unrated), ...]
    """
    rows = []
    for vendor in SECURITY_VENDORS_ORDER:
        status = "Unrated"
        if isinstance(vt_results, dict) and vendor in vt_results:
            status = normalize_vendor_status_from_vt(vt_results.get(vendor) or {})
        rows.append((vendor, status))
    return rows

def vendors_rows_to_text(vendors_rows):
    """
    Build a readable text block for popup/PDF
    """
    if not vendors_rows:
        return "Security vendors' analysis: Not available"
    lines = ["Security vendors' analysis:"]
    for v, s in vendors_rows:
        lines.append(f"- {v}: {s}")
    return "\n".join(lines)

def query_virustotal_url(url: str, poll_seconds: int = 8, poll_interval: float = 1.0):
    """
    Submit + poll for up to poll_seconds.
    Verdict uses ONLY VirusTotal:
      - malicious > 0 => malicious
      - else => safe
    Returns:
      (is_malicious_bool, malicious_count, reason_message, vendors_rows)
    """
    if not VIRUSTOTAL_API_KEY or VIRUSTOTAL_API_KEY == "PUT_YOUR_VIRUSTOTAL_API_KEY_HERE":
        return False, 0, "VirusTotal API key is not configured.", []

    ok, msg = submit_url_to_virustotal(url)
    if not ok:
        return False, 0, msg, []

    # poll
    start = time.time()
    while time.time() - start < poll_seconds:
        ok2, malicious, stats, vt_results, message = fetch_url_report(url)
        if ok2:
            harmless = int(stats.get("harmless", 0) or 0)
            suspicious = int(stats.get("suspicious", 0) or 0)
            undetected = int(stats.get("undetected", 0) or 0)
            timeout = int(stats.get("timeout", 0) or 0)

            vendors_rows = build_security_vendors_rows(vt_results)

            details = (f"VirusTotal stats: malicious={malicious}, suspicious={suspicious}, "
                       f"harmless={harmless}, undetected={undetected}, timeout={timeout}")

            if malicious > 0 or suspicious > 0:
                # For your UI: anything suspicious or malicious => MALICIOUS
                det_count = int(malicious + suspicious)
                return True, det_count, f"VirusTotal detected malicious/suspicious engines. {details}", vendors_rows

            return False, 0, f"VirusTotal: No malicious detections. {details}", vendors_rows

        time.sleep(poll_interval)

    return False, 0, "VirusTotal: URL submitted, but analysis not ready yet. Please scan again in a few seconds.", []

def query_virustotal_hash(file_hash: str):
    """
    GET /files/{sha256}
    Returns:
      (is_malicious_bool, malicious_or_suspicious_count, reason_message, vendors_rows)
    """
    if not VIRUSTOTAL_API_KEY or VIRUSTOTAL_API_KEY == "PUT_YOUR_VIRUSTOTAL_API_KEY_HERE":
        return False, 0, "VirusTotal API key is not configured.", []

    vt_url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    try:
        resp = requests.get(vt_url, headers=vt_headers(), timeout=20)
        if resp.status_code == 404:
            return False, 0, "VirusTotal: No existing report for this hash.", []
        resp.raise_for_status()
        data = resp.json()
        attrs = data.get("data", {}).get("attributes", {}) or {}
        stats = attrs.get("last_analysis_stats", {}) or {}
        vt_results = attrs.get("last_analysis_results", {}) or {}

        malicious = int(stats.get("malicious", 0) or 0)
        suspicious = int(stats.get("suspicious", 0) or 0)

        harmless = int(stats.get("harmless", 0) or 0)
        undetected = int(stats.get("undetected", 0) or 0)
        timeout = int(stats.get("timeout", 0) or 0)

        vendors_rows = build_security_vendors_rows(vt_results)

        details = (f"VirusTotal stats: malicious={malicious}, suspicious={suspicious}, "
                   f"harmless={harmless}, undetected={undetected}, timeout={timeout}")

        if malicious > 0 or suspicious > 0:
            det_count = int(malicious + suspicious)
            return True, det_count, f"VirusTotal detected malicious/suspicious engines for this hash. {details}", vendors_rows
        return False, 0, f"VirusTotal: No malicious detections for this hash. {details}", vendors_rows
    except Exception as e:
        return False, 0, f"VirusTotal API error: {e}", []


# =========================
# Detection (VirusTotal ONLY) + Vendors Analysis
# =========================
def is_malicious(input_string, is_hash_scan=False):
    s = (input_string or "").strip()
    reasons = []
    tld = "N/A"
    vendors_rows = []

    if not s:
        return False, ["Empty input."], tld, vendors_rows

    if is_hash_scan:
        if not re.match(r'^[0-9a-fA-F]{64}$', s):
            return False, ["Please enter a valid SHA-256 hash (64 hex)."], tld, vendors_rows

        vt_is_mal, _, vt_reason, vendors_rows = query_virustotal_hash(s.lower())
        reasons.append(f"VirusTotal Hash Scan: {vt_reason}")
        return bool(vt_is_mal), reasons, tld, vendors_rows

    # If user typed domain only, add https://
    if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$', s) and not s.lower().startswith(("http://", "https://")):
        s = "https://" + s

    if not s.lower().startswith(("http://", "https://")):
        return False, ["Input is not a valid URL (must start with http:// or https://)."], tld, vendors_rows

    # Extract TLD for display only
    try:
        domain_part = s.lower().split('//')[-1].split('/')[0].split(':')[0]
        tld_match = re.search(r'\.([a-zA-Z]{2,})$', domain_part)
        if tld_match:
            tld = tld_match.group(1)
    except Exception:
        tld = "N/A"

    vt_is_mal, _, vt_reason, vendors_rows = query_virustotal_url(s)
    reasons.append(f"VirusTotal URL Scan: {vt_reason}")
    return bool(vt_is_mal), reasons, tld, vendors_rows


# =========================
# PDF + Email
# =========================
def generate_pdf_report(report_data):
    temp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(temp_dir, f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    styles = getSampleStyleSheet()

    body_style = ParagraphStyle(
        name='BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=12,
        alignment=TA_LEFT
    )

    y_position = height - 50
    margin_left = 40
    content_width = width - 2 * margin_left

    vendors_rows = report_data.get("vendors_rows") or []

    if report_data.get('scan_type') == 'URL':
        c.setFont("Helvetica-Bold", 18)
        c.drawString(margin_left, y_position, "Malware Link Detection Report")
        y_position -= 30

        c.setFont("Helvetica", 10)
        c.drawString(margin_left, y_position, f"Scan Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        y_position -= 14
        c.drawString(margin_left, y_position, "Tool Version: 1.0.0")
        y_position -= 14
        c.drawString(margin_left, y_position, "Detection Source: VirusTotal ONLY")
        y_position -= 28

        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin_left, y_position, "Scanned URL:")
        y_position -= 20
        p = Paragraph(report_data.get('input_value', 'N/A'), body_style)
        p.wrapOn(c, content_width, height)
        p.drawOn(c, margin_left, y_position - p.height)
        y_position -= (p.height + 20)

        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin_left, y_position, f"Verdict: {report_data.get('verdict', 'Unknown')}")
        y_position -= 18

        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin_left, y_position, "Detected Reasons:")
        y_position -= 14

        c.setFont("Helvetica", 10)
        for r in report_data.get('detected_reasons', []):
            p = Paragraph(f"• {r}", body_style)
            p.wrapOn(c, content_width, height)
            p.drawOn(c, margin_left, y_position - p.height)
            y_position -= (p.height + 4)
            if y_position < 120:
                c.showPage()
                y_position = height - 50
                c.setFont("Helvetica", 10)

        # Vendors block
        if vendors_rows:
            y_position -= 10
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin_left, y_position, "Security vendors' analysis:")
            y_position -= 14
            c.setFont("Helvetica", 9)
            for v, s in vendors_rows:
                p = Paragraph(f"• {v}: {s}", body_style)
                p.wrapOn(c, content_width, height)
                p.drawOn(c, margin_left, y_position - p.height)
                y_position -= (p.height + 2)
                if y_position < 60:
                    c.showPage()
                    y_position = height - 50
                    c.setFont("Helvetica", 9)

    else:
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin_left, y_position, f"{report_data.get('scan_type', 'Scan')} Report")
        y_position -= 25
        report_text = report_data.get('report_text') or "No report content available."
        for line in report_text.split('\n'):
            p = Paragraph(line, body_style)
            p.wrapOn(c, content_width, height)
            p.drawOn(c, margin_left, y_position - p.height)
            y_position -= (p.height + 2)
            if y_position < 60:
                c.showPage()
                y_position = height - 50
                c.setFont("Helvetica", 10)

    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2.0, 30, "Generated by: Malware Link Detection Tool")
    c.drawCentredString(width / 2.0, 20, "Detection: VirusTotal ONLY")
    c.save()
    return pdf_path

def show_custom_popup(title, message, alert_type="info"):
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.geometry("860x620")
    popup.configure(bg="#0b1020")
    popup.transient(root)
    popup.grab_set()

    colors_map = {
        "info": ("#2dd4bf", "✅"),
        "warning": ("#f59e0b", "⚠"),
        "error": ("#ef4444", "❌")
    }
    color, symbol = colors_map.get(alert_type, ("#22c55e", "✅"))

    card = tk.Frame(popup, bg="#0f172a", highlightbackground="#1f2a44", highlightthickness=1)
    card.pack(padx=18, pady=18, fill=tk.BOTH, expand=True)

    header = tk.Frame(card, bg="#0f172a")
    header.pack(fill=tk.X, padx=16, pady=(16, 8))

    tk.Label(header, text=symbol, font=("Segoe UI Emoji", 34), fg=color, bg="#0f172a").pack(side=tk.LEFT)
    tk.Label(header, text=title, font=("Segoe UI", 20, "bold"), fg="white", bg="#0f172a").pack(side=tk.LEFT, padx=10)

    body = tk.Frame(card, bg="#0f172a")
    body.pack(fill=tk.BOTH, expand=True, padx=16, pady=(8, 12))

    text_widget = Text(
        body, wrap=tk.WORD, font=("Consolas", 11),
        bg="#0b1020", fg="#e5e7eb", insertbackground="white",
        relief=tk.FLAT, highlightthickness=1, highlightbackground="#1f2a44"
    )
    text_widget.insert(tk.END, message)
    text_widget.config(state=tk.DISABLED)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    sb = Scrollbar(body, command=text_widget.yview)
    sb.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=sb.set)

    footer = tk.Frame(card, bg="#0f172a")
    footer.pack(fill=tk.X, padx=16, pady=(0, 16))

    tk.Button(
        footer, text="OK", command=popup.destroy,
        bg=color, fg="black", font=("Segoe UI", 11, "bold"),
        activebackground=color, activeforeground="black",
        relief=tk.FLAT, padx=18, pady=8, cursor="hand2"
    ).pack(side=tk.RIGHT)

def send_email_report(recipient_email, subject, body_data):
    if not GMAIL_SENDER or not GMAIL_APP_PASSWORD or "your_gmail_app_password" in GMAIL_APP_PASSWORD:
        show_custom_popup("Email Error", "Configure GMAIL_SENDER and GMAIL_APP_PASSWORD first.", "error")
        return

    pdf_path = None
    try:
        pdf_path = generate_pdf_report(body_data)

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = GMAIL_SENDER
        msg['To'] = recipient_email

        msg.set_content(
            f"Dear User,\n\nPlease find the attached scan report.\n\n"
            f"Scan Type: {body_data.get('scan_type', 'N/A')}\n"
            f"Input: {body_data.get('input_value', 'N/A')}\n"
            f"Verdict: {body_data.get('verdict', 'Unknown')}\n\n"
            f"Regards,\nMalware Link Detection Tool"
        )

        with open(pdf_path, 'rb') as f:
            msg.add_attachment(
                f.read(),
                maintype='application',
                subtype='pdf',
                filename=os.path.basename(pdf_path)
            )

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)

        show_custom_popup("Email Sent", f"Report sent to {recipient_email}", "info")

    except smtplib.SMTPAuthenticationError as e:
        show_custom_popup("Email Error", f"SMTP Authentication Error: {e}", "error")
    except Exception as e:
        show_custom_popup("Email Error", f"Could not send email:\n{e}", "error")
    finally:
        if pdf_path and os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
            except Exception:
                pass


# =========================
# Main scan actions
# =========================
def scan_url():
    url = url_entry.get().strip()
    recipient_email = email_entry.get().strip()

    if not url:
        show_custom_popup("Input Error", "Please enter a URL to scan.", "error")
        return

    if recipient_email and not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", recipient_email):
        show_custom_popup("Invalid Email", "Only Gmail addresses are allowed.", "error")
        return

    is_threat, reasons, tld, vendors_rows = is_malicious(url)
    verdict = "Malicious" if is_threat else "Safe"

    open_result_html_dynamic(is_threat, url, reasons, tld, vendors_rows=vendors_rows)

    popup_msg = (
        f"Verdict: {verdict}\n\n"
        + "\n".join(f"- {r}" for r in reasons)
        + "\n\n"
        + vendors_rows_to_text(vendors_rows)
    )

    show_custom_popup(
        "Scan Results",
        popup_msg,
        "warning" if is_threat else "info"
    )

    if recipient_email:
        send_email_report(recipient_email, f"URL Scan Report - {verdict}", {
            "scan_type": "URL",
            "input_value": url,
            "verdict": verdict,
            "detected_reasons": reasons,
            "tld": tld,
            "vendors_rows": vendors_rows
        })

def extract_qr_from_image(image_path):
    results = []
    img = cv2.imread(image_path)
    if img is None:
        return results

    if PYZBAR_AVAILABLE:
        try:
            decoded = zbar_decode(img)
            for d in decoded:
                try:
                    results.append(d.data.decode("utf-8", errors="ignore").strip())
                except Exception:
                    pass
            if results:
                return results
        except Exception:
            pass

    try:
        detector = cv2.QRCodeDetector()
        data, points, _ = detector.detectAndDecode(img)
        if data:
            results.append(data.strip())
    except Exception:
        pass

    return results

def scan_qr_from_image():
    img_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp")]
    )
    if not img_path:
        return

    decoded_list = extract_qr_from_image(img_path)
    if not decoded_list:
        show_custom_popup("QR Scan", "No QR code detected in the selected image.", "warning")
        return

    qr_data = decoded_list[0].strip()

    url_entry.delete(0, tk.END)
    url_entry.insert(0, qr_data)

    # normalize domain-only to https://
    if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$', qr_data) and not qr_data.lower().startswith(("http://", "https://")):
        qr_data = "https://" + qr_data
        url_entry.delete(0, tk.END)
        url_entry.insert(0, qr_data)

    if qr_data.lower().startswith(("http://", "https://")):
        is_threat, reasons, tld, vendors_rows = is_malicious(qr_data)
        verdict = "Malicious" if is_threat else "Safe"

        open_result_html_dynamic(is_threat, qr_data, reasons, tld, vendors_rows=vendors_rows)

        popup_msg = "\n".join(reasons) + "\n\n" + vendors_rows_to_text(vendors_rows)
        show_custom_popup("QR Scan Results", popup_msg, "warning" if is_threat else "info")

        # ✅ ADDED: send email for QR scan also (uses same recipient field)
        recipient_email = email_entry.get().strip()
        if recipient_email:
            if not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", recipient_email):
                show_custom_popup("Invalid Email", "Only Gmail addresses are allowed.", "error")
                return

            send_email_report(recipient_email, f"QR Scan Report - {verdict}", {
                "scan_type": "URL",  # keep PDF format consistent (URL-style section)
                "input_value": qr_data,
                "verdict": verdict,
                "detected_reasons": reasons,
                "tld": tld,
                "vendors_rows": vendors_rows
            })

    else:
        show_custom_popup("QR Decoded", f"QR content detected:\n\n{qr_data}", "info")

def scan_qr_via_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        show_custom_popup("Camera Error", "Could not open webcam.", "error")
        return

    detector = cv2.QRCodeDetector()
    found_data = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        data, points, _ = detector.detectAndDecode(frame)

        if not data and PYZBAR_AVAILABLE:
            try:
                decoded = zbar_decode(frame)
                if decoded:
                    data = decoded[0].data.decode("utf-8", errors="ignore").strip()
            except Exception:
                pass

        if data:
            found_data = data.strip()
            cv2.putText(frame, "QR DETECTED", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("QR Scanner (press q to quit)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if found_data:
            break

    cap.release()
    cv2.destroyAllWindows()

    if not found_data:
        show_custom_popup("QR Scan", "No QR code detected from camera.", "warning")
        return

    qr_data = found_data
    url_entry.delete(0, tk.END)
    url_entry.insert(0, qr_data)

    if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$', qr_data) and not qr_data.lower().startswith(("http://", "https://")):
        qr_data = "https://" + qr_data
        url_entry.delete(0, tk.END)
        url_entry.insert(0, qr_data)

    if qr_data.lower().startswith(("http://", "https://")):
        is_threat, reasons, tld, vendors_rows = is_malicious(qr_data)
        verdict = "Malicious" if is_threat else "Safe"

        open_result_html_dynamic(is_threat, qr_data, reasons, tld, vendors_rows=vendors_rows)

        popup_msg = "\n".join(reasons) + "\n\n" + vendors_rows_to_text(vendors_rows)
        show_custom_popup("QR Camera Results", popup_msg, "warning" if is_threat else "info")

        # ✅ ADDED: send email for QR camera scan also (uses same recipient field)
        recipient_email = email_entry.get().strip()
        if recipient_email:
            if not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", recipient_email):
                show_custom_popup("Invalid Email", "Only Gmail addresses are allowed.", "error")
                return

            send_email_report(recipient_email, f"QR Camera Scan Report - {verdict}", {
                "scan_type": "URL",  # keep PDF format consistent (URL-style section)
                "input_value": qr_data,
                "verdict": verdict,
                "detected_reasons": reasons,
                "tld": tld,
                "vendors_rows": vendors_rows
            })

    else:
        show_custom_popup("QR Decoded", f"QR content detected:\n\n{qr_data}", "info")

def scan_hash():
    text_input = hash_entry.get().strip()
    if not text_input:
        show_custom_popup("Input Error", "Please enter a hash to scan.", "error")
        return
    if not re.match(r'^[0-9a-fA-F]{64}$', text_input):
        show_custom_popup("Input Error", "Please enter a valid SHA-256 hash (64 hex).", "error")
        return

    is_threat, reasons, tld, vendors_rows = is_malicious(text_input, is_hash_scan=True)
    verdict = "Malicious" if is_threat else "Safe"

    open_result_html_dynamic(is_threat, text_input, reasons, tld, vendors_rows=vendors_rows)

    popup_msg = "\n".join(reasons) + "\n\n" + vendors_rows_to_text(vendors_rows)
    show_custom_popup("Hash Scan Results", popup_msg, "warning" if is_threat else "info")

    # ✅ ADDED: send email for hash scan also (uses same recipient field)
    recipient_email = email_entry.get().strip()
    if recipient_email:
        if not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", recipient_email):
            show_custom_popup("Invalid Email", "Only Gmail addresses are allowed.", "error")
            return

        send_email_report(recipient_email, f"Hash Scan Report - {verdict}", {
            "scan_type": "HASH",  # keeps your existing PDF "else" branch
            "input_value": text_input,
            "verdict": verdict,
            "detected_reasons": reasons,
            "tld": tld,
            "vendors_rows": vendors_rows,
            "report_text": (
                f"Scan Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Tool Version: 1.0.0\n"
                f"Detection Source: VirusTotal ONLY\n\n"
                f"Scanned Hash (SHA-256): {text_input}\n"
                f"Verdict: {verdict}\n\n"
                + "\n".join(f"- {r}" for r in reasons)
                + "\n\n"
                + vendors_rows_to_text(vendors_rows)
            )
        })


# =========================
# Background UI helpers
# =========================
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    r = int(lerp(r1, r2, t))
    g = int(lerp(g1, g2, t))
    b = int(lerp(b1, b2, t))
    return rgb_to_hex((r, g, b))

def draw_gradient(canvas_bg, w, h, c1, c2, steps=140):
    canvas_bg.delete("grad")
    for i in range(steps):
        t = i / max(1, steps - 1)
        col = lerp_color(c1, c2, t)
        y1 = int((h / steps) * i)
        y2 = int((h / steps) * (i + 1)) + 1
        canvas_bg.create_rectangle(0, y1, w, y2, outline="", fill=col, tags="grad")

def draw_glow_orbs(canvas_bg, w, h, tick):
    canvas_bg.delete("orbs")
    orbs = [
        (0.22 + 0.06 * math.sin(tick/32.0), 0.22 + 0.08 * math.cos(tick/45.0), 220, "#22c55e"),
        (0.75 + 0.07 * math.cos(tick/40.0), 0.30 + 0.06 * math.sin(tick/38.0), 260, "#38bdf8"),
        (0.55 + 0.08 * math.sin(tick/50.0), 0.78 + 0.07 * math.cos(tick/34.0), 300, "#a855f7"),
        (0.15 + 0.05 * math.cos(tick/28.0), 0.80 + 0.05 * math.sin(tick/26.0), 260, "#f97316"),
    ]
    for (px, py, size, color) in orbs:
        x = int(px * w)
        y = int(py * h)
        r = size
        for k in range(6, 0, -1):
            rr = int(r * (k / 6))
            canvas_bg.create_oval(x-rr, y-rr, x+rr, y+rr, outline="", fill=color, tags="orbs")

def set_status(text, kind="info"):
    colors_map = {"info": "#cbd5e1", "ok": "#22c55e", "warn": "#f59e0b", "error": "#ef4444"}
    status_label.config(text=text, fg=colors_map.get(kind, "#cbd5e1"))

def disable_actions(state=True):
    widgets = [btn_scan_url, btn_qr_img, btn_qr_cam, btn_scan_hash]
    for w in widgets:
        try:
            w.config(state=tk.DISABLED if state else tk.NORMAL)
        except Exception:
            pass

def run_with_loader(job_func, label_text="Scanning..."):
    disable_actions(True)
    set_status(label_text, "info")
    progress_bar.start(10)

    def worker():
        try:
            job_func()
        finally:
            root.after(0, done)

    def done():
        progress_bar.stop()
        disable_actions(False)
        set_status("Ready", "ok")

    threading.Thread(target=worker, daemon=True).start()

def make_hover(btn, normal_bg, hover_bg, normal_fg="white", hover_fg="white"):
    def on_enter(_=None):
        btn.config(bg=hover_bg, fg=hover_fg)
    def on_leave(_=None):
        btn.config(bg=normal_bg, fg=normal_fg)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

def pulse_title():
    global title_pulse_t
    title_pulse_t += 1
    t = (math.sin(title_pulse_t / 18.0) + 1) / 2
    color = lerp_color("#22c55e", "#a7f3d0", t)
    title_label.config(fg=color)
    root.after(50, pulse_title)

def animate_background():
    global bg_tick
    bg_tick += 1
    w = root.winfo_width()
    h = root.winfo_height()
    if w < 10 or h < 10:
        root.after(60, animate_background)
        return

    t = (math.sin(bg_tick / 60.0) + 1) / 2
    c1 = lerp_color("#05070f", "#0b1020", t)
    c2 = lerp_color("#0b1020", "#111827", 1 - t)
    draw_gradient(bg_canvas, w, h, c1, c2, steps=140)
    draw_glow_orbs(bg_canvas, w, h, bg_tick)

    root.after(60, animate_background)

def center_window(window, w=760, h=980):
    window.update_idletasks()
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    x = (sw // 2) - (w // 2)
    y = (sh // 2) - (h // 2)
    window.geometry(f"{w}x{h}+{x}+{y}")


# =========================
# INFO BUTTON ACTION
# =========================
def open_info_page():
    try:
        if not os.path.exists(INFO_HTML_PATH):
            show_custom_popup("Info", f"INFO file not found:\n{INFO_HTML_PATH}", "warning")
            return
        webbrowser.open_new_tab("file:///" + INFO_HTML_PATH.replace("\\", "/"))
    except Exception as e:
        show_custom_popup("Info Error", f"Could not open INFO page:\n{e}", "error")


# =========================
# GUI
# =========================
root = tk.Tk()
root.title("Malware Link Detection Tool")
center_window(root, 780, 900)
root.configure(bg="#05070f")
root.minsize(720, 850)

bg_canvas = tk.Canvas(root, highlightthickness=0, bd=0)
bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

outer = tk.Frame(root, bg="#05070f")
outer.place(relx=0.5, rely=0.5, anchor="center")

card = tk.Frame(outer, bg="#0b1020", highlightbackground="#1f2a44", highlightthickness=1)
card.pack(padx=18, pady=18)

header = tk.Frame(card, bg="#0b1020")
header.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 10))
header.grid_columnconfigure(0, weight=1)

title_label = tk.Label(
    header,
    text="🛡 Malware Link Detection Tool",
    font=("Segoe UI", 22, "bold"),
    fg="#22c55e",
    bg="#0b1020"
)
title_label.grid(row=0, column=0, pady=(0, 6))

subtitle = tk.Label(
    header,
    text="VirusTotal-only scan + Stylish HTML report",
    font=("Segoe UI", 11, "bold"),
    fg="#cbd5e1",
    bg="#0b1020"
)
subtitle.grid(row=1, column=0, pady=(0, 4))

divider = tk.Frame(card, bg="#1f2a44", height=1)
divider.grid(row=1, column=0, sticky="ew", padx=18)

body = tk.Frame(card, bg="#0b1020")
body.grid(row=2, column=0, padx=18, pady=18, sticky="nsew")
body.grid_columnconfigure(0, weight=1)

tk.Label(body, text="🔗 Enter URL", font=("Segoe UI", 12, "bold"), fg="#e5e7eb", bg="#0b1020").grid(row=0, column=0, sticky="w", pady=(0, 6))
url_entry = tk.Entry(body, width=60, font=("Segoe UI", 12), bg="#05070f", fg="#e5e7eb",
                     insertbackground="white", relief=tk.FLAT, highlightthickness=1, highlightbackground="#1f2a44")
url_entry.grid(row=1, column=0, sticky="ew", pady=(0, 12), ipady=6)

tk.Label(body, text="📧 Recipient Gmail (optional)", font=("Segoe UI", 12, "bold"), fg="#e5e7eb", bg="#0b1020").grid(row=2, column=0, sticky="w", pady=(0, 6))
email_entry = tk.Entry(body, width=60, font=("Segoe UI", 12), bg="#05070f", fg="#e5e7eb",
                       insertbackground="white", relief=tk.FLAT, highlightthickness=1, highlightbackground="#1f2a44")
email_entry.grid(row=3, column=0, sticky="ew", pady=(0, 12), ipady=6)

tk.Label(body, text="🔍 Enter SHA-256 hash (64 hex)", font=("Segoe UI", 12, "bold"), fg="#e5e7eb", bg="#0b1020").grid(row=4, column=0, sticky="w", pady=(0, 6))
hash_entry = tk.Entry(body, width=60, font=("Segoe UI", 12), bg="#05070f", fg="#e5e7eb",
                      insertbackground="white", relief=tk.FLAT, highlightthickness=1, highlightbackground="#1f2a44")
hash_entry.grid(row=5, column=0, sticky="ew", pady=(0, 14), ipady=6)

btn_scan_url = tk.Button(
    body, text="Scan URL", command=lambda: run_with_loader(scan_url, "Scanning URL..."),
    bg="#22c55e", fg="black", font=("Segoe UI", 11, "bold"),
    relief=tk.FLAT, padx=14, pady=10, cursor="hand2"
)
btn_scan_url.grid(row=6, column=0, sticky="ew", pady=(0, 10))

btn_qr_img = tk.Button(
    body, text="📷 Scan QR (Image)", command=lambda: run_with_loader(scan_qr_from_image, "Scanning QR (image)..."),
    bg="#2563eb", fg="white", font=("Segoe UI", 11, "bold"),
    relief=tk.FLAT, padx=14, pady=10, cursor="hand2"
)
btn_qr_img.grid(row=7, column=0, sticky="ew", pady=(0, 10))

btn_qr_cam = tk.Button(
    body, text="🎥 Scan QR (Camera)", command=lambda: run_with_loader(scan_qr_via_camera, "Opening camera..."),
    bg="#1d4ed8", fg="white", font=("Segoe UI", 11, "bold"),
    relief=tk.FLAT, padx=14, pady=10, cursor="hand2"
)
btn_qr_cam.grid(row=8, column=0, sticky="ew", pady=(0, 10))

btn_scan_hash = tk.Button(
    body, text="Scan Hash", command=lambda: run_with_loader(scan_hash, "Scanning hash..."),
    bg="#f59e0b", fg="black", font=("Segoe UI", 11, "bold"),
    relief=tk.FLAT, padx=14, pady=10, cursor="hand2"
)
btn_scan_hash.grid(row=9, column=0, sticky="ew", pady=(0, 6))

footer = tk.Frame(card, bg="#0b1020")
footer.grid(row=3, column=0, sticky="ew", padx=18, pady=(0, 16))
footer.grid_columnconfigure(0, weight=1)

progress_bar = ttk.Progressbar(footer, mode="indeterminate", length=260)
progress_bar.grid(row=0, column=0, sticky="w", pady=(6, 4))

status_label = tk.Label(footer, text="Ready", font=("Segoe UI", 10, "bold"), fg="#22c55e", bg="#0b1020")
status_label.grid(row=0, column=0, sticky="e", pady=(6, 4))

btn_info = tk.Button(
    footer, text="ℹ INFO", command=open_info_page,
    bg="#0ea5e9", fg="black", font=("Segoe UI", 10, "bold"),
    relief=tk.FLAT, padx=12, pady=6, cursor="hand2"
)
btn_info.grid(row=1, column=0, sticky="e", pady=(10, 0))

make_hover(btn_scan_url, "#22c55e", "#34d399", normal_fg="black", hover_fg="black")
make_hover(btn_qr_img, "#2563eb", "#3b82f6")
make_hover(btn_qr_cam, "#1d4ed8", "#2563eb")
make_hover(btn_scan_hash, "#f59e0b", "#fbbf24", normal_fg="black", hover_fg="black")
make_hover(btn_info, "#0ea5e9", "#38bdf8", normal_fg="black", hover_fg="black")

bg_tick = 0
title_pulse_t = 0
animate_background()
pulse_title()
set_status("Ready", "ok")

root.mainloop()