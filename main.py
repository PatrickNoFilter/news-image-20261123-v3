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
    ("CLIMATE", "COP31 ends with no deal", "Longest UN climate summit, Antalya", "#E8B24C", "gavel"),
    ("UKRAINE", "Dnipro strike kills 11", "Boy, 7, pulled alive from rubble", "#E46965", "drones"),
    ("US POLITICS", "Democrats win the House", "258 seats, best since 1992", "#6BCB9A", "house"),
]

GRID = [
    ("EUROPE", "Belgium flights grounded", "Strike against austerity measures", "#8E9BF6", "plane"),
    ("BALTIC", "Ship attacked in Gulf of Finland", "Ukraine likely behind drone strike", "#E46965", "ship"),
    ("ASIA", "Korea exam chief resigns", "Chaos over AI-cheating measures", "#4FC3D9", "exam"),
    ("CULTURE", "Miley Cyrus marries Maxx Morando", "California ceremony, four years together", "#C792EA", "rings"),
    ("US", "Iowa explosives to be detonated", "Army defies court order", "#E8B24C", "blast"),
    ("AFRICA", "Nigeria boat tragedy rescue race", "Overcrowding and missing life jackets", "#D98CB3", "boat"),
    ("SCIENCE", "Mercury gets first visitors", "Two spacecraft enter orbit", "#63C7B2", "space"),
    ("CULTURE", "Ancient library opens in Rome", "Restored after years of work", "#4FC3D9", "book"),
]

MORE = [
    ("FRANCE", "Street protests over reforms — Macron blames the radical left"),
    ("PENTAGON", "More UFO footage declassified — eighth tranche includes three videos"),
    ("MARKETS", "Anthropic record IPO — charities prepare for windfall"),
    ("HEALTH", "Virginia reports measles death — first young child death in 2026"),
    ("CANADA", "Carney jokes at press dinner — fake Trump draws laughs"),
    ("SEATTLE", "Two passengers detained by ICE — family baptism trip, lawyer says"),
    ("SPORT", "NFL analyst Tom Jackson dies — Broncos star and analyst was 75"),
    ("DIPLOMACY", "Kenya, DR Congo restore ties — leaders pledge non-interference"),
]


def build():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.rectangle((0, 0, W, 7), fill=AMBER)
    text(d, (40, 26), "THE WORLD IN ONE IMAGE  ·  MONDAY EDITION", 17, MUTED, True)
    text(d, (38, 56), "23 NOVEMBER 2026", 74, WHITE, True)
    d.line((40, 146, 984, 146), fill=BORDER, width=3)

    cw, gap = 312, 12
    for i, (tag, head, sub, col, ico) in enumerate(HEROES):
        x = 40 + i * (cw + gap)
        panel(d, (x, 162, x + cw, 326), col)
        d.rectangle((x + 1, 163, x + cw - 1, 170), fill=col)
        text(d, (x + 18, 182), tag, 15, col, True)
        icon(img, x + cw - 38, 200, ico, col, 36)
        wrapped = wrap(d, head, 24, cw - 36, True)
        multiline(d, (x + 18, 212), wrapped, 24, WHITE, True, 1)
        text(d, (x + 18, 292), sub, 14, MUTED)

    stats = [("11", "killed in Dnipro strike"), ("258", "House seats won"),
             ("19", "stories, 7 regions"), ("1", "day: 23 Nov 2026")]
    sw = (944 - 3 * 10) // 4
    for i, (num, lab) in enumerate(stats):
        x = 40 + i * (sw + 10)
        panel(d, (x, 338, x + sw, 402), radius=10)
        text(d, (x + 14, 350), num, 30, AMBER, True)
        text(d, (x + 14, 386), lab, 13, MUTED)

    gx0, gy0, gw, gh, vgap = 40, 414, 462, 78, 8
    for i, (tag, head, sub, col, ico) in enumerate(GRID):
        x = gx0 + (i % 2) * (gw + 20)
        y = gy0 + (i // 2) * (gh + vgap)
        panel(d, (x, y, x + gw, y + gh), col)
        text(d, (x + 18, y + 8), tag, 12, col, True)
        icon(img, x + gw - 36, y + 26, ico, col, 30)
        wrapped = wrap(d, head, 19, gw - 70, True)
        multiline(d, (x + 18, y + 26), wrapped, 19, WHITE, True, 0)
        text(d, (x + 18, y + 56), sub, 13, MUTED)

    panel(d, (40, 752, 620, 962), radius=12)
    text(d, (58, 766), "ALSO ON MONDAY", 19, AMBER, True)
    for i, (tag, line) in enumerate(MORE):
        y = 800 + i * 19
        d.ellipse((58, y + 4, 66, y + 12), fill=["#8E9BF6", "#E46965", "#4FC3D9", "#C792EA"][i % 4])
        text(d, (76, y), line, 14, WHITE)

    panel(d, (640, 752, 984, 962), radius=12)
    text(d, (658, 766), "REGIONS COVERED", 19, AMBER, True)
    regions = [
        ("EUROPE", "#8E9BF6"), ("UKRAINE / BALTIC", "#E46965"),
        ("AFRICA", "#D98CB3"), ("ASIA / PACIFIC", "#4FC3D9"),
        ("AMERICAS", "#6BCB9A"), ("SCIENCE / CULTURE", "#C792EA"),
        ("CLIMATE / MARKETS", "#E8B24C"),
    ]
    for i, (name, col) in enumerate(regions):
        y = 802 + i * 21
        d.rounded_rectangle((658, y + 3, 670, y + 15), radius=3, fill=col)
        text(d, (680, y), name, 15, WHITE)

    text(d, (40, 976),
         "All stories happened or were first reported on Monday 23 November 2026. One day, one image.",
         14, MUTED)

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
