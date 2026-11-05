"""Build assets/header.svg: logo-trace name + scramble-text role lines (pure SVG/SMIL, no JS)."""
import random, sys
from xml.sax.saxutils import escape

random.seed(7)
W, H = 1000, 280
LINES = [
    "Senior Infrastructure Analyst",
    "Talos Kubernetes on a 6-node Proxmox lab",
    "Self-hosted AI: Ollama + ComfyUI on k8s",
    "Builder of tools for Plex, Pi-hole & n8n",
    "Streamer & Discord community host",
]
GLYPHS = "!<>-_\\/[]{}=+*^?#01ABCDEFXYZ$%&"
SLOT, FRAME, FRAMES = 3.2, 0.045, 16      # seconds per line, per scramble frame, frames per scramble
CYCLE = SLOT * len(LINES)
AMBER, DIM = "#ffb000", "#b07f1c"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "'Segoe UI',Inter,Helvetica,Arial,sans-serif"


def frame_text(line, k):
    reveal = int(len(line) * k / FRAMES)
    return "".join(c if i < reveal or c == " " else random.choice(GLYPHS) for i, c in enumerate(line))


def kt(t):
    return f"{t / CYCLE:.5f}"


texts = []
for li, line in enumerate(LINES):
    start = li * SLOT
    for k in range(FRAMES + 1):
        a = start + k * FRAME
        b = start + (k + 1) * FRAME if k < FRAMES else start + SLOT
        s = line if k == FRAMES else frame_text(line, k)
        fill = AMBER if k == FRAMES else DIM
        if b >= CYCLE - 1e-9:
            anim = f'values="0;1" keyTimes="0;{kt(a)}"'
        else:
            anim = f'values="0;1;0" keyTimes="0;{kt(a)};{kt(b)}"'
        texts.append(
            f'<text x="68" y="218" fill="{fill}" opacity="0">{escape(s)}'
            f'<animate attributeName="opacity" {anim} calcMode="discrete" dur="{CYCLE:.1f}s" repeatCount="indefinite"/></text>'
        )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="T13o - Senior Infrastructure Analyst, homelab and Kubernetes builder">
<defs>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="2" fill="#000" fill-opacity=".2"/>
  </pattern>
  <radialGradient id="vignette" cx=".5" cy=".5" r=".75">
    <stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".75"/>
  </radialGradient>
  <radialGradient id="bloom" cx=".22" cy=".5" r=".6">
    <stop offset="0" stop-color="{AMBER}" stop-opacity=".10"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
  </radialGradient>
  <filter id="glow" x="-20%" y="-40%" width="140%" height="180%">
    <feGaussianBlur stdDeviation="3" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="#0b0904"/>
<rect width="{W}" height="{H}" fill="url(#bloom)"/>

<g filter="url(#glow)">
  <animate attributeName="opacity" values="1;.94;1;1;.97;1" keyTimes="0;.02;.04;.6;.62;1" dur="5s" repeatCount="indefinite"/>
  <g font-family="{MONO}" font-size="14" fill="{DIM}" letter-spacing="1">
    <text x="40" y="42">T13O-OS 2.6 · TTY1</text>
    <text x="{W - 40}" y="42" text-anchor="end">HOMELAB ONLINE</text>
    <rect x="{W - 192}" y="31" width="9" height="13" fill="{AMBER}"><animate attributeName="opacity" values="1;.2;1" dur="2s" repeatCount="indefinite"/></rect>
    <path d="M40 58H{W - 40}" stroke="{DIM}" stroke-opacity=".5" stroke-dasharray="2 6"/>
  </g>

  <text x="36" y="160" font-family="{MONO}" font-size="120" font-weight="700"
        fill="{AMBER}" fill-opacity="0" stroke="{AMBER}" stroke-width="2" stroke-dasharray="1400" stroke-dashoffset="1400">T13o
    <animate attributeName="stroke-dashoffset" from="1400" to="0" begin="0.2s" dur="2.2s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".6 0 .2 1"/>
    <animate attributeName="fill-opacity" from="0" to="1" begin="2s" dur=".6s" fill="freeze"/>
  </text>
  <rect x="318" y="80" width="40" height="82" fill="{AMBER}" opacity="0">
    <animate attributeName="opacity" values="0;1;0" keyTimes="0;.5;1" calcMode="discrete" dur="1.1s" begin="2.4s" repeatCount="indefinite"/>
  </rect>

  <g font-family="{MONO}" font-size="15" letter-spacing="1">
    <text x="660" y="98" fill="{DIM}">K8S <tspan fill="{DIM}" fill-opacity=".5">..........</tspan> <tspan fill="{AMBER}">TALOS</tspan></text>
    <text x="660" y="124" fill="{DIM}">STORAGE <tspan fill="{DIM}" fill-opacity=".5">......</tspan> <tspan fill="{AMBER}">TRUENAS</tspan></text>
    <text x="660" y="150" fill="{DIM}">HYPERVISOR <tspan fill="{DIM}" fill-opacity=".5">...</tspan> <tspan fill="{AMBER}">PROXMOX</tspan></text>
    <text x="660" y="176" fill="{DIM}">LOCAL AI <tspan fill="{DIM}" fill-opacity=".5">.....</tspan> <tspan fill="{AMBER}">OLLAMA</tspan></text>
  </g>

  <g font-family="{MONO}" font-size="22">
    <text x="40" y="218" fill="{AMBER}">$</text>
    {"".join(texts)}
  </g>
</g>

<rect width="{W}" height="{H}" fill="url(#scan)"/>
<rect width="{W}" height="{H}" fill="url(#vignette)"/>
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="13.5" fill="none" stroke="{AMBER}" stroke-opacity=".35" stroke-width="1.5"/>
</svg>
'''
open(sys.argv[1], "w", encoding="utf-8").write(svg)

# self-check: final frame of every line is the real line, scramble keeps length
assert all(len(frame_text(l, k)) == len(l) for l in LINES for k in range(FRAMES))
assert frame_text(LINES[0], FRAMES) == LINES[0]
print("ok", len(texts), "frames,", len(svg), "bytes")
