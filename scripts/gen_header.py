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
        fill = "#f5f5f7" if k == FRAMES else "#ff69b4"
        if b >= CYCLE - 1e-9:
            anim = f'values="0;1" keyTimes="0;{kt(a)}"'
        else:
            anim = f'values="0;1;0" keyTimes="0;{kt(a)};{kt(b)}"'
        texts.append(
            f'<text x="72" y="214" fill="{fill}" opacity="0">{escape(s)}'
            f'<animate attributeName="opacity" {anim} calcMode="discrete" dur="{CYCLE:.1f}s" repeatCount="indefinite"/></text>'
        )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="TheInfamousToTo - Senior Infrastructure Analyst, homelab and Kubernetes builder">
<defs>
  <linearGradient id="foil" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
    <stop offset="0" stop-color="#ff69b4"/><stop offset=".35" stop-color="#c084fc"/>
    <stop offset=".65" stop-color="#67e8f9"/><stop offset="1" stop-color="#ff69b4"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;0 0;-1 0" dur="8s" repeatCount="indefinite"/>
  </linearGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="#ffffff" stroke-opacity=".035"/>
  </pattern>
  <radialGradient id="glow" cx=".18" cy=".1" r=".9">
    <stop offset="0" stop-color="#ff69b4" stop-opacity=".22"/><stop offset="1" stop-color="#ff69b4" stop-opacity="0"/>
  </radialGradient>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="#0d0b12"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#grid)"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#glow)"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" fill="none" stroke="#ff69b4" stroke-opacity=".25"/>

<g font-family="{MONO}" font-size="14" fill="#8b8597">
  <circle cx="34" cy="34" r="5" fill="#ff5f57"/><circle cx="52" cy="34" r="5" fill="#febc2e"/><circle cx="70" cy="34" r="5" fill="#28c840"/>
  <text x="94" y="39">~/github/theinfamoustoto</text>
  <text x="{W - 40}" y="39" text-anchor="end">homelab · online</text>
  <circle cx="{W - 170}" cy="34" r="4" fill="#28c840"><animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>
</g>

<text x="70" y="148" font-family="{SANS}" font-size="78" font-weight="800" letter-spacing="-1.5"
      fill="url(#foil)" fill-opacity="0" stroke="#ff69b4" stroke-width="1.4" stroke-dasharray="900" stroke-dashoffset="900">TheInfamousToTo
  <animate attributeName="stroke-dashoffset" from="900" to="0" begin="0.2s" dur="2.4s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".6 0 .2 1"/>
  <animate attributeName="fill-opacity" from="0" to="1" begin="2.2s" dur=".9s" fill="freeze"/>
  <animate attributeName="stroke-opacity" from="1" to="0" begin="2.6s" dur=".8s" fill="freeze"/>
</text>

<g font-family="{MONO}" font-size="22">
  <text x="44" y="214" fill="#ff69b4">&gt;</text>
  {"".join(texts)}
</g>
</svg>
'''
open(sys.argv[1], "w", encoding="utf-8").write(svg)

# self-check: final frame of every line is the real line, scramble keeps length
assert all(len(frame_text(l, k)) == len(l) for l in LINES for k in range(FRAMES))
assert frame_text(LINES[0], FRAMES) == LINES[0]
print("ok", len(texts), "frames,", len(svg), "bytes")
