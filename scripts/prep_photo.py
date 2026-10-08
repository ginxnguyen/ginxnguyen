import sys
import cv2
import numpy as np
from PIL import Image

src = sys.argv[1] if len(sys.argv) > 1 else "photo.jpg"
dst = "source-prepped.png"

img = Image.open(src).convert("RGB")
img.thumbnail((1200, 1200))

# 1) remove background
try:
    from rembg import remove
    rgba = remove(img)
except ImportError:
    print("rembg not installed - skipping background removal")
    rgba = img.convert("RGBA")

rgba = np.array(rgba.convert("RGBA"))
rgb = rgba[..., :3]
alpha = rgba[..., 3].astype(np.float32) / 255.0

# 2) CLAHE: local contrast boost on the grayscale face
gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
gray = clahe.apply(gray)

# 3) composite onto pure white (background -> blank end of the ramp)
out = (gray * alpha + 255 * (1 - alpha)).astype(np.uint8)

# crop to the subject with a small margin
ys, xs = np.where(alpha > 0.5)
if len(xs):
    m = int(0.05 * max(out.shape))
    y0, y1 = max(ys.min() - m, 0), min(ys.max() + m, out.shape[0])
    x0, x1 = max(xs.min() - m, 0), min(xs.max() + m, out.shape[1])
    out = out[y0:y1, x0:x1]

Image.fromarray(out).save(dst)
print("Wrote", dst)
