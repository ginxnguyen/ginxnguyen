import json
from datetime import date

data = json.load(open("data/contributions.json"))
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
CELL, GAP, PAD_X, PAD_Y = 12, 3, 10, 30

days = data["days"]
first = date.fromisoformat(days[0]["date"])
offset = (first.weekday() + 1) % 7          # Chủ nhật = 0

rects = []
for d in days:
    idx = (date.fromisoformat(d["date"]) - first).days + offset
    x = PAD_X + (idx // 7) * (CELL + GAP)
    y = PAD_Y + (idx % 7) * (CELL + GAP)
    color = PALETTE[min(d["level"], 4)]
    rects.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{color}"/>')

width = PAD_X * 2 + 54 * (CELL + GAP)
height = PAD_Y + 7 * (CELL + GAP) + 30
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="#0d1117" rx="8"/>
<text x="{PAD_X}" y="20" fill="#c9d1d9" font-family="monospace" font-size="12">{data["total"]} contributions in the last year</text>
{chr(10).join(rects)}
</svg>'''
open("contrib-heatmap.svg", "w").write(svg)