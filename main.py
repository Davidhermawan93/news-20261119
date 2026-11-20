#!/usr/bin/env python3
"""Deterministic 1024x1024 PNG: front page of the world's news, 19 November 2026.
No network: everything is drawn from constants with PIL."""
from PIL import Image, ImageDraw, ImageFont
import hashlib
import sys

W = H = 1024
DARK = (16, 18, 24)
PAPER = (238, 234, 224)

FDIR = "/usr/share/fonts/truetype/dejavu/"

def font(size, bold=True, serif=True):
    f = "DejaVuSerif-Bold.ttf" if (bold and serif) else ("DejaVuSerif.ttf" if serif else ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"))
    return ImageFont.truetype(FDIR + f, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# masthead
d.rectangle([0, 0, W, 112], fill=DARK)
ct = font(42)
d.text((W // 2, 22), "THE WORLD IN ONE DAY", fill=(238, 234, 224), font=ct, anchor="ma")
d.text((W // 2, 76), "Thursday, 19 November 2026", fill=(160, 170, 190), font=font(21, bold=False, serif=False), anchor="ma")

panels = [
    ((214, 60, 48), (255, 255, 255), ["TRILATERAL", "TALKS", "SHENZHEN"],
     "Trump, Putin and Xi meet at APEC: nuclear-risk talks pledged, Ukraine unmentioned"),
    ((30, 50, 90), (255, 255, 255), ["STRIKE HITS", "RIYADH", "TOWER"],
     "Houthi projectile hits PIF tower; IEA: Hormuz oil reliance to be slashed"),
    ((222, 178, 44), (20, 20, 20), ["FRANCE'S", "'VOLIA'", "IN UKRAINE"],
     "Secret training mission admitted; Lavrov: 'direct participation'"),
    ((40, 110, 70), (255, 255, 255), ["OIL SLIDES", "TO $92", "DESPITE WAR"],
     "Brent falls as US crude stocks jump; surplus priced in over risk premium"),
    ((120, 40, 100), (255, 255, 255), ["EU LOANS", "45 BILLION", "TO KYIV"],
     "Interest paid by EU budget; repayment only when Russia pays reparations"),
    ((70, 70, 70), (255, 255, 255), ["BOAT SINKS", "OFF", "SENEGAL"],
     "Dozens missing en route to Spain; 11,000+ reached Canaries in two weeks"),
]
pw, ph, gap = 320, 418, 14
x0 = (W - 3 * pw - 2 * gap) // 2
y0 = 140

for i, (bg, fg, head, sub) in enumerate(panels):
    px = x0 + (i % 3) * (pw + gap)
    py = y0 + (i // 3) * (ph + gap)
    d.rectangle([px, py, px + pw, py + ph], fill=bg)
    d.rectangle([px, py, px + pw, py + 8], fill=fg)
    # auto-fit headline font size
    size = 40
    f = font(18)
    while size > 18:
        f = font(size)
        if all(d.textlength(line, font=f) <= pw - 28 for line in head):
            break
        size -= 2
    yy = py + 30
    for line in head:
        d.text((px + pw // 2, yy), line, fill=fg, font=f, anchor="ma")
        yy += size + 10
    # wrap sub
    fs = font(19, bold=False, serif=False)
    words = sub.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fs) > pw - 32:
            lines.append(cur); cur = w
        else:
            cur = t
    lines.append(cur)
    yy += 6
    for line in lines:
        d.text((px + pw // 2, yy), line, fill=fg, font=fs, anchor="ma")
        yy += 25

# footer
d.rectangle([0, H - 64, W, H], fill=DARK)
d.text((W // 2, H - 32), "ONE PAGE  ·  SIX STORIES  ·  19.11.2026", fill=(160, 170, 190), font=font(21, bold=False, serif=False), anchor="mm")

out = sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png"
img.save(out, "PNG", optimize=True)
print("wrote", out, "sha256", hashlib.sha256(open(out, "rb").read()).hexdigest()[:16])
