"""
Generates on-brand placeholder art so the app runs out of the box.
Replace these with real photography before going live —
run once with: python static/images/generate_placeholders.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

INK = (23, 50, 44)
PAPER = (238, 239, 231)
BRICK = (181, 72, 45)
OCHRE = (201, 162, 39)
LINE = (201, 204, 192)

HERE = os.path.dirname(os.path.abspath(__file__))

def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def grid(draw, w, h, step, color, offset=0):
    for x in range(0, w, step):
        draw.line([(x, 0), (x, h)], fill=color, width=1)
    for y in range(0, h, step):
        draw.line([(0, y), (w, y)], fill=color, width=1)

def make_logo():
    size = 256
    img = Image.new("RGB", (size, size), PAPER)
    d = ImageDraw.Draw(img)
    pad = 40
    cell = (size - pad * 2 - 8) // 2
    coords = [
        (pad, pad, BRICK),
        (pad + cell + 8, pad, INK),
        (pad, pad + cell + 8, INK),
        (pad + cell + 8, pad + cell + 8, INK),
    ]
    for x, y, c in coords:
        d.rectangle([x, y, x + cell, y + cell], fill=c)
    img.save(os.path.join(HERE, "logo.png"))

def make_hero():
    w, h = 1200, 1500
    img = Image.new("RGB", (w, h), INK)
    d = ImageDraw.Draw(img)
    grid(d, w, h, 60, (35, 68, 61))
    # simple abstracted skyline / balcony blocks
    for i, (x, bw, bh) in enumerate([(80, 220, 900), (340, 260, 1100), (640, 200, 800), (880, 260, 1000)]):
        color = BRICK if i % 3 == 0 else (44, 82, 74)
        d.rectangle([x, h - bh, x + bw, h], fill=color)
        for wy in range(h - bh + 40, h - 20, 90):
            for wx in range(x + 20, x + bw - 20, 70):
                d.rectangle([wx, wy, wx + 40, wy + 55], fill=OCHRE if (wx + wy) % 3 == 0 else PAPER)
    d.rectangle([0, 0, w, 90], fill=INK)
    f = font(28, bold=True)
    d.text((40, 30), "TOLET EARTH — SEC 35-A, CHANDIGARH", font=f, fill=PAPER)
    img.save(os.path.join(HERE, "hero.jpg"), quality=88)

def make_property(name, sector, city, seed_color):
    w, h = 900, 700
    img = Image.new("RGB", (w, h), seed_color)
    d = ImageDraw.Draw(img)
    grid(d, w, h, 50, tuple(min(c + 20, 255) for c in seed_color))
    d.rectangle([0, h - 140, w, h], fill=INK)
    f_big = font(46, bold=True)
    f_small = font(24)
    d.text((30, h - 120), sector, font=f_big, fill=PAPER)
    d.text((30, h - 55), city, font=f_small, fill=OCHRE)
    img.save(os.path.join(HERE, "properties", f"{name}.jpg"), quality=88)

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "properties"), exist_ok=True)
    make_logo()
    make_hero()
    sets = [
        ("1", "SECTOR 70", "MOHALI", (74, 96, 88)),
        ("2", "SECTOR 11", "CHANDIGARH", (120, 84, 60)),
        ("3", "SECTOR 20", "PANCHKULA", (58, 78, 92)),
        ("4", "AEROCITY", "MOHALI", (92, 70, 90)),
        ("5", "SECTOR 22", "CHANDIGARH", (70, 90, 70)),
        ("6", "SECTOR 8", "PANCHKULA", (100, 76, 58)),
    ]
    for name, sector, city, color in sets:
        make_property(name, sector, city, color)
    print("Placeholders generated.")
