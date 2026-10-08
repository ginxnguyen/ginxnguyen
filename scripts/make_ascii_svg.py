import sys
from html import escape
from PIL import Image

RAMP = " .`:-=+*cs#%@"   # bright (sparse) -> dark (dense)
#        ^ leading space clears the background to nothing

COLS = 100
FS, CW, LH = 8, 4.8, 9          # font size, char width, line height
PAD = 10
COLOR = "#c9d1d9"               # one light-gray fill
STAGGER, DUR = 0.06, 0.9        # seconds

src = sys.argv[1] if len(sys.argv) > 1 else "source-prepped.png"
out = sys.argv[2] if len(sys.argv) > 2 else "ginxnguyen-ascii.svg"

img = Image.open(src).convert("L")
rows = max(1, round(img.height / img.width * COLS * CW / LH))
img = img.resize((COLS, rows), Image.LANCZOS)
px = img.load()

n = len(RAMP) - 1
lines = []
for y in range(rows):
    lines.append("".join(RAMP[(255 - px[x, y]) * n // 255] for x in range(COLS)))

GW = COLS * CW
W, H = GW + 2 * PAD, rows * LH + 2 * PAD

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}">',
    f'<rect width="100%" height="100%" fill="#0d1117" rx="10"/>',
    f'<g font-family="ui-monospace,Menlo,Consolas,monospace" font-size="{FS}" fill="{COLOR}">',
]
for r, line in enumerate(lines):
    top = PAD + r * LH
    b = r * STAGGER
    parts.append(
        f'<clipPath id="c{r}"><rect x="{PAD}" y="{top}" width="0" height="{LH}">'
        f'<animate attributeName="width" from="0" to="{GW:.1f}" begin="{b:.2f}s" dur="{DUR}s" fill="freeze"/>'
        f'</rect></clipPath>'
    )
    parts.append(
        f'<text x="{PAD}" y="{top + FS}" textLength="{GW:.1f}" lengthAdjust="spacing" '
        f'clip-path="url(#c{r})" xml:space="preserve">{escape(line)}</text>'
    )
    parts.append(
        f'<rect x="{PAD}" y="{top}" width="{CW}" height="{LH - 1}" opacity="0">'
        f'<set attributeName="opacity" to="1" begin="{b:.2f}s"/>'
        f'<animate attributeName="x" from="{PAD}" to="{PAD + GW:.1f}" begin="{b:.2f}s" dur="{DUR}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0" begin="{b + DUR:.2f}s"/>'
        f'</rect>'
    )
parts.append("</g></svg>")

open(out, "w").write("\n".join(parts))
print("Wrote", out, f"({COLS}x{rows} chars)")
