#!/usr/bin/env python3
"""Draw the front page for Tuesday 17 November 2026 as a 1024x1024 PNG.

Everything is drawn from scratch with Pillow: flat vector-style
illustrations, a masthead, three lead stories, nine mid stories, a
numbered list of thirty-one further stories, and a world map with
numbered pins. No network, no timestamps, no randomness, so the
output bytes are identical on every run.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 18
CONTENT = W - 2 * MARGIN  # 988

PAPER = (247, 241, 222)
INK = (26, 26, 26)
SOFT_INK = (74, 68, 58)
RED = (176, 30, 30)
BLUE = (31, 78, 121)
RULE = (150, 138, 110)
BOX_BG = (238, 231, 205)
SKY = (205, 224, 235)
SEA = (120, 165, 200)
LAND = (222, 205, 160)
LAND2 = (200, 210, 170)

REGION = {
    "Americas": (31, 119, 180),
    "Europe": (44, 160, 44),
    "Middle East": (214, 39, 40),
    "Asia": (255, 127, 14),
    "Africa": (148, 103, 189),
    "Oceania": (23, 190, 207),
}

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    """Split text into lines that fit width (greedy, by words)."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, width, fill=INK, leading=None):
    """Draw wrapped text; return the y just below the last line."""
    if leading is None:
        leading = int(font.size * 1.25)
    for line in wrap(d, text, font, width):
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def rule(d, x0, x1, y, width=1, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def centre(d, cx, y, text, font, fill=INK):
    w = d.textlength(text, font=font)
    d.text((cx - w / 2, y), text, font=font, fill=fill)
    return w


def pin(d, x, y, number, colour):
    """A numbered round map pin."""
    r = 9
    d.ellipse([x - r, y - r, x + r, y + r], fill=colour,
              outline=(255, 255, 255), width=2)
    f = F(SANS_B, 10)
    t = str(number)
    tw = d.textlength(t, font=f)
    th = f.getbbox(t)[3]
    d.text((x - tw / 2, y - th / 2 - 1), t, font=f, fill=(255, 255, 255))

# ---------------------------------------------------------------------------
# Lead illustrations (flat drawn scenes, 322 px wide each)
# ---------------------------------------------------------------------------

def draw_bridge(d, x, y, w, h):
    """Kerch Strait: a road bridge over water, middle span broken."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=SEA)
    # far shore
    d.polygon([(x, y + int(h * 0.58)), (x + w, y + int(h * 0.58)),
               (x + w, y + int(h * 0.62)), (x, y + int(h * 0.62))],
              fill=(170, 185, 165))
    deck_y = y + int(h * 0.42)
    # towers
    for tx in (x + 52, x + w - 62):
        d.rectangle([tx, deck_y - 34, tx + 8, deck_y + 30], fill=(90, 90, 90))
        d.line([(tx + 4, deck_y - 34), (tx - 34, deck_y)],
               fill=(90, 90, 90), width=2)
        d.line([(tx + 4, deck_y - 34), (tx + 42, deck_y)],
               fill=(90, 90, 90), width=2)
    # deck: left span intact, middle span fallen, right span intact
    d.rectangle([x + 6, deck_y, x + 132, deck_y + 7], fill=(70, 70, 70))
    d.rectangle([x + 196, deck_y, x + w - 6, deck_y + 7], fill=(70, 70, 70))
    # fallen span, tilted down into the water
    d.polygon([(x + 136, deck_y + 2), (x + 192, deck_y + 2),
               (x + 186, deck_y + 34), (x + 140, deck_y + 26)],
              fill=(52, 52, 52))
    # splash + smoke over the gap (kept inside the picture)
    for cx, cy, r in ((x + 164, deck_y + 30, 9), (x + 176, deck_y + 26, 7)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(235, 244, 248))
    for cx, cy, r in ((x + 150, deck_y - 12, 8), (x + 166, deck_y - 18, 10),
                       (x + 184, deck_y - 12, 7)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 120))
    d.ellipse([x + 161, deck_y - 16, x + 171, deck_y - 6],
              fill=(220, 90, 40))
    # caption banner
    d.rectangle([x, y + h - 15, x + w, y + h], fill=INK)
    centre(d, x + w // 2, y + h - 14, "KERCH STRAIT  ·  STRUCK FOR A SECOND DAY",
           F(SANS_B, 9), fill=(255, 255, 255))


def draw_gulf(d, x, y, w, h):
    """Persian Gulf: Iran above, Bahrain, Qeshm, Hormuz, a tanker."""
    d.rectangle([x, y, x + w, y + h], fill=LAND)
    # the gulf water, running diagonally
    d.polygon([(x + 60, y + h), (x + 150, y), (x + 235, y),
               (x + 150, y + h)], fill=SEA)
    # Bahrain island
    d.ellipse([x + 158, y + 34, x + 168, y + 46], fill=(255, 255, 255),
              outline=INK, width=1)
    # Qeshm island
    d.polygon([(x + 205, y + 52), (x + 245, y + 46), (x + 258, y + 58),
               (x + 218, y + 64)], fill=(235, 220, 180), outline=INK)
    # tanker in the gulf
    d.rectangle([x + 128, y + 62, x + 158, y + 72], fill=(40, 40, 40))
    d.rectangle([x + 138, y + 56, x + 148, y + 62], fill=(40, 40, 40))
    # drone dots, crossed out
    for dx, dy in ((x + 120, y + 26), (x + 140, y + 18), (x + 100, y + 40)):
        d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=RED)
        d.line([(dx - 5, dy - 5), (dx + 5, dy + 5)], fill=RED, width=2)
        d.line([(dx - 5, dy + 5), (dx + 5, dy - 5)], fill=RED, width=2)
    f = F(SANS_B, 10)
    d.text((x + 8, y + 6), "IRAN", font=f, fill=INK)
    d.text((x + 176, y + 30), "BAHRAIN", font=F(SANS_B, 8), fill=INK)
    d.text((x + 208, y + 66), "QESHM", font=F(SANS_B, 8), fill=INK)
    d.text((x + 238, y + 8), "HORMUZ", font=F(SANS_B, 8), fill=INK)
    d.text((x + 8, y + h - 30), "DRONES DOWNED", font=f, fill=RED)
    d.text((x + 8, y + h - 16), "US STRIKES", font=f, fill=INK)


def draw_bars(d, x, y, w, h):
    """Nvidia sales bars rising to $115.8bn; Dow arrow falling."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                outline=RULE, width=1)
    base = y + h - 18
    vals = [("Q1", 30), ("Q2", 46), ("Q3", 57), ("Q4", 115.8)]
    bw, gap = 34, 22
    bx = x + 18
    for label, v in vals:
        bh = int(v / 115.8 * (h - 38))
        last = v == 115.8
        d.rectangle([bx, base - bh, bx + bw, base],
                    fill=RED if last else BLUE)
        f = F(SANS_B, 9)
        centre(d, bx + bw // 2, base - bh - 12,
               "$%.1fbn" % v if last else "$%.0fbn" % v, f,
               fill=RED if last else INK)
        centre(d, bx + bw // 2, base + 3, label, F(SANS, 9), fill=SOFT_INK)
        bx += bw + gap
    d.line([(x + 10, base), (x + w - 8, base)], fill=INK, width=1)
    # falling Dow arrow, top right
    ax, ay = x + w - 96, y + 8
    d.polygon([(ax, ay), (ax + 62, ay + 26), (ax + 62, ay + 18),
               (ax + 12, ay - 4)], fill=RED)
    d.polygon([(ax + 56, ay + 12), (ax + 68, ay + 30), (ax + 52, ay + 26)],
              fill=RED)
    d.text((ax + 2, ay + 30), "DOW -849", font=F(SANS_B, 10), fill=RED)


# ---------------------------------------------------------------------------
# Small icons for the nine mid stories (54x54 boxes)
# ---------------------------------------------------------------------------

def icon_summit(d, x, y):
    d.rectangle([x, y, x + 54, y + 54], fill=BOX_BG, outline=RULE)
    d.rectangle([x + 12, y + 26, x + 42, y + 32], fill=(150, 110, 60))
    for i, c in enumerate(((31, 119, 180), (214, 39, 40),
                           (44, 160, 44), (255, 127, 14))):
        cx = x + 12 + i * 11
        d.ellipse([cx, y + 10, cx + 8, y + 18], fill=c)
    d.text((x + 14, y + 36), "QUAD", font=F(SANS_B, 9), fill=INK)


def icon_virus(d, x, y):
    d.rectangle([x, y, x + 54, y + 54], fill=BOX_BG, outline=RULE)
    cx, cy = x + 27, y + 27
    for ang in range(0, 360, 30):
        import math
        r = math.radians(ang)
        d.line([(cx + 12 * math.cos(r), cy + 12 * math.sin(r)),
                (cx + 19 * math.cos(r), cy + 19 * math.sin(r))],
               fill=RED, width=2)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=RED)
    d.ellipse([cx - 4, cy - 5, cx + 1, cy], fill=(255, 255, 255))
    d.ellipse([cx + 3, cy + 2, cx + 8, cy + 7], fill=(255, 255, 255))


def icon_measles(d, x, y):
    d.rectangle([x, y, x + 54, y + 54], fill=BOX_BG, outline=RULE)
    d.polygon([(x + 27, y + 6), (x + 44, y + 13), (x + 44, y + 28),
               (x + 27, y + 48), (x + 10, y + 28), (x + 10, y + 13)],
              outline=BLUE, width=2)
    d.line([(x + 20, y + 20), (x + 34, y + 34)], fill=RED, width=3)
    d.line([(x + 34, y + 20), (x + 20, y + 34)], fill=RED, width=3)


def icon_climate(d, x, y):
    d.rectangle([x, y, x + 54, y + 54], fill=BOX_BG, outline=RULE)
    cx, cy = x + 24, y + 30
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=SEA,
              outline=BLUE, width=1)
    d.ellipse([cx - 14, cy - 4, cx + 14, cy + 4], outline=BLUE, width=1)
    d.line([(cx, cy - 14), (cx, cy + 14)], fill=BLUE, width=1)
    d.ellipse([x + 38, y + 8, x + 48, y + 18], fill=(240, 180, 40))
    for dx, dy in ((-4, -4), (4, -4), (-4, 4), (4, 4)):
        d.line([(x + 43 + dx, y + 13 + dy), (x + 43 + dx * 2, y + 13 + dy * 2)],
               fill=(240, 180, 40), width=2)


def icon_truce(d, x, y):
    d.rectangle([x, y, x + 54, y + 54], fill=BOX_BG, outline=RULE)
    d.polygon([(x + 16, y + 10), (x + 38, y + 10), (x + 38, y + 22),
               (x + 16, y + 22)], fill=(255, 255, 255), outline=INK)
    d.line([(x + 16, y + 10), (x + 16, y + 46)], fill=INK, width=2)
    d.line([(x + 16, y + 34), (x + 38, y + 46)], fill=RED, width=3)
    d.line([(x + 38, y + 34), (x + 16, y + 46)], fill=RED, width=3)
    d.text((x + 30, y + 38), "?", font=F(SANS_B, 12), fill=RED)


def icon_jets(d, x, y):
    d.rectangle([x, y, x + 54, y + 54], fill=BOX_BG, outline=RULE)
    d.polygon([(x + 12, y + 30), (x + 34, y + 18), (x + 44, y + 30),
               (x + 34, y + 34)], fill=INK)
    d.polygon([(x + 30, y + 34), (x + 40, y + 44), (x + 34, y + 44)],
              fill=INK)
    for r in (8, 15, 22):
        d.arc([x + 34 - r, y + 8 - r, x + 34 + r, y + 8 + r],
              start=200, end=340, fill=RED, width=2)
    d.ellipse([x + 31, y + 5, x + 37, y + 11], fill=RED)


def icon_bank(d, x, y):
    d.rectangle([x, y, x + 54, y + 54], fill=BOX_BG, outline=RULE)
    d.polygon([(x + 10, y + 20), (x + 27, y + 8), (x + 44, y + 20)],
              fill=BLUE)
    for cx in (x + 14, x + 24, x + 34):
        d.rectangle([cx, y + 22, cx + 4, y + 38], fill=BLUE)
    d.rectangle([x + 10, y + 38, x + 44, y + 42], fill=BLUE)
    d.line([(x + 34, y + 44), (x + 46, y + 50)], fill=RED, width=3)
    d.polygon([(x + 42, y + 44), (x + 50, y + 50), (x + 44, y + 52)],
              fill=RED)
    d.text((x + 8, y + 44), "-6%", font=F(SANS_B, 9), fill=RED)


def icon_voyager(d, x, y):
    d.rectangle([x, y, x + 54, y + 54], fill=(20, 30, 60), outline=RULE)
    for sx, sy in ((x + 8, y + 10), (x + 44, y + 12), (x + 14, y + 44),
                    (x + 40, y + 42), (x + 48, y + 28)):
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    d.polygon([(x + 18, y + 30), (x + 30, y + 20), (x + 38, y + 30),
               (x + 28, y + 32)], fill=(220, 220, 220))
    d.line([(x + 30, y + 20), (x + 38, y + 14)], fill=(220, 220, 220),
           width=2)
    d.text((x + 6, y + 40), "1 LIGHT-DAY", font=F(SANS_B, 7),
           fill=(255, 255, 255))


def icon_airspace(d, x, y):
    d.rectangle([x, y, x + 54, y + 54], fill=BOX_BG, outline=RULE)
    d.ellipse([x + 10, y + 12, x + 26, y + 22], fill=(255, 255, 255),
              outline=SOFT_INK)
    d.ellipse([x + 20, y + 8, x + 36, y + 22], fill=(255, 255, 255),
              outline=SOFT_INK)
    for dx, dy in ((x + 16, y + 34), (x + 28, y + 40), (x + 40, y + 32)):
        d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=INK)
    d.ellipse([x + 34, y + 36, x + 50, y + 52], outline=RED, width=3)
    d.line([(x + 37, y + 39), (x + 47, y + 49)], fill=RED, width=3)

# ---------------------------------------------------------------------------
# Story data
# ---------------------------------------------------------------------------

LEADS = [
    ("EUROPE  ·  UKRAINE WAR", REGION["Europe"], draw_bridge,
     "Ukraine says a Kerch Bridge road span fell into the sea",
     "Second strike in two days; Zelensky hails an \u2018unprecedented "
     "operation\u2019. The Kremlin vows to rebuild."),
    ("MIDDLE EAST  ·  IRAN WAR", REGION["Middle East"], draw_gulf,
     "Iran sends drones at a US radar in Bahrain; US hits back",
     "Bahrain and the US say all were downed; US jets then strike Qeshm. "
     "Iran says tankers hit mines in Hormuz."),
    ("US  ·  BUSINESS", REGION["Americas"], draw_bars,
     "Nvidia\u2019s quarterly sales double to $115.8bn",
     "Reported after the close. Earlier the Dow fell 849 points."),
]

MIDS = [
    ("ASIA  ·  DIPLOMACY", "Asia", icon_summit,
     "Trump holds his first Quad summit, in Manila",
     "The four unveil critical-minerals deals; Putin reaches Shenzhen for "
     "Thursday\u2019s talks with Trump and Xi."),
    ("AFRICA  ·  HEALTH", "Africa", icon_virus,
     "Ebola cases in DR Congo top 11,000, WHO says",
     "Cases more than doubled in three months; about 5,400 have died."),
    ("AMERICAS  ·  HEALTH", "Americas", icon_measles,
     "US, Mexico and Bolivia lose measles-free status",
     "PAHO cites a year of spread; the US has 5,700+ cases in 2026."),
    ("GLOBAL  ·  CLIMATE", "Europe", icon_climate,
     "COP31 divided over a fossil-fuel phase-out",
     "Nations weigh the first draft; the Antalya talks end Friday."),
    ("MIDDLE EAST  ·  GAZA", "Middle East", icon_truce,
     "Gaza truce at risk of collapse, UN is told",
     "Board of Peace report; UN agencies say 1.4m face acute hunger."),
    ("ASIA  ·  SECURITY", "Asia", icon_jets,
     "Japan scrambles jets over airspace breach",
     "Two suspected Russian aircraft near Fukuoka; Tokyo protests."),
    ("EUROPE  ·  BANKING", "Europe", icon_bank,
     "Deutsche Bank falls 6% on leaked files",
     "Reuters could not verify the claims."),
    ("SPACE", "Oceania", icon_voyager,
     "Voyager 1 nears one light-day from Earth",
     "Crosses early Wednesday; \u221225.9bn km."),
    ("EUROPE  ·  SECURITY", "Europe", icon_airspace,
     "Moldova shuts airspace over drones",
     "7 detected; 5 fell near villages."),
]

NUMBERS = [
    ("11,000+", "Ebola cases in DR Congo"),
    ("$115.8bn", "Nvidia quarterly sales"),
    ("\u2212849", "Dow points lost"),
    ("1,441", "drones Russia says it downed"),
    ("2m+", "facing acute hunger in Gaza"),
    ("1 light-day", "Voyager 1 nears it"),
]

ALSO = [
    "Russia: says it downed a record 1,441 drones overnight.",
    "Kyiv: missiles hit the North and South Dnipro bridges.",
    "UN: Ukraine\u2019s civilian deaths this year top all of 2025.",
    "France: public-sector strike, 146,000 march.",
    "Poland: Tusk\u2019s government survives a no-confidence vote.",
    "Turkey: police seize opposition broadcaster S\u00f6zc\u00fc TV.",
    "UK: sanctions 8 settlement firms and Tzav 9.",
    "Israel: Eisenkot ally Matan Kahana elected speaker, 66\u201352.",
    "West Bank: settlers kill a woman, 72, near Jericho.",
    "Oman: Iran\u2019s Araghchi holds shipping-safety talks.",
    "India: Cyclone Akvan strengthens; Odisha evacuates.",
    "India: bus falls into an Uttarakhand gorge, 8 dead.",
    "China\u2013Canada: more tariff cuts after Carney\u2013Xi talks.",
    "Malaysia: Macron visit seals a strategic partnership.",
    "Thailand: pledges to scrap tariffs on US goods.",
    "South Korea: IMF lifts 2026 growth forecast to 3.9%.",
    "Football: India beat Pakistan 2\u20131 in SAFF final.",
    "Football: Togo beat Algeria 3\u20130 in AFCON qualifier.",
    "Football: Norway win 3\u20132 in Denmark; Haaland scores twice.",
    "Kenya: WFP aids 30,000 who fled Ethiopia clashes.",
    "Haiti: Aristide\u2019s party will field no candidates.",
    "US Senate: Van Hollen challenges Schumer for leader.",
    "Australia: eases planned backpacker visa curbs.",
    "Darwin: M6.6 quake off Indonesia felt; no tsunami.",
    "Apple: Pay, iCloud and App Store outage; not a hack.",
    "JPMorgan: software bug, \u201cnot cyber\u201d, hit Zelle payments.",
    "France: Depardieu drops appeal, admits sexual assault charge.",
    "Serbia: student-led majority sworn in, 140 of 250 seats.",
    "Mongolia: president says he will resign; denies $25m bribe claim.",
    "Bangladesh: police tear-gas garment workers\u2019 wage protest.",
    "Russia: An-12 crash in Siberia kills all 19 aboard.",
]

# (story number, lon, lat, region) for the world map pins.
PINS = [
    (1, 38, 48, "Europe"), (2, 52, 24, "Middle East"),
    (3, -90, 42, "Americas"), (4, 121, 14.5, "Asia"),
    (5, 23, -2, "Africa"), (6, -102, 22, "Americas"),
    (7, 28, 40, "Europe"), (8, 34, 30, "Middle East"),
    (9, 130.4, 33.6, "Asia"), (10, 8.7, 50.1, "Europe"),
    (11, 150, 55, "Oceania"), (12, 28.8, 47, "Europe"),
]

CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73),
           (-60, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 25),
           (-90, 20), (-105, 20), (-115, 30), (-125, 40), (-140, 60)],
    "SA": [(-80, 10), (-60, 5), (-50, 0), (-40, -5), (-35, -10),
           (-40, -20), (-50, -30), (-60, -35), (-70, -50), (-75, -40),
           (-75, -20), (-80, -5)],
    "EU": [(-10, 36), (-5, 44), (0, 50), (5, 55), (10, 58), (20, 60),
           (30, 70), (40, 68), (30, 60), (25, 55), (20, 45), (12, 44),
           (3, 42), (-2, 37)],
    "AF": [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (32, 31),
           (35, 28), (43, 12), (48, 10), (40, 0), (35, -10), (30, -20),
           (20, -35), (12, -30), (15, -20), (9, 0), (0, 5), (-8, 5)],
    "AS": [(40, 68), (60, 70), (80, 73), (100, 75), (130, 72), (160, 70),
           (178, 66), (162, 60), (158, 52), (142, 45), (135, 35),
           (127, 33), (120, 25), (110, 20), (105, 10), (100, 8),
           (95, 15), (90, 22), (80, 15), (75, 10), (70, 20), (60, 25),
           (50, 28), (45, 30), (40, 36)],
    "OC": [(113, -22), (125, -15), (142, -11), (150, -22), (153, -27),
           (146, -39), (140, -38), (130, -32), (115, -35)],
}


def draw_map(d, x, y, w, h):
    """Simplified equirectangular world map with numbered pins."""
    d.rectangle([x, y, x + w, y + h], fill=(225, 235, 240),
                outline=RULE, width=1)
    lat_top, lat_bot = 78, -58
    span = lat_top - lat_bot

    def px(lon, lat):
        return (x + (lon + 180) / 360 * w,
                y + (lat_top - lat) / span * h)

    for poly in CONTINENTS.values():
        d.polygon([px(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=(120, 105, 75))
    # New Zealand dot
    nzx, nzy = px(172, -41)
    d.ellipse([nzx - 3, nzy - 3, nzx + 3, nzy + 3], fill=LAND,
              outline=(120, 105, 75))
    for num, lon, lat, region in PINS:
        px_, py_ = px(lon, lat)
        pin(d, px_, py_, num, REGION[region])


def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN
    y = 8

    # Masthead
    centre(d, W // 2, y, "THE WORLD\u2019S NEWS IN ONE PICTURE",
           F(SANS_B, 13), fill=RED)
    y += 20
    centre(d, W // 2, y, "Tuesday 17 November 2026",
           F(SERIF_B, 46), fill=INK)
    y += 54
    rule(d, x0, x1, y, width=2, fill=INK)
    y += 6
    centre(d, W // 2, y, "43 STORIES  ·  6 CONTINENTS  ·  ONE DAY",
           F(SANS_B, 13), fill=INK)
    y += 20
    rule(d, x0, x1, y, width=1)
    y += 6

    # Day in numbers
    bw = CONTENT // 6
    for i, (num, label) in enumerate(NUMBERS):
        bx = x0 + i * bw
        d.rectangle([bx, y, bx + bw - 2, y + 48], outline=RULE, width=1)
        centre(d, bx + (bw - 2) // 2, y + 2, num, F(SANS_B, 16), fill=RED)
        para(d, bx + 5, y + 23, label, F(SANS, 9), bw - 12,
             fill=SOFT_INK, leading=11)
    y += 54
    rule(d, x0, x1, y, width=2, fill=INK)
    y += 8

    # Three lead stories
    col_w = (CONTENT - 2 * 11) // 3  # 322
    lead_top = y
    for i, (kicker, colour, artist, headline, deck) in enumerate(LEADS):
        cx = x0 + i * (col_w + 11)
        d.text((cx, y), kicker, font=F(SANS_B, 11), fill=colour)
        artist(d, cx, y + 16, col_w, 84)
        ny = para(d, cx, y + 104, headline, F(SERIF_B, 17), col_w,
                  leading=20)
        para(d, cx, ny + 2, deck, F(SANS, 11), col_w, leading=14)
        if i < 2:
            d.line([(cx + col_w + 5, lead_top),
                    (cx + col_w + 5, y + 188)], fill=RULE, width=1)
    y += 190
    rule(d, x0, x1, y, width=2, fill=INK)
    y += 8

    # Nine mid stories, 3x3 grid
    row_h = 78
    for row in range(3):
        for col in range(3):
            idx = row * 3 + col
            kicker, region, artist, headline, deck = MIDS[idx]
            cx = x0 + col * (col_w + 11)
            cy = y + row * row_h
            artist(d, cx, cy + 2, )
            tx = cx + 62
            tw = col_w - 62
            d.text((tx, cy), kicker, font=F(SANS_B, 9), fill=REGION[region])
            ny = para(d, tx, cy + 12, headline, F(SERIF_B, 13), tw,
                      leading=14)
            para(d, tx, ny + 1, deck, F(SANS, 10), tw, leading=12)
        if row < 2:
            rule(d, x0, x1, y + (row + 1) * row_h - 5, width=1)
    y += 3 * row_h
    rule(d, x0, x1, y, width=2, fill=INK)
    y += 6

    # Also on Tuesday: items 13-43 in two columns
    d.text((x0, y), "ALSO ON TUESDAY 17 NOVEMBER",
           font=F(SANS_B, 13), fill=INK)
    y += 18
    col_w2 = (CONTENT - 16) // 2
    f_item = F(SANS, 11)
    for i, item in enumerate(ALSO):
        col = 0 if i < 16 else 1
        r = i if i < 16 else i - 16
        ix = x0 + col * (col_w2 + 16)
        iy = y + r * 12
        d.text((ix, iy), "%d  %s" % (13 + i, item), font=f_item, fill=INK)
    y += 16 * 12 + 4
    rule(d, x0, x1, y, width=2, fill=INK)
    y += 6

    # World map
    d.text((x0, y), "WHERE IT HAPPENED",
           font=F(SANS_B, 13), fill=INK)
    y += 18
    map_h = 96
    draw_map(d, x0, y, CONTENT, map_h)
    y += map_h + 4
    lx = x0
    for name, colour in REGION.items():
        d.rectangle([lx, y + 2, lx + 10, y + 12], fill=colour)
        lx += 14
        w_ = d.textlength(name, font=F(SANS_B, 10))
        d.text((lx, y), name, font=F(SANS_B, 10), fill=INK)
        lx += int(w_) + 16
    y += 18
    rule(d, x0, x1, y, width=1)
    y += 5

    # Footer
    centre(d, W // 2, y,
           "Every story here happened or was first reported on "
           "Tuesday 17 November 2026. Contested claims are marked as claims.",
           F(SANS, 10), fill=SOFT_INK)
    y += 14
    centre(d, W // 2, y,
           "Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN. "
           "Original drawings.",
           F(SANS, 10), fill=SOFT_INK)
    y += 14
    assert y <= H - 4, "layout overflow: y=%d" % y

    img.save(path, optimize=True)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    build(out)
    print("wrote", out, os.path.getsize(out), "bytes")
