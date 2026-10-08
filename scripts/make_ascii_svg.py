import sys
from PIL import Image

RAMP = " .`:-=+*cs#%@"          # sáng (thưa) -> tối (dày)
W = 100
path = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
img = Image.open(path).convert("L")
H = int(img.height / img.width * W * 0.5)   # 0.5 vì ký tự cao hơn rộng
img = img.resize((W, H))

lines = []
for y in range(H):
    row = "".join(RAMP[(255 - img.getpixel((x, y))) * (len(RAMP) - 1) // 255] for x in range(W))
    lines.append(row)

FS = 8
texts = "\n".join(
    f'<text x="5" y="{10 + i * FS}" xml:space="preserve">{line}</text>'
    for i, line in enumerate(lines)
)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{int(W * FS * 0.6) + 10}" height="{H * FS + 15}">
<g font-family="monospace" font-size="{FS}" fill="#c9d1d9">
{texts}
</g></svg>'''
open("portrait-ascii.svg", "w").write(svg)
print("Wrote portrait-ascii.svg")
