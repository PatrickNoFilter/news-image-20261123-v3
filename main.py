#!/usr/bin/env python3
"""Deterministic generator for the 23 November 2026 one-image news summary."""
import os
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = "#0D1426"
CARD = "#18233D"
BORDER = "#2B3A5C"
WHITE = "#F6F8FC"
MUTED = "#A9B6D0"
AMBER = "#F3B64B"

# One palette, used by cards, stats, bullets and the key so a colour always
# means the same thing wherever it appears in the image.
CLIMATE = "#E8B24C"
CONFLICT = "#E46965"
EUROPE = "#8E9BF6"
AMERICAS = "#6BCB9A"
ASIA = "#4FC3D9"
AFRICA = "#D98CB3"
SCIENCE = "#63C7B2"
CULTURE = "#C792EA"

FONTS = {
    "regular": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
}


def font(size, bold=False):
    return ImageFont.truetype(FONTS["bold"] if bold else FONTS["regular"], size)


def text(d, xy, s, size, color=WHITE, bold=False, anchor=None):
    d.text(xy, s, font=font(size, bold), fill=color, anchor=anchor)


def wrap(d, s, size, max_width, bold=False):
    f = font(size, bold)
    lines, line = [], ""
    for word in s.split():
        trial = (line + " " + word).strip()
        if d.textlength(trial, font=f) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return "\n".join(lines)


def multiline(d, xy, s, size, color=WHITE, bold=False, spacing=2):
    x, y = xy
    for line in s.split("\n"):
        d.text((x, y), line, font=font(size, bold), fill=color)
        y += size + spacing
    return y


def panel(d, box, accent=None, radius=11):
    d.rounded_rectangle(box, radius=radius, fill=CARD, outline=BORDER, width=2)
    if accent:
        x0, y0, x1, y1 = box
        d.rounded_rectangle((x0, y0 + 3, x0 + 6, y1 - 3), radius=3, fill=accent)


def icon(img, cx, cy, kind, color, size=38):
    """Small unambiguous line icons, drawn on a temp layer then scaled."""
    S = 90
    tmp = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    c = S // 2
    if kind == "drones":
        for dx, dy in ((-18, -6), (16, -14), (0, 14)):
            x, y = c + dx, c + dy
            d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=color)
            d.line((x - 13, y - 13, x - 6, y - 6), fill=color, width=3)
            d.line((x + 6, y - 6, x + 13, y - 13), fill=color, width=3)
        d.line((c - 26, c + 26, c + 26, c + 26), fill=color, width=4)
    elif kind == "gavel":
        d.line((c - 22, c + 22, c + 14, c - 18), fill=color, width=12)
        d.rectangle((c + 2, c - 30, c + 30, c - 8), outline=color, width=4)
        d.line((c - 28, c + 28, c + 28, c + 28), fill=color, width=5)
    elif kind == "house":
        d.polygon([(c - 28, c - 2), (c, c - 28), (c + 28, c - 2)], fill=color)
        d.rectangle((c - 22, c - 2, c + 22, c + 26), outline=color, width=4)
        d.line((c, c + 26, c, c + 2), fill=color, width=3)
    elif kind == "plane":
        d.line((c - 30, c + 12, c + 28, c - 14), fill=color, width=6)
        d.line((c - 8, c + 2, c - 20, c - 22), fill=color, width=5)
        d.line((c + 14, c - 6, c + 4, c - 28), fill=color, width=5)
    elif kind == "ship":
        d.polygon([(c - 32, c + 4), (c + 32, c + 4), (c + 22, c + 24), (c - 22, c + 24)], outline=color)
        d.rectangle((c - 6, c - 22, c + 16, c + 4), fill=color)
        d.line((c - 36, c + 30, c + 36, c + 30), fill=color, width=3)
    elif kind == "exam":
        d.rectangle((c - 20, c - 26, c + 20, c + 24), outline=color, width=4)
        for i in range(3):
            d.line((c - 12, c - 14 + i * 13, c + 10, c - 14 + i * 13), fill=color, width=3)
    elif kind == "rings":
        d.ellipse((c - 26, c - 14, c + 4, c + 16), outline=color, width=5)
        d.ellipse((c - 4, c - 14, c + 26, c + 16), outline=color, width=5)
    elif kind == "blast":
        d.ellipse((c - 20, c - 20, c + 20, c + 20), outline=color, width=4)
        for a in range(0, 360, 45):
            r = math.radians(a)
            d.line((c + 24 * math.cos(r), c + 24 * math.sin(r),
                    c + 34 * math.cos(r), c + 34 * math.sin(r)), fill=color, width=4)
    elif kind == "boat":
        d.polygon([(c - 30, c + 2), (c + 30, c + 2), (c + 18, c + 22), (c - 18, c + 22)], outline=color)
        d.line((c, c + 2, c, c - 24), fill=color, width=4)
        d.polygon([(c + 2, c - 22), (c + 24, c - 8), (c + 2, c - 2)], fill=color)
    elif kind == "space":
        d.ellipse((c - 16, c - 16, c + 16, c + 16), outline=color, width=4)
        d.line((c - 30, c, c - 16, c), fill=color, width=4)
        d.line((c + 16, c, c + 30, c), fill=color, width=4)
    elif kind == "book":
        d.polygon([(c - 28, c - 20), (c - 2, c - 10), (c - 2, c + 24), (c - 28, c + 14)], outline=color)
        d.polygon([(c + 28, c - 20), (c + 2, c - 10), (c + 2, c + 24), (c + 28, c + 14)], outline=color)
    elif kind == "protest":
        d.line((c - 18, c + 24, c - 18, c - 14), fill=color, width=5)
        d.rectangle((c - 22, c - 32, c + 18, c - 14), fill=color)
    elif kind == "ufo":
        d.ellipse((c - 32, c - 10, c + 32, c + 8), outline=color, width=4)
        d.ellipse((c - 14, c - 24, c + 14, c - 6), outline=color, width=4)
    elif kind == "virus":
        d.ellipse((c - 14, c - 14, c + 14, c + 14), outline=color, width=4)
        for a in range(0, 360, 60):
            r = math.radians(a)
            d.line((c + 16 * math.cos(r), c + 16 * math.sin(r),
                    c + 26 * math.cos(r), c + 26 * math.sin(r)), fill=color, width=3)
    elif kind == "globe":
        d.ellipse((c - 24, c - 24, c + 24, c + 24), outline=color, width=4)
        d.line((c - 24, c, c + 24, c), fill=color, width=3)
        d.ellipse((c - 11, c - 24, c + 11, c + 24), outline=color, width=3)
    tmp = tmp.resize((size, size), Image.LANCZOS)
    img.paste(tmp, (int(cx - size / 2), int(cy - size / 2)), tmp)


HEROES = [
    ("CLIMATE", "COP31 ends with no deal", "Longest UN climate summit, Antalya", CLIMATE, "gavel"),
    ("UKRAINE", "Dnipro strike kills 11", "Boy, 7, pulled alive from rubble", CONFLICT, "drones"),
    ("US POLITICS", "Democrats win the House", "258 seats, best since 1992", AMERICAS, "house"),
]

GRID = [
    ("EUROPE", "Belgium flights grounded", "Strike against austerity measures", EUROPE, "plane"),
    ("BALTIC", "Ship attacked in Gulf of Finland", "Ukraine likely behind drone strike", CONFLICT, "ship"),
    ("ASIA", "Korea exam chief resigns", "Chaos over AI-cheating measures", ASIA, "exam"),
    ("CULTURE", "Miley Cyrus marries Maxx Morando", "California ceremony, four years together", CULTURE, "rings"),
    ("US", "Iowa explosives to be detonated", "Army defies court order", AMERICAS, "blast"),
    ("AFRICA", "Nigeria boat tragedy rescue race", "Overcrowding and missing life jackets", AFRICA, "boat"),
    ("SCIENCE", "Mercury gets first visitors", "Two spacecraft enter orbit", SCIENCE, "space"),
    ("CULTURE", "Ancient library opens in Rome", "Restored after years of work", CULTURE, "book"),
]

# Each stat is tied to a real story and carries that story's accent colour.
STATS = [
    ("11", "killed in Dnipro strike", CONFLICT),
    ("258", "House seats won", AMERICAS),
    ("2", "spacecraft at Mercury", SCIENCE),
    ("19", "stories in one image", CLIMATE),
]

# Bullet colour follows the same key as the cards above.
MORE = [
    (EUROPE, "Street protests over reforms — Macron blames the radical left"),
    (AMERICAS, "More UFO footage declassified — eighth tranche includes three videos"),
    (CLIMATE, "Anthropic record IPO — charities prepare for windfall"),
    (CONFLICT, "Virginia reports measles death — first young child death in 2026"),
    (AMERICAS, "Carney jokes at press dinner — fake Trump draws laughs"),
    (AMERICAS, "Two passengers detained by ICE — family baptism trip, lawyer says"),
    (CULTURE, "NFL analyst Tom Jackson dies — Broncos star and analyst was 75"),
    (AFRICA, "Kenya, DR Congo restore ties — leaders pledge non-interference"),
]

KEY = [
    ("CLIMATE / MARKETS", CLIMATE),
    ("UKRAINE / BALTIC", CONFLICT),
    ("EUROPE", EUROPE),
    ("AMERICAS", AMERICAS),
    ("ASIA / PACIFIC", ASIA),
    ("AFRICA", AFRICA),
    ("SCIENCE", SCIENCE),
    ("CULTURE / SPORT", CULTURE),
]


def build():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.rectangle((0, 0, W, 7), fill=AMBER)
    text(d, (40, 22), "THE WORLD IN ONE IMAGE  ·  MONDAY EDITION", 15, MUTED, True)
    text(d, (38, 44), "23 NOVEMBER 2026", 54, WHITE, True)
    text(d, (984, 56), "ONE DAY  ·  ONE IMAGE", 14, MUTED, False, "ra")
    d.line((40, 116, 984, 116), fill=BORDER, width=3)

    cw, gap = 312, 12
    for i, (tag, head, sub, col, ico) in enumerate(HEROES):
        x = 40 + i * (cw + gap)
        panel(d, (x, 130, x + cw, 298), col)
        d.rectangle((x + 1, 131, x + cw - 1, 137), fill=col)
        text(d, (x + 18, 148), tag, 15, col, True)
        icon(img, x + cw - 34, 162, ico, col, 28)
        wrapped = wrap(d, head, 23, cw - 36, True)
        multiline(d, (x + 18, 180), wrapped, 23, WHITE, True, 1)
        text(d, (x + 18, 252), sub, 13, MUTED)

    sw = (944 - 3 * 10) // 4
    for i, (num, lab, col) in enumerate(STATS):
        x = 40 + i * (sw + 10)
        panel(d, (x, 310, x + sw, 368), col, radius=10)
        text(d, (x + 16, 320), num, 28, col, True)
        text(d, (x + 16, 351), lab, 13, MUTED)

    gx0, gy0, gw, gh, vgap = 40, 382, 462, 80, 8
    for i, (tag, head, sub, col, ico) in enumerate(GRID):
        x = gx0 + (i % 2) * (gw + 20)
        y = gy0 + (i // 2) * (gh + vgap)
        panel(d, (x, y, x + gw, y + gh), col)
        text(d, (x + 18, y + 8), tag, 12, col, True)
        icon(img, x + gw - 32, y + 22, ico, col, 26)
        wrapped = wrap(d, head, 19, gw - 36, True)
        multiline(d, (x + 18, y + 26), wrapped, 19, WHITE, True, 0)
        lines = len(wrapped.split("\n"))
        text(d, (x + 18, y + 28 + lines * 21), sub, 13, MUTED)

    panel(d, (40, 742, 620, 966), radius=12)
    text(d, (58, 754), "ALSO ON MONDAY", 18, AMBER, True)
    for i, (col, line) in enumerate(MORE):
        y = 788 + i * 20
        d.ellipse((58, y + 4, 66, y + 12), fill=col)
        text(d, (76, y), line, 14, WHITE)

    panel(d, (640, 742, 984, 966), radius=12)
    text(d, (658, 754), "COLOUR KEY", 18, AMBER, True)
    for i, (name, col) in enumerate(KEY):
        y = 788 + i * 20
        d.rounded_rectangle((658, y + 3, 670, y + 15), radius=3, fill=col)
        text(d, (680, y), name, 14, WHITE)

    text(d, (40, 980),
         "All stories happened or were first reported on Monday 23 November 2026. One day, one image.",
         13, MUTED)

    out_dir = "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
    except PermissionError:
        out_dir = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(out_dir, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
