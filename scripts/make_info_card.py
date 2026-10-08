import os
from html import escape

STATIC = os.environ.get("STATIC") == "1"
USER = "ginxnguyen"

# ---- EDIT YOUR STORY HERE (keep each line under ~46 chars) ----
ROWS = [
    ("Now", "#ff7b72", ["Data Scientist · NLP & AI research",
                        "Socioeconomic Statistics @ UE-UDN"]),
    ("Stack", "#7ee787", ["Python · SQL · Power BI "]),
    ("Highlights", "#d2a8ff", ["BERTopic · 6 languages · Da Nang/Hoi An",
                               "ABSA with local LLMs",
                               "Vietnamese medical NER + ICD-10 linking"]),
]

# ----------------------------------------------------------------

W, LINE = 490, 22
BG, BORDER, BAR, FG = "#0d1117", "#30363d", "#161b22", "#c9d1d9"

items = [("", "#58a6ff", f"{USER}@github"), ("", BORDER, "-" * (len(USER) + 7))]
for key, color, texts in ROWS:
    for i, t in enumerate(texts):
        items.append((f"{key}:" if i == 0 else "", color, t))

H = 64 + len(items) * LINE + 16

css = ("text{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px}"
       ".k{font-weight:bold}")
css += (".l{opacity:1}" if STATIC else
        ".l{opacity:0;animation:in .45s ease-out forwards}"
        "@keyframes in{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:translateX(0)}}")

p = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    f'<style>{css}</style>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
    f'<rect x="1" y="1" width="{W-2}" height="31" rx="9" fill="{BAR}"/>',
    f'<rect x="1" y="20" width="{W-2}" height="12" fill="{BAR}"/>',
    '<circle cx="18" cy="16" r="6" fill="#ff5f56"/>',
    '<circle cx="38" cy="16" r="6" fill="#ffbd2e"/>',
    '<circle cx="58" cy="16" r="6" fill="#27c93f"/>',
    f'<text x="{W/2}" y="20" text-anchor="middle" fill="#8b949e" style="font-size:12px">neofetch</text>',
]
for i, (key, color, text) in enumerate(items):
    y = 64 + i * LINE
    p.append(
        f'<g class="l" style="animation-delay:{i * 0.18:.2f}s">'
        f'<text class="k" x="24" y="{y}" fill="{color}">{escape(key)}</text>'
        f'<text x="130" y="{y}" fill="{color if key == "" else FG}">{escape(text)}</text></g>'
        if key == "" and i < 2 else
        f'<g class="l" style="animation-delay:{i * 0.18:.2f}s">'
        f'<text class="k" x="24" y="{y}" fill="{color}">{escape(key)}</text>'
        f'<text x="130" y="{y}" fill="{FG}">{escape(text)}</text></g>'
    )
p.append("</svg>")

open("info-card.svg", "w").write("\n".join(p))
print("Wrote info-card.svg")
