import json
from datetime import date
from math import ceil

data = json.load(open("data/contributions.json"))
days = data["days"]

PALETTE = ["#161b22", "#0e4429", "#006d32",
           "#26a641", "#39d353", "#69f0a0"]
#          none -> brightest (level 5 is a neon top end)
CELL, GAP = 12, 3
STEP = CELL + GAP
LEFT, TOP = 36, 56

first = date.fromisoformat(days[0]["date"])
offset = (first.weekday() + 1) % 7            # Sunday = 0
weeks = ceil((offset + len(days)) / 7)
W = LEFT + weeks * STEP + 20
H = TOP + 7 * STEP + 64
max_count = max(d["count"] for d in days) or 1


def level(d):
    lv = d["level"]
    if lv >= 4 and d["count"] >= 0.75 * max_count:
        lv = 5                                  # neon top end
    return min(lv, 5)


rects, first_in_col = [], {}
for d in days:
    dt = date.fromisoformat(d["date"])
    col, row = divmod((dt - first).days + offset, 7)
    first_in_col.setdefault(col, dt)
    x, y = LEFT + col * STEP, TOP + row * STEP
    delay = (col + row) * 0.02                  # diagonal, line-after-line
    rects.append(
        f'<rect class="d" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" '
        f'fill="{PALETTE[level(d)]}" style="animation-delay:{delay:.2f}s"/>'
    )

labels, prev = [], None
for col in sorted(first_in_col):
    m = first_in_col[col].month
    if m != prev:
        labels.append((col, first_in_col[col].strftime("%b")))
        prev = m
if len(labels) > 1 and labels[1][0] - labels[0][0] < 3:
    labels.pop(0)

STYLE = ("@keyframes drop{from{opacity:0;transform:translateY(-10px)}"
         "to{opacity:1;transform:translateY(0)}}"
         ".d{opacity:0;animation:drop .5s ease-out forwards}"
         "text{font-family:ui-monospace,Menlo,Consolas,monospace;fill:#8b949e}")

p = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    f'<style>{STYLE}</style>',
    f'<rect width="100%" height="100%" rx="10" fill="#0d1117" stroke="#30363d"/>',
    f'<text x="{LEFT}" y="26" style="font-size:13px;fill:#c9d1d9">{data["user"]} · contribution graph</text>',
]
for col, name in labels:
    p.append(f'<text x="{LEFT + col * STEP}" y="{TOP - 8}" style="font-size:10px">{name}</text>')
for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    p.append(f'<text x="6" y="{TOP + row * STEP + 10}" style="font-size:9px">{name}</text>')
p += rects

# legend: Less -> More
ly = TOP + 7 * STEP + 14
lx = W - 20 - (6 * STEP + 62)
p.append(f'<text x="{lx}" y="{ly + 10}" style="font-size:10px">Less</text>')
for i, c in enumerate(PALETTE):
    p.append(f'<rect x="{lx + 30 + i * STEP}" y="{ly}" width="{CELL}" height="{CELL}" rx="2" fill="{c}"/>')
p.append(f'<text x="{lx + 30 + 6 * STEP + 4}" y="{ly + 10}" style="font-size:10px">More</text>')

# stats footer
b = data["best_day"]
p.append(
    f'<text x="{LEFT}" y="{H - 16}" style="font-size:11px">'
    f'{data["total"]:,} contributions in the last year  ·  current streak {data["current_streak"]}d'
    f'  ·  longest {data["longest_streak"]}d  ·  best day {b["count"]} ({b["date"]})</text>'
)
p.append("</svg>")

open("contrib-heatmap.svg", "w").write("\n".join(p))
print("Wrote contrib-heatmap.svg")
