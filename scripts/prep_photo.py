"""
Prepare a portrait photo for clean ASCII conversion:
  1. composite transparent PNG onto white background
  2. boost LOCAL contrast (CLAHE) so a flatly-lit face gains highlights and
     shadows
  3. output grayscale PNG

Foto udah no-background (PNG with transparency), jadi skip rembg.
Output: source-prepped.png, consumed by make_ascii_svg.py.

    python scripts/prep_photo.py <input.png> [output.png]
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

# 1. open PNG with transparency, composite onto white
img = Image.open(INP).convert("RGBA")
bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
composite = Image.alpha_composite(bg, img)
rgb = np.array(composite.convert("RGB"))

# 2. local-contrast the luminance (CLAHE)
gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.6, tileGridSize=(8, 8))
gray = clahe.apply(gray)

# a touch of global lift so the face sits in the sparse end of the ramp
gray = cv2.convertScaleAbs(gray, alpha=1.05, beta=18)

# 3. save as grayscale
Image.fromarray(gray, mode="L").save(OUT)
print("wrote", OUT, gray.shape)
