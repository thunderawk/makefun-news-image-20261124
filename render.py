#!/usr/bin/env python3
"""Render the front page for make.fun news-image-20261124.

Draws "TUESDAY 24 NOVEMBER 2026 - THE WORLD IN ONE DAY": a modern
broadsheet front page on cream paper with real drawn text (PIL), flat
illustrated art, a dotted world map, and a DATE CHECK box that keeps
Monday's news honestly dated. Deterministic: same bytes every run.
Stdlib + Pillow only, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 16                      # margin
CW = W - 2 * M              # content width = 992
PAPER = (247, 242, 231)
INK = (26, 26, 26)
NAVY = (27, 42, 74)
RED = (176, 30, 36)
GREY = (107, 107, 107)
GOLD = (217, 164, 65)
GREEN = (46, 125, 70)
TEAL = (31, 120, 110)
OCHRE = (198, 138, 28)
PURPLE = (96, 63, 131)
SKY = (135, 180, 210)
CREAM2 = (238, 231, 214)

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def FSB(size):   # DejaVu Serif Bold
    return font(FD + "DejaVuSerif-Bold.ttf", size)


def FSN(size):   # DejaVu Sans
    return font(FD + "DejaVuSans.ttf", size)


def FSBI(size):  # DejaVu Sans Bold
    return font(FD + "DejaVuSans-Bold.ttf", size)


def FSI(size):   # Liberation Serif Italic (no DejaVu serif italic on this box)
    return font(FL + "LiberationSerif-Italic.ttf", size)


def tw(d, text, f):
    return d.textlength(text, font=f)


def wrap(d, text, f, width):
    """Greedy word wrap to the given pixel width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if tw(d, trial, f) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, f, width, fill, lh, max_lines=None):
    """Draw wrapped text; returns (lines_drawn, new_y)."""
    lines = wrap(d, text, f, width)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        print("WARN wrap: truncated to %d lines: %s" % (max_lines, text[:40]))
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return len(lines), y


# ---------------------------------------------------------------- art ---
def art_markets(d, x, y, w, h):
    """Candlestick chart with a rising line on navy."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    pts = [0.78, 0.66, 0.70, 0.52, 0.58, 0.38, 0.44, 0.26]
    n = len(pts)
    for i, p in enumerate(pts):
        cx = x + 14 + i * (w - 28) / (n - 1)
        top = y + 10 + p * (h - 34)
        bot = top + 16
        col = (232, 90, 70) if i % 3 else (90, 180, 120)
        d.rectangle([cx - 4, top, cx + 4, bot], fill=col)
        d.line([cx, top - 6, cx, bot + 6], fill=col, width=2)
    line = [(x + 14 + i * (w - 28) / (n - 1),
             y + 10 + p * (h - 34) + 8) for i, p in enumerate(pts)]
    d.line(line, fill=GOLD, width=3, joint="curve")
    for px, py in line:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=GOLD)


def art_chess(d, x, y, w, h):
    """Chess board, a white king, a black king, and a clock."""
    sq = w / 8.0
    for r in range(4):
        for c in range(8):
            if (r + c) % 2 == 0:
                d.rectangle([x + c * sq, y + r * (h / 4.0),
                             x + (c + 1) * sq, y + (r + 1) * (h / 4.0)],
                            fill=(232, 224, 200))
    d.rectangle([x, y, x + w, y + h], fill=(27, 42, 74), outline=None)
    for r in range(4):
        for c in range(8):
            if (r + c) % 2 == 0:
                d.rectangle([x + c * sq, y + r * (h / 4.0),
                             x + (c + 1) * sq, y + (r + 1) * (h / 4.0)],
                            fill=(232, 224, 200))
    # white king, left
    kx, ky = x + w * 0.30, y + h * 0.42
    d.ellipse([kx - 16, ky - 14, kx + 16, ky + 14], fill=(250, 250, 250),
              outline=INK, width=2)
    d.polygon([(kx, ky - 26), (kx - 9, ky - 8), (kx + 9, ky - 8)],
              fill=(250, 250, 250), outline=INK)
    d.rectangle([kx - 18, ky + 10, kx + 18, ky + 22], fill=(250, 250, 250),
                outline=INK, width=2)
    # black king, right
    kx2, ky2 = x + w * 0.68, y + h * 0.42
    d.ellipse([kx2 - 16, ky2 - 14, kx2 + 16, ky2 + 14], fill=INK)
    d.polygon([(kx2, ky2 - 26), (kx2 - 9, ky2 - 8), (kx2 + 9, ky2 - 8)],
              fill=INK)
    d.rectangle([kx2 - 18, ky2 + 10, kx2 + 18, ky2 + 22], fill=INK)
    # clock, bottom right
    cx, cy, r = x + w - 26, y + h - 24, 15
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 250, 250),
              outline=INK, width=2)
    d.line([cx, cy, cx, cy - 9], fill=INK, width=2)
    d.line([cx, cy, cx + 7, cy + 3], fill=INK, width=2)


def art_trophy(d, x, y, w, h):
    """Gold trophy on green, with a small football."""
    d.rectangle([x, y, x + w, y + h], fill=(31, 92, 52))
    cx, cy = x + w * 0.42, y + h * 0.44
    d.ellipse([cx - 34, cy - 26, cx - 18, cy + 4], outline=GOLD, width=5)
    d.ellipse([cx + 18, cy - 26, cx + 34, cy + 4], outline=GOLD, width=5)
    d.polygon([(cx - 26, cy - 28), (cx + 26, cy - 28), (cx + 18, cy + 12),
               (cx - 18, cy + 12)], fill=GOLD)
    d.rectangle([cx - 6, cy + 12, cx + 6, cy + 30], fill=GOLD)
    d.rectangle([cx - 22, cy + 30, cx + 22, cy + 38], fill=GOLD)
    # football, bottom right
    bx, by, r = x + w - 30, y + h - 26, 14
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=(250, 250, 250),
              outline=INK, width=2)
    d.polygon([(bx, by - 6), (bx + 6, by - 2), (bx + 4, by + 6),
               (bx - 4, by + 6), (bx - 6, by - 2)], fill=INK)


def art_parliament(d, x, y, w, h):
    """Parliament house: columns and a red dome."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
    cx = x + w / 2
    d.pieslice([cx - 22, y + 2, cx + 22, y + 30], 180, 360, fill=RED)
    d.rectangle([x + 8, y + h - 14, x + w - 8, y + h - 6], fill=INK)
    for i in range(5):
        px = x + 14 + i * (w - 28) / 4
        d.rectangle([px - 4, y + 16, px + 4, y + h - 14], fill=(250, 250, 250),
                    outline=INK, width=1)


def art_skyline(d, x, y, w, h):
    """Night skyline with lit windows and a moon."""
    d.rectangle([x, y, x + w, y + h], fill=(38, 52, 82))
    d.ellipse([x + w - 26, y + 4, x + w - 10, y + 20], fill=(250, 230, 140))
    for i, (bw, bh) in enumerate([(20, 26), (16, 34), (22, 20), (16, 30),
                                  (20, 24)]):
        bx = x + 6 + i * 36
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(16, 22, 38))
        for wy in range(y + h - bh + 4, y + h - 4, 7):
            for wx in range(bx + 3, bx + bw - 3, 6):
                if (wx + wy) % 11 < 6:
                    d.rectangle([wx, wy, wx + 2, wy + 2], fill=GOLD)


def art_islands(d, x, y, w, h):
    """Pacific islands: sea, sand, palms."""
    d.rectangle([x, y, x + w, y + h], fill=(96, 170, 205))
    for (ix, iy, iw) in [(0.18, 0.55, 34), (0.52, 0.62, 44), (0.80, 0.48, 28)]:
        cx, cy = x + w * ix, y + h * iy
        d.ellipse([cx - iw / 2, cy - 7, cx + iw / 2, cy + 7], fill=(238, 220, 170))
        d.line([cx, cy - 4, cx, cy - 20], fill=(60, 90, 40), width=2)
        d.ellipse([cx - 10, cy - 24, cx + 2, cy - 14], fill=(46, 125, 70))
        d.ellipse([cx, cy - 24, cx + 12, cy - 14], fill=(46, 125, 70))


def art_storm(d, x, y, w, h):
    """Storm clouds, rain, lightning."""
    d.rectangle([x, y, x + w, y + h], fill=(120, 140, 165))
    for (cx, cy, r) in [(0.25, 0.40, 16), (0.45, 0.32, 20), (0.68, 0.42, 17)]:
        px, py = x + w * cx, y + h * cy
        d.ellipse([px - r, py - r * 0.7, px + r, py + r * 0.7], fill=(52, 62, 82))
    d.polygon([(x + w * 0.55, y + h * 0.55), (x + w * 0.48, y + h * 0.78),
               (x + w * 0.56, y + h * 0.78), (x + w * 0.50, y + h * 0.95)],
              fill=(250, 220, 60))
    for i in range(5):
        rx = x + 12 + i * 34
        d.line([rx, y + h - 18, rx - 3, y + h - 6], fill=(220, 230, 245),
               width=2)


def art_ballot(d, x, y, w, h):
    """Ballot box with a ticked slip."""
    d.rectangle([x, y, x + w, y + h], fill=(178, 30, 36))
    d.rectangle([x + w * 0.18, y + h * 0.42, x + w * 0.82, y + h * 0.88],
                fill=(250, 250, 250))
    d.rectangle([x + w * 0.38, y + h * 0.34, x + w * 0.62, y + h * 0.44],
                fill=INK)
    d.rectangle([x + w * 0.30, y + h * 0.12, x + w * 0.66, y + h * 0.36],
                fill=(250, 250, 250), outline=INK, width=1)
    d.line([x + w * 0.36, y + h * 0.24, x + w * 0.44, y + h * 0.32,
            x + w * 0.60, y + h * 0.16], fill=(46, 125, 70), width=3)


def art_tower(d, x, y, w, h):
    """Skyscraper with a phone showing a green chart."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 30, 48))
    d.rectangle([x + 12, y + 8, x + 34, y + h], fill=(52, 66, 96))
    d.rectangle([x + 40, y + 16, x + 58, y + h], fill=(38, 50, 76))
    for bx in (12, 40):
        for wy in range(y + 12, y + h - 6, 8):
            d.rectangle([x + bx + 4, wy, x + bx + 8, wy + 3], fill=GOLD)
            d.rectangle([x + bx + 12, wy, x + bx + 16, wy + 3], fill=GOLD)
    d.rectangle([x + w - 52, y + 8, x + w - 12, y + h - 8], fill=(16, 16, 16),
                outline=(200, 200, 200), width=1)
    d.rectangle([x + w - 48, y + 12, x + w - 16, y + h - 12], fill=(20, 40, 30))
    d.line([(x + w - 46, y + h - 18), (x + w - 36, y + h - 28),
            (x + w - 28, y + h - 24), (x + w - 18, y + h - 34)],
           fill=(90, 220, 120), width=2)


def art_chart(d, x, y, w, h):
    """Bar chart, last bar green."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 224, 200))
    bars = [14, 20, 16, 26, 22, 34]
    bw = (w - 16) / len(bars)
    for i, bh in enumerate(bars):
        bx = x + 8 + i * bw
        col = (46, 125, 70) if i == len(bars) - 1 else (27, 42, 74)
        d.rectangle([bx + 2, y + h - 6 - bh, bx + bw - 2, y + h - 6], fill=col)


def art_book(d, x, y, w, h):
    """Open book with text lines and a red bookmark."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 231, 214))
    d.polygon([(x + 10, y + 8), (x + w / 2, y + 14), (x + w / 2, y + h - 8),
               (x + 10, y + h - 8)], fill=(250, 248, 240), outline=INK)
    d.polygon([(x + w - 10, y + 8), (x + w / 2, y + 14), (x + w / 2, y + h - 8),
               (x + w - 10, y + h - 8)], fill=(250, 248, 240), outline=INK)
    for wy in range(y + 16, y + h - 12, 6):
        d.line([x + 16, wy, x + w / 2 - 8, wy], fill=GREY, width=1)
        d.line([x + w / 2 + 8, wy, x + w - 16, wy], fill=GREY, width=1)
    d.polygon([(x + w - 30, y + 6), (x + w - 20, y + 6), (x + w - 20, y + 22),
               (x + w - 25, y + 17), (x + w - 30, y + 22)], fill=RED)


def art_stadium(d, x, y, w, h):
    """Stadium bowl under floodlights."""
    d.rectangle([x, y, x + w, y + h], fill=(31, 92, 52))
    d.ellipse([x + 8, y + 8, x + w - 8, y + h - 6], fill=(200, 210, 220),
              outline=(250, 250, 250), width=3)
    d.ellipse([x + 22, y + 16, x + w - 22, y + h - 14], fill=(46, 125, 70))
    d.line([x + 10, y + 6, x + 10, y + 2], fill=(250, 250, 200), width=3)
    d.line([x + w - 10, y + 6, x + w - 10, y + 2], fill=(250, 250, 200),
           width=3)


def art_controller(d, x, y, w, h):
    """Game controller with coloured buttons."""
    d.rectangle([x, y, x + w, y + h], fill=(58, 28, 92))
    cx, cy = x + w / 2, y + h / 2
    d.rounded_rectangle([cx - 62, cy - 16, cx + 62, cy + 18], radius=14,
                        fill=(30, 30, 30))
    d.line([cx - 46, cy, cx - 34, cy], fill=(250, 250, 250), width=3)
    d.line([cx - 40, cy - 6, cx - 40, cy + 6], fill=(250, 250, 250), width=3)
    for (bx, by, col) in [(cx + 34, cy - 8, (250, 220, 60)),
                          (cx + 44, cy + 2, (232, 90, 70)),
                          (cx + 34, cy + 8, (90, 180, 120)),
                          (cx + 24, cy + 2, (96, 170, 205))]:
        d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=col)

# ---------------------------------------------------------------- map ---
# Dotted world map: land spans on a 48x24 grid, lon -170..190, lat 75..-55.
LAND = [
    (2, 3, 10, 3), (4, 6, 8, 2), (12, 3, 6, 3), (13, 6, 5, 2),
    (18, 2, 12, 4), (19, 6, 9, 3), (20, 9, 6, 2), (24, 3, 8, 3),
    (25, 6, 10, 4), (26, 10, 7, 2), (28, 12, 5, 2), (31, 3, 6, 2),
    (32, 5, 5, 3), (33, 8, 4, 2), (34, 10, 6, 2), (36, 4, 5, 2),
    (37, 6, 4, 2), (38, 8, 3, 2), (40, 12, 4, 2), (41, 14, 3, 2),
    (42, 16, 3, 2), (43, 18, 2, 2), (44, 14, 4, 3), (45, 11, 3, 2),
]
PINS = [  # (story no, lon, lat)
    (1, 139.7, 35.7), (2, 6.1, 46.2), (3, 6.6, 46.5),
    (4, 147.3, -9.4), (5, 149.1, -35.3), (10, -77.0, 38.9),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
    gw, gh = w / 48.0, h / 24.0
    for (cx0, cy0, cw, ch) in LAND:
        for gx in range(cx0, cx0 + cw):
            for gy in range(cy0, cy0 + ch):
                px = x + gx * gw + gw / 2
                py = y + gy * gh + gh / 2
                d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6],
                          fill=(120, 110, 88))
    for (no, lon, lat) in PINS:
        px = x + (lon + 170) / 360.0 * w
        py = y + (75 - lat) / 130.0 * h
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((px - 3, py - 6), str(no), font=FSBI(9), fill=(255, 255, 255))


# --------------------------------------------------------------- data ---
PRESS_UTC = "00:00"          # wires read to this UTC time

NUMBERS = [
    ("60,279", "Nikkei close, +2.6%"),
    ("+4%", "Kospi jump to 5,219"),
    ("$2.5m", "World chess title fund"),
    ("15%", "SoftBank leap"),
    ("98%", "Bougainville's 2019 vote"),
]
REGIONS = [
    ("EUROPE 2", 79, NAVY), ("ASIA-PACIFIC 6", 238, OCHRE),
    ("OCEANIA 13", 500, GREEN), ("AMERICAS 3", 119, PURPLE),
    ("WORLD 1", 56, GREY),
]
TIMELINE = [
    (PRESS_UTC, "Wires read to press time"),
    ("13:30", "US inflation data due"),
    ("14:00", "Game 1, Geneva"),
    ("15:00", "CAS ruling due"),
]

LEADS = [
    dict(chip="REPORTED", num=1, loc="TOKYO, JAPAN", kicker="WORLD \u00b7 MARKETS",
         head="Asia roars back as Tokyo reopens",
         body=("The Nikkei jumps 2.6% to 60,279 after the long weekend, the "
               "Kospi climbs 4% to 5,219 and Taiwan's Taiex gains 3.4% \u2014 "
               "riding Wall Street's best day since April, when the Nasdaq "
               "rose 6.5%."),
         src="Reuters \u00b7 AP", art=art_markets),
    dict(chip="TODAY", num=2, loc="GENEVA, SWITZERLAND", kicker="WORLD \u00b7 CHESS",
         head="Youngest title match opens in Geneva",
         body=("Gukesh, 20, defends his crown against Sindarov, 20 \u2014 the "
               "youngest World Championship ever. Game 1 starts 15:00 CET, "
               "Sindarov with White; 14 games, $2.5m fund."),
         src="FIDE \u00b7 Chess.com", art=art_chess),
    dict(chip="PENDING", num=3, loc="LAUSANNE, SWITZERLAND",
         kicker="WORLD \u00b7 FOOTBALL",
         head="AFCON title to be decided in court today",
         body=("CAS rules this afternoon on Senegal's appeal against losing "
               "the 2025 Africa Cup of Nations title to Morocco after "
               "January's chaotic final in Rabat."),
         src="Reuters \u00b7 CAS", art=art_trophy),
]

CARDS = [
    dict(chip="TODAY", num=4, loc="PORT MORESBY, PNG", kicker="OCEANIA \u00b7 POLITICS",
         head="PNG votes on Bougainville independence",
         body=("Parliament votes today on ratifying the 2019 vote, when "
               "almost 98% backed independence."),
         art=art_parliament),
    dict(chip="TODAY", num=5, loc="CANBERRA, AUSTRALIA", kicker="OCEANIA \u00b7 DIPLOMACY",
         head="Albanese hosts Singapore's Wong",
         body=("Trade, AI and defence on the agenda as the Singapore PM "
               "visits Canberra."),
         art=art_skyline),
    dict(chip="REPORTED", num=6, loc="PACIFIC", kicker="OCEANIA \u00b7 CLIMATE",
         head="Pacific states go it alone after COP31 fails",
         body=("Island nations form their own climate coalitions after the "
               "Antalya talks collapse."),
         art=art_islands),
    dict(chip="FORECAST", num=7, loc="AUSTRALIA", kicker="OCEANIA \u00b7 WEATHER",
         head="Storms to hit four states today",
         body=("Hail, heavy rain and damaging winds forecast for millions "
               "this afternoon."),
         art=art_storm),
    dict(chip="REPORTED", num=8, loc="MELBOURNE, AUSTRALIA",
         kicker="OCEANIA \u00b7 POLITICS",
         head="Labor faces worst poll since 1902",
         body=("A new poll puts the 12-year Victorian government on course "
               "for disaster at Saturday's election."),
         art=art_ballot),
    dict(chip="REPORTED", num=9, loc="TOKYO, JAPAN", kicker="ASIA-PACIFIC \u00b7 MARKETS",
         head="SoftBank leaps 15% before earnings",
         body=("The OpenAI investor leads Asia's tech rebound as chip "
               "stocks recover."),
         art=art_tower),
    dict(chip="TODAY", num=10, loc="WASHINGTON, USA", kicker="AMERICAS \u00b7 ECONOMY",
         head="US inflation data due today",
         body=("The release could steer Fed rate expectations after "
               "Monday's Wall Street rally."),
         art=art_chart),
    dict(chip="REPORTED", num=11, loc="SYDNEY, AUSTRALIA", kicker="OCEANIA \u00b7 CULTURE",
         head="\u2018Pervert glasses\u2019 is word of the year",
         body=("Macquarie Dictionary picks the slang for camera-fitted "
               "smart glasses as its 2026 word."),
         art=art_book),
    dict(chip="REPORTED", num=12, loc="HOBART, AUSTRALIA", kicker="OCEANIA \u00b7 SPORT",
         head="Hobart stadium cost jumps $100m",
         body=("The AFL stadium bill rises to $1.23 billion, figures "
               "released today show."),
         art=art_stadium),
    dict(chip="REPORTED", num=13, loc="NEW YORK, USA", kicker="AMERICAS \u00b7 GAMING",
         head="GTA VI hides 60 birds to find",
         body=("The New Yorker counts the hidden birds players can track "
               "across the new game."),
         art=art_controller),
]

ALSO = [
    (14, "Taiex gains 3.4% as chip stocks rebound", "Reuters"),
    (15, "Hang Seng +0.4% to 24,535", "Reuters"),
    (16, "Shanghai Composite +0.4% to 3,673", "Reuters"),
    (17, "ASX 200 +1.1% to 9,131", "Reuters"),
    (18, "MSCI Asia-Pacific ex-Japan +1.5%", "Reuters"),
    (19, "Oil eases as Iran strike fears fade", "Reuters"),
    (20, "Hunter rentals eat 31% of wages, worst ever", "Newcastle Herald"),
    (21, "Two die in head-on crash near Grafton", "AAP"),
    (22, "Teen critical after Gold Coast Schoolies row", "9News"),
    (23, "Bluey float scrapped over BBC copyright claim", "ABC News"),
    (24, "Remote NT childcare centres shut for good", "ABC News"),
    (25, "VW rebadges Chinese van as new Tempest", "Reuters"),
]

DATE_CHECK = (
    "Left out because they happened on an earlier day: Nvidia reinstates "
    "Huang (Mon) \u00b7 India gives Nepal $1.62bn (Mon) \u00b7 Zelenskiy "
    "warns of new strikes (Mon) \u00b7 Moscow warns Estonia of \u2018open "
    "war\u2019 (Mon) \u00b7 US drone helped catch \u2018Chapo Isidro\u2019 "
    "(Mon) \u00b7 Cikande toll 24 (Mon) \u00b7 US blacklists Megaspeed "
    "(Mon) \u00b7 Two states sue SpaceX over Grok (Mon) \u00b7 Denmark "
    "backs \u2018ghetto law\u2019 (Mon) \u00b7 Iran flogs Ahmadi (Mon) \u00b7 "
    "Israeli strike kills UNRWA worker (Mon) \u00b7 Trump pauses Iowa "
    "blast (Mon) \u00b7 COP31 ends with no deal (Sun) \u00b7 Alcaraz wins "
    "ATP Finals (Sun)")

SOURCES = ("Sources: Reuters, AP, AFP, BBC, ABC News, AAP, The Conversation, "
           "FIDE, Chess.com, CAS. Scenes are drawn illustrations, not "
           "photographs. Wires read to %s UTC, Tue 24 Nov 2026." % PRESS_UTC)

# -------------------------------------------------------------- layout ---
def chip_color(chip):
    return {"REPORTED": GREEN, "TODAY": OCHRE, "PENDING": PURPLE,
            "FORECAST": GREY}.get(chip, NAVY)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top bar
    d.rectangle([0, 0, W, 20], fill=NAVY)
    d.text((M, 5), "THE WORLD IN ONE DAY", font=FSBI(10), fill=(255, 255, 255))
    top_right = "25 STORIES \u00b7 5 REGIONS \u00b7 TUESDAY 24 NOVEMBER 2026"
    d.text((W - M - tw(d, top_right, FSBI(10)), 5), top_right,
           font=FSBI(10), fill=GOLD)

    # masthead: the date is the biggest type on the page
    y = 20
    mast = "Tuesday 24 November 2026"
    print("masthead width %d (limit %d)" % (tw(d, mast, FSB(62)), CW))
    d.text((M, y + 4), mast, font=FSB(62), fill=INK)
    y += 76

    # deck: the 3 top stories in one line
    deck = ("Asia roars back as Tokyo reopens \u00b7 Youngest chess title "
            "match opens in Geneva \u00b7 CAS to rule on the AFCON title today")
    print("deck width %d (limit %d)" % (tw(d, deck, FSI(15)), CW))
    d.text(((W - tw(d, deck, FSI(15))) / 2, y), deck, font=FSI(15), fill=RED)
    y += 22
    d.line([M, y, W - M, y], fill=INK, width=2)
    y += 4

    # BY THE NUMBERS strip
    col_w = CW / 5.0
    for i, (num, lab) in enumerate(NUMBERS):
        cx = M + col_w * (i + 0.5)
        d.text((cx - tw(d, num, FSB(30)) / 2, y), num, font=FSB(30), fill=RED)
        d.text((cx - tw(d, lab, FSN(9)) / 2, y + 34), lab, font=FSN(9),
               fill=GREY)
        if i:
            d.line([M + col_w * i, y + 4, M + col_w * i, y + 42], fill=GREY,
                   width=1)
    y += 46
    d.line([M, y, W - M, y], fill=INK, width=1)
    y += 2

    # region bar
    rx = M
    for (name, rw, col) in REGIONS:
        d.rectangle([rx, y, rx + rw, y + 22], fill=col)
        d.text((rx + (rw - tw(d, name, FSBI(9))) / 2, y + 6), name,
               font=FSBI(9), fill=(255, 255, 255))
        rx += rw
    y += 22

    # UTC timeline
    d.rectangle([M, y, W - M, y + 22], fill=NAVY)
    tx = M + 8
    d.text((tx, y + 6), "THE DAY IN UTC", font=FSBI(10), fill=GOLD)
    tx += tw(d, "THE DAY IN UTC", FSBI(10)) + 16
    for (t, what) in TIMELINE:
        d.text((tx, y + 6), t, font=FSBI(10), fill=GOLD)
        tx += tw(d, t, FSBI(10)) + 6
        d.text((tx, y + 6), what, font=FSN(10), fill=(255, 255, 255))
        tx += tw(d, what, FSN(10)) + 22
    y += 22 + 6

    # 3 lead panels
    lead_w, lead_gap, lead_h = 325, 8, 250
    for i, L in enumerate(LEADS):
        lx = M + i * (lead_w + lead_gap)
        d.rectangle([lx, y, lx + lead_w, y + lead_h], outline=INK, width=1,
                    fill=(255, 255, 255))
        L["art"](d, lx + 1, y + 1, lead_w - 2, 106)
        ly = y + 106 + 8
        # chip + location on one line
        cw_ = tw(d, L["chip"], FSBI(9)) + 10
        d.rectangle([lx + 8, ly, lx + 8 + cw_, ly + 14],
                    fill=chip_color(L["chip"]))
        d.text((lx + 13, ly + 2), L["chip"], font=FSBI(9), fill=(255, 255, 255))
        d.text((lx + 8 + cw_ + 6, ly + 2),
               "%d \u00b7 %s" % (L["num"], L["loc"]), font=FSBI(9), fill=GREY)
        ly += 18
        d.text((lx + 8, ly), L["kicker"], font=FSBI(9), fill=RED)
        ly += 13
        _, ly = draw_wrapped(d, lx + 8, ly, L["head"], FSB(17), lead_w - 16,
                             INK, 21, max_lines=2)
        _, ly = draw_wrapped(d, lx + 8, ly, L["body"], FSN(10), lead_w - 16,
                             INK, 13, max_lines=4)
        d.text((lx + 8, y + lead_h - 14), L["src"], font=FSN(8), fill=GREY)
    y += lead_h + 6

    # section label
    d.text((M, y), "THE DAY IN TEN", font=FSBI(11), fill=INK)
    right = "THE STORIES THAT MOVED THE WORLD TODAY"
    d.text((W - M - tw(d, right, FSN(9)), y + 2), right, font=FSN(9),
           fill=GREY)
    y += 16

    # 10 cards, 2 rows of 5
    card_w, card_gap, card_h = 193, 6, 132
    for i, C in enumerate(CARDS):
        row, col = divmod(i, 5)
        cx = M + col * (card_w + card_gap)
        cy = y + row * (card_h + card_gap)
        d.rectangle([cx, cy, cx + card_w, cy + card_h], outline=INK, width=1,
                    fill=(255, 255, 255))
        C["art"](d, cx + 1, cy + 1, card_w - 2, 44)
        ly = cy + 44 + 5
        cw_ = tw(d, C["chip"], FSBI(8)) + 8
        d.rectangle([cx + 6, ly, cx + 6 + cw_, ly + 12],
                    fill=chip_color(C["chip"]))
        d.text((cx + 10, ly + 1), C["chip"], font=FSBI(8), fill=(255, 255, 255))
        d.text((cx + 6 + cw_ + 4, ly + 1),
               "%d \u00b7 %s" % (C["num"], C["loc"]), font=FSBI(8), fill=GREY)
        ly += 15
        d.text((cx + 6, ly), C["kicker"], font=FSBI(8), fill=RED)
        ly += 11
        _, ly = draw_wrapped(d, cx + 6, ly, C["head"], FSB(12), card_w - 12,
                             INK, 14, max_lines=2)
        draw_wrapped(d, cx + 6, ly, C["body"], FSN(9), card_w - 12, INK, 11,
                     max_lines=3)
    y += 2 * card_h + card_gap + 6

    # map + ALSO (ALSO rows are relative to the label row, y0)
    y0 = y
    d.text((M, y0), "WHERE IT HAPPENED", font=FSBI(11), fill=INK)
    d.text((M, y0 + 12), "pins match story numbers", font=FSN(8), fill=GREY)
    also_x = M + 330 + 12
    d.text((also_x, y0), "ALSO ON TUESDAY 24 NOVEMBER \u2014 12 MORE STORIES",
           font=FSBI(11), fill=INK)
    y += 26
    map_w = 330
    draw_map(d, M, y, map_w, 132)
    f_also = FSN(10)
    for i, (no, text, src) in enumerate(ALSO):
        col = i // 6
        ax = also_x + col * 330
        cy = y0 + 18 + (i % 6) * 24
        d.text((ax, cy), str(no), font=FSBI(10), fill=RED)
        _, _ = draw_wrapped(d, ax + 24, cy, "%s (%s)" % (text, src), f_also,
                            330 - 24, INK, 12, max_lines=2)
    y += 132 + 8

    # DATE CHECK
    d.rectangle([M, y, W - M, y + 48], outline=RED, width=2)
    f_dc = FSBI(10)
    lab_w = tw(d, "DATE CHECK", f_dc)
    d.text((M + 8, y + 5), "DATE CHECK", font=f_dc, fill=RED)
    f_dct = FSN(10)
    first_w = CW - 16 - lab_w - 12
    lines = wrap(d, DATE_CHECK, f_dct, first_w)
    rest = wrap(d, " ".join(lines[1:]), f_dct, CW - 16) if len(lines) > 1 else []
    all_lines = [lines[0]] + rest if lines else []
    if len(all_lines) > 3:
        print("WARN date-check: %d lines" % len(all_lines))
        all_lines = all_lines[:3]
    ly = y + 5
    d.text((M + 8 + lab_w + 8, ly), all_lines[0], font=f_dct, fill=INK)
    for ln in all_lines[1:]:
        ly += 13
        d.text((M + 8, ly), ln, font=f_dct, fill=INK)
    y += 48 + 6

    # sources line
    _, y = draw_wrapped(d, M, y, SOURCES, FSN(8), CW, GREY, 11, max_lines=1)
    y += 4
    print("content bottom y=%d (limit %d)" % (y, H - 18))

    # footer
    d.rectangle([0, H - 18, W, H], fill=NAVY)
    d.text((M, H - 13), "THE WORLD IN ONE DAY", font=FSBI(9),
           fill=(255, 255, 255))
    foot = "TUESDAY 24 NOVEMBER 2026 \u00b7 ONE PAGE"
    d.text((W - M - tw(d, foot, FSBI(9)), H - 13), foot, font=FSBI(9),
           fill=GOLD)
    return img


def main():
    out = os.environ.get("OUT", "entry.png")
    img = render()
    img.save(out)
    print("wrote %s" % out)


if __name__ == "__main__":
    main()
