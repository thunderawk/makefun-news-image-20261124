#!/usr/bin/env python3
"""Render the news-image-20261124 entry: one front page summing up
Tuesday 24 November 2026. Deterministic: no randomness, no clock —
press time is a fixed string. Writes entry.png next to this file."""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952

PAPER = (247, 241, 222)
INK = (27, 23, 18)
MUTED = (107, 97, 86)
RULE = (180, 168, 145)
RED = (169, 50, 38)
BLUE = (31, 78, 121)
TEAL = (15, 118, 110)
GREEN = (46, 125, 79)
OCHRE = (183, 121, 31)
PURPLE = (107, 78, 155)
SLATE = (71, 85, 105)
PALE_BLUE = (220, 233, 245)
PALE_CREAM = (239, 230, 208)
PALE_TERRA = (243, 226, 216)

LIB = "/usr/share/fonts/truetype/liberation/"
DJV = "/usr/share/fonts/truetype/dejavu/"


def font(cands, size):
    for path in cands:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def serif_b(size):
    return font([LIB + "LiberationSerif-Bold.ttf",
                 DJV + "DejaVuSerif-Bold.ttf"], size)


def serif(size):
    return font([LIB + "LiberationSerif-Regular.ttf",
                 DJV + "DejaVuSerif.ttf"], size)


def serif_i(size):
    return font([LIB + "LiberationSerif-Italic.ttf",
                 DJV + "DejaVuSerif-Italic.ttf"], size)


def sans_b(size):
    return font([LIB + "LiberationSans-Bold.ttf",
                 DJV + "DejaVuSans-Bold.ttf"], size)


def sans(size):
    return font([LIB + "LiberationSans-Regular.ttf",
                 DJV + "DejaVuSans.ttf"], size)


def wrap(d, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def ellipsize(d, text, fnt, width):
    if d.textlength(text, font=fnt) <= width:
        return text
    while text and d.textlength(text + "\u2026", font=fnt) > width:
        text = text[:-1]
    return text + "\u2026"


def fit_font(cands_fn, text, width, start):
    size = start
    while size > 10:
        fnt = cands_fn(size)
        tmp = Image.new("RGB", (8, 8))
        d = ImageDraw.Draw(tmp)
        if d.textlength(text, font=fnt) <= width:
            return fnt
        size -= 1
    return cands_fn(10)


# ---------------------------------------------------------------- stories
# 25 stories: 3 leads + 10 cards + 6 ALSO + 6 DATE CHECK.
# Region counts (honest, from this list): Europe 5, Asia-Pacific 5,
# Oceania 7, Americas 5, World 3. Continents: 4.

LEADS = [
    dict(tag="MARKETS", title="Tokyo roars back: Nikkei tops 60,000",
         body=("Nikkei +2.6% to 60,279 as Tokyo reopens; Kospi +4% to "
               "5,219; SoftBank +15%."),
         art="markets"),
    dict(tag="CHESS", title="Gukesh v Sindarov: the kids' title match begins",
         body=("Game 1 today, 15:00 CET, Sindarov White. Both 20 — the "
               "youngest title match ever; $2.5m fund."),
         art="chess"),
    dict(tag="FOOTBALL", title="CAS to rule on Senegal's AFCON appeal",
         body=("Ruling due in the afternoon (GMT). Marca reports Morocco "
               "expected to keep the title — unconfirmed."),
         art="cas"),
]

CARDS = [
    dict(n=1, tag="OCEANIA", title="Bougainville vote goes to parliament",
         body="PNG MPs vote today — 98% backed independence in 2019.",
         color=TEAL, glyph="peak"),
    dict(n=2, tag="OCEANIA", title="Albanese hosts Singapore's Wong",
         body="The Singapore PM visits Canberra to deepen ties.",
         color=BLUE, glyph="circles"),
    dict(n=3, tag="OCEANIA", title="Pacific states go it alone after COP31",
         body="With COP31 ending in no deal, island nations chart their own course.",
         color=TEAL, glyph="wave"),
    dict(n=4, tag="OCEANIA", title="Storms lash four Australian states",
         body="Severe weather hits the east and south as the week begins.",
         color=SLATE, glyph="bolt"),
    dict(n=5, tag="OCEANIA", title="Victorian Labor's worst poll since 1902",
         body="State Labor slumps to a historic low in the latest polling.",
         color=PURPLE, glyph="bars"),
    dict(n=6, tag="AMERICAS", title="US inflation data due today",
         body="Out this morning; markets watch for the Fed's next move.",
         color=GREEN, glyph="arrow"),
    dict(n=7, tag="OCEANIA", title="Word of the year: \u2018pervert glasses\u2019",
         body="Macquarie Dictionary picks the slang term for 2026.",
         color=OCHRE, glyph="book"),
    dict(n=8, tag="OCEANIA", title="Hobart's $1.23bn stadium debate",
         body="Tasmania's new arena plan divides the island state.",
         color=RED, glyph="arc"),
    dict(n=9, tag="WORLD", title="GTA VI hides 60 birds",
         body="Rockstar's trailer rewards sharp eyes: 60 birds to spot.",
         color=INK, glyph="star"),
    dict(n=10, tag="AMERICAS", title="Nvidia brings Huang back",
         body="Mon 23 Nov — The chip giant reinstates its co-founder as CEO.",
         color=GREEN, glyph="chip"),
]

ALSO = [
    "India gives Nepal $1.62bn",
    "Zelenskiy warns of new Russian strikes",
    "Moscow warns Estonia of \u2018open war\u2019",
    "Cikande toll road confirmed for the 24th",
    "US blacklists Megaspeed",
    "Two states sue SpaceX over Grok",
]

DATE_CHECK = [
    ("Denmark backs \u2018ghetto law\u2019", "MON 23 NOV"),
    ("Iran flogs Ahmadi, 74 lashes", "MON 23 NOV"),
    ("Israeli strike kills UNRWA worker", "MON 23 NOV"),
    ("US drone helped catch \u2018Chapo Isidro\u2019", "MON 23 NOV"),
    ("COP31 ends with no deal", "SUN 22 NOV"),
    ("Alcaraz wins the ATP Finals", "SUN 22 NOV"),
]

NUMBERS = [
    ("60,279", "Nikkei close, +2.6%"),
    ("+4%", "Kospi to 5,219"),
    ("+15%", "SoftBank shares"),
    ("$2.5m", "Chess title fund"),
    ("98%", "Bougainville vote"),
]

TIMELINE = [
    ("00:00 UTC", "Tokyo reopens"),
    ("13:30 UTC", "US inflation data"),
    ("14:00 UTC", "Gukesh\u2013Sindarov G1 (15:00 CET)"),
    ("Afternoon", "CAS ruling due (GMT)"),
]

# Dotted world map: continents as ellipses on a 72 x 36 grid
# (5 degrees per cell; y 0 = lat 90).
CONTINENTS = [
    (11, 8, 10, 5),      # North America
    (22, 3.5, 2, 1.5),   # Greenland
    (17, 21, 4, 6.5),    # South America
    (35, 7, 4.5, 3),     # Europe
    (36.5, 16, 5, 6),    # Africa
    (49, 7, 11, 5),      # Asia
    (53, 13.5, 4, 2),    # SE Asia
    (56.5, 22, 4.5, 2.5),  # Australia
    (62, 24, 1, 1.5),    # New Zealand
    (32.5, 5.5, 1, 1.2),  # UK
    (63, 10, 1.2, 2),    # Japan
    (53, 15.5, 5, 1),    # Indonesia
]

# lon, lat, label, label side (l/r), label dy
PINS = [
    (139.7, 35.7, "TOKYO", "l", -4),
    (147.2, -9.5, "PORT MORESBY", "r", -4),
    (149.1, -35.3, "CANBERRA", "r", 2),
    (6.6, 46.5, "LAUSANNE", "l", -4),
    (-77.0, 38.9, "WASHINGTON", "l", -4),
    (77.2, 28.6, "NEW DELHI", "r", -4),
]


def in_land(gx, gy):
    for cx, cy, rx, ry in CONTINENTS:
        if ((gx - cx) / rx) ** 2 + ((gy - cy) / ry) ** 2 <= 1.0:
            return True
    return False


# ---------------------------------------------------------------- art
def draw_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PALE_BLUE)
    # sun
    d.ellipse([x + w - 52, y + 10, x + w - 16, y + 46], fill=OCHRE)
    # ascending bars
    base = y + h - 18
    bw, gap = 34, 16
    heights = [28, 44, 58, 74, 92]
    for i, bh in enumerate(heights):
        bx = x + 22 + i * (bw + gap)
        d.rectangle([bx, base - bh, bx + bw, base], fill=GREEN)
    # rising arrow
    pts = [(x + 22, base - 28), (x + 90, base - 52),
           (x + 150, base - 66), (x + 216, base - 96)]
    d.line(pts, fill=RED, width=4)
    d.polygon([(x + 216, base - 96), (x + 196, base - 96),
               (x + 214, base - 78)], fill=RED)
    d.line([x + 14, base, x + w - 14, base], fill=INK, width=2)


def draw_crown(d, cx, base, s, fill, outline):
    # simple three-spike crown, s = half-width
    pts = [(cx - s, base), (cx - s, base - int(s * 0.9)),
           (cx - int(s * 0.5), base - int(s * 0.45)),
           (cx, base - int(s * 1.05)),
           (cx + int(s * 0.5), base - int(s * 0.45)),
           (cx + s, base - int(s * 0.9)), (cx + s, base)]
    d.polygon(pts, fill=fill, outline=outline)
    d.rectangle([cx - s, base - 4, cx + s, base], fill=fill, outline=outline)


def draw_chess(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PALE_CREAM)
    # checker strip at the bottom
    sq = 29
    top = y + h - 2 * sq
    for r in range(2):
        for c in range(10):
            if (r + c) % 2 == 0:
                d.rectangle([x + 8 + c * sq, top + r * sq,
                             x + 8 + (c + 1) * sq, top + (r + 1) * sq],
                            fill=INK)
    draw_crown(d, x + 78, top - 6, 30, (255, 255, 255), INK)
    draw_crown(d, x + w - 78, top - 6, 30, INK, INK)


def draw_cas(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PALE_TERRA)
    cx, top = x + w // 2, y + 16
    # post and beam
    d.line([cx, top, cx, top + 62], fill=INK, width=4)
    d.line([cx - 78, top + 8, cx + 78, top + 8], fill=INK, width=4)
    # pans
    for sx in (cx - 78, cx + 78):
        d.line([sx, top + 8, sx, top + 34], fill=INK, width=3)
        d.polygon([(sx - 26, top + 34), (sx + 26, top + 34),
                   (sx, top + 52)], fill=RED, outline=INK)
    # soccer ball
    bx, by, br = x + w - 46, y + h - 34, 20
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 255, 255),
              outline=INK, width=2)
    d.polygon([(bx, by - 7), (bx + 7, by - 2), (bx + 4, by + 7),
               (bx - 4, by + 7), (bx - 7, by - 2)], fill=INK)


ART = {"markets": draw_markets, "chess": draw_chess, "cas": draw_cas}


def draw_glyph(d, x, y, s, kind, color):
    # white pictogram inside a coloured tile of size s at (x, y)
    wht = (255, 255, 255)
    if kind == "peak":
        d.polygon([(x + 4, y + s - 4), (x + s // 2, y + 5),
                   (x + s - 4, y + s - 4)], outline=wht, width=2)
    elif kind == "circles":
        d.ellipse([x + 4, y + 8, x + s - 12, y + s - 4], outline=wht, width=2)
        d.ellipse([x + 12, y + 4, x + s - 4, y + s - 12], outline=wht, width=2)
    elif kind == "wave":
        for k in range(3):
            yy = y + 8 + k * 7
            d.line([(x + 4, yy), (x + 10, yy - 3), (x + 16, yy),
                    (x + 22, yy - 3), (x + s - 4, yy)], fill=wht, width=2)
    elif kind == "bolt":
        d.polygon([(x + 17, y + 3), (x + 8, y + 16), (x + 14, y + 16),
                   (x + 12, y + s - 3), (x + 22, y + 13), (x + 16, y + 13)],
                  fill=wht)
    elif kind == "bars":
        for i, bh in enumerate((8, 14, 20)):
            bx = x + 6 + i * 8
            d.rectangle([bx, y + s - 5 - bh, bx + 5, y + s - 5], fill=wht)
    elif kind == "arrow":
        d.line([x + 6, y + s - 8, x + s - 8, y + 8], fill=wht, width=3)
        d.polygon([(x + s - 8, y + 8), (x + s - 8, y + 16),
                   (x + s - 16, y + 8)], fill=wht)
    elif kind == "book":
        d.polygon([(x + 4, y + 7), (x + s // 2, y + 11), (x + s // 2, y + s - 5),
                   (x + 4, y + s - 9)], outline=wht, width=2)
        d.polygon([(x + s - 4, y + 7), (x + s // 2, y + 11),
                   (x + s // 2, y + s - 5), (x + s - 4, y + s - 9)],
                  outline=wht, width=2)
    elif kind == "arc":
        d.arc([x + 4, y + 8, x + s - 4, y + s + 6], 180, 360, fill=wht, width=3)
        d.line([x + 4, y + s - 6, x + s - 4, y + s - 6], fill=wht, width=2)
    elif kind == "star":
        cx, cy = x + s // 2, y + s // 2
        d.polygon([(cx, cy - 10), (cx + 3, cy - 3), (cx + 10, cy),
                   (cx + 3, cy + 3), (cx, cy + 10), (cx - 3, cy + 3),
                   (cx - 10, cy), (cx - 3, cy - 3)], fill=wht)
    elif kind == "chip":
        d.rectangle([x + 9, y + 9, x + s - 9, y + s - 9], outline=wht, width=2)
        for px in (12, 18, 24):
            d.line([x + px, y + 4, x + px, y + 9], fill=wht, width=2)
            d.line([x + px, y + s - 9, x + px, y + s - 4], fill=wht, width=2)


# ---------------------------------------------------------------- render
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead
    f_mast = serif_b(30)
    t = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 18), t, font=f_mast, fill=INK)
    d.line([MARGIN, 52, W - MARGIN, 52], fill=RULE, width=2)

    # --- giant date (heavy grotesque sans, biggest type on the page)
    date = "TUESDAY 24 NOVEMBER 2026"
    f_date = fit_font(sans_b, date, CW, 78)
    d.text(((W - d.textlength(date, font=f_date)) / 2, 60), date,
           font=f_date, fill=INK)
    d.line([MARGIN, 132, W - MARGIN, 132], fill=INK, width=3)

    # --- deck: the 3 top stories
    f_deck = serif_i(21)
    deck = ("Tokyo rallies as markets reopen  \u00b7  Gukesh\u2013Sindarov "
            "title match begins  \u00b7  CAS to rule on Senegal's AFCON appeal")
    lines = wrap(d, deck, f_deck, CW)
    y = 140
    for ln in lines[:2]:
        d.text(((W - d.textlength(ln, font=f_deck)) / 2, y), ln,
               font=f_deck, fill=INK)
        y += 24

    # --- BY THE NUMBERS strip
    y0 = 190
    bw = CW // 5
    f_num = sans_b(30)
    f_numlab = sans(13)
    for i, (fig, lab) in enumerate(NUMBERS):
        x0 = MARGIN + i * bw
        d.rectangle([x0 + 2, y0, x0 + bw - 2, y0 + 56], outline=RULE, width=1)
        d.text(((x0 + bw / 2 - d.textlength(fig, font=f_num) / 2), y0 + 4),
               fig, font=f_num, fill=RED)
        d.text(((x0 + bw / 2 - d.textlength(lab, font=f_numlab) / 2), y0 + 36),
               lab, font=f_numlab, fill=MUTED)
    y = y0 + 56

    # --- region bar
    f_reg = sans_b(14)
    reg = ("EUROPE 5   \u00b7   ASIA-PACIFIC 5   \u00b7   OCEANIA 7   \u00b7   "
           "AMERICAS 5   \u00b7   WORLD 3        25 STORIES  \u00b7  4 CONTINENTS")
    d.text(((W - d.textlength(reg, font=f_reg)) / 2, y + 8), reg,
           font=f_reg, fill=INK)
    d.line([MARGIN, y + 30, W - MARGIN, y + 30], fill=RULE, width=1)

    # --- UTC timeline (honest labels: CAS has no exact time)
    y = y + 38
    line_y = y + 30
    d.line([MARGIN, line_y, W - MARGIN, line_y], fill=INK, width=2)
    f_time = sans_b(14)
    f_tdesc = sans(13)
    xs = [MARGIN + 60, MARGIN + 330, MARGIN + 600, MARGIN + 850]
    for (tm, desc), cx in zip(TIMELINE, xs):
        d.ellipse([cx - 6, line_y - 6, cx + 6, line_y + 6], fill=RED)
        d.text((cx - d.textlength(tm, font=f_time) / 2, line_y - 28), tm,
               font=f_time, fill=INK)
        dl = wrap(d, desc, f_tdesc, 210)
        ly = line_y + 12
        for ln in dl[:2]:
            d.text((cx - d.textlength(ln, font=f_tdesc) / 2, ly), ln,
                   font=f_tdesc, fill=MUTED)
            ly += 16
    y = line_y + 46

    # --- 3 lead panels
    gap = 16
    pw = (CW - 2 * gap) // 3
    art_h = 108
    f_leadtag = sans_b(12)
    f_leadtitle = sans_b(18)
    f_leadbody = sans(14)
    for i, lead in enumerate(LEADS):
        x0 = MARGIN + i * (pw + gap)
        ART[lead["art"]](d, x0, y, pw, art_h)
        ly = y + art_h + 8
        d.text((x0, ly), lead["tag"], font=f_leadtag, fill=RED)
        ly += 16
        for ln in wrap(d, lead["title"], f_leadtitle, pw)[:2]:
            d.text((x0, ly), ln, font=f_leadtitle, fill=INK)
            ly += 21
        for ln in wrap(d, lead["body"], f_leadbody, pw)[:2]:
            d.text((x0, ly), ln, font=f_leadbody, fill=MUTED)
            ly += 17
    y = y + art_h + 8 + 16 + 42 + 34 + 4
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=1)

    # --- 10 numbered cards, 2 columns x 5 rows
    y += 10
    col_w = CW // 2
    row_h = 36
    f_cardn = sans_b(20)
    f_cardtitle = sans_b(16)
    f_cardbody = sans(13)
    for i, card in enumerate(CARDS):
        col, row = i % 2, i // 2
        x0 = MARGIN + col * col_w
        cy = y + row * row_h
        d.text((x0, cy + 2), str(card["n"]), font=f_cardn, fill=RED)
        tx = x0 + 30
        d.rounded_rectangle([tx, cy + 2, tx + 30, cy + 32],
                            radius=5, fill=card["color"])
        draw_glyph(d, tx, cy + 2, 30, card["glyph"], card["color"])
        hx = tx + 38
        tw = col_w - 30 - 38 - 8
        d.text((hx, cy + 1), ellipsize(d, card["title"], f_cardtitle, tw),
               font=f_cardtitle, fill=INK)
        d.text((hx, cy + 20), ellipsize(d, card["body"], f_cardbody, tw),
               font=f_cardbody, fill=MUTED)
    y = y + 5 * row_h + 6

    # --- map (left) + ALSO list (right); ALSO rows anchored to the
    #     label row, not to the map row (previous overlap defect).
    map_x0, map_y0 = MARGIN, y
    map_w, map_h = 470, 146
    also_x0 = MARGIN + 492
    f_lab = sans_b(12)
    d.text((map_x0, map_y0), "WHERE IT HAPPENED", font=f_lab, fill=RED)
    d.text((also_x0, map_y0), "ALSO \u2014 MONDAY 23 NOVEMBER", font=f_lab,
           fill=RED)
    # dotted map
    mx0, my0 = map_x0, map_y0 + 22
    cw_, ch_ = map_w / 72.0, (map_h - 26) / 36.0
    for gy in range(36):
        for gx in range(72):
            if in_land(gx + 0.5, gy + 0.5):
                px = mx0 + gx * cw_ + cw_ / 2
                py = my0 + gy * ch_ + ch_ / 2
                d.ellipse([px - 1.6, py - 1.4, px + 1.6, py + 1.4],
                          fill=(120, 110, 95))
    f_pin = sans_b(10)
    for lon, lat, label, side, dy in PINS:
        gx = (lon + 180) / 5.0
        gy = (90 - lat) / 5.0
        px = mx0 + gx * cw_
        py = my0 + gy * ch_
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED, outline=INK)
        lw = d.textlength(label, font=f_pin)
        if side == "l":
            lx = max(mx0, px - lw - 8)
        else:
            lx = min(mx0 + map_w - lw, px + 8)
        d.rectangle([lx - 2, py + dy - 1, lx + lw + 2, py + dy + 11],
                    fill=PAPER)
        d.text((lx, py + dy), label, font=f_pin, fill=INK)
    # ALSO rows, anchored to the label row
    f_also = sans(14)
    ay = map_y0 + 24
    for i, item in enumerate(ALSO):
        ry = ay + i * 22
        d.text((also_x0, ry), f"{i + 1}.", font=sans_b(14), fill=RED)
        d.text((also_x0 + 22, ry), item, font=f_also, fill=INK)
    y = map_y0 + map_h + 10

    # --- DATE CHECK box
    d.rectangle([MARGIN, y, W - MARGIN, y + 54], outline=INK, width=1)
    d.text((MARGIN + 10, y + 6), "DATE CHECK \u2014 honestly dated: these "
           "happened Monday 23 or Sunday 22 November, not today.",
           font=sans_b(12), fill=RED)
    f_dc = sans(13)
    f_dctag = sans_b(10)
    for i, (item, when) in enumerate(DATE_CHECK):
        col, row = i % 3, i // 3
        x0 = MARGIN + 10 + col * 318
        cy = y + 24 + row * 15
        txt = f"\u2022 {item}"
        tw = d.textlength(txt, font=f_dc)
        tagw = d.textlength(when, font=f_dctag)
        while tw + 8 + tagw > 306 and len(item) > 10:
            item = item[:-1]
            txt = f"\u2022 {item}\u2026"
            tw = d.textlength(txt, font=f_dc)
        d.text((x0, cy), txt, font=f_dc, fill=INK)
        d.text((x0 + tw + 8, cy), when, font=f_dctag, fill=MUTED)
    y = y + 54 + 8

    # --- sources line
    f_src = sans(12)
    src = ("Sources: wire reports and official statements, 24 Nov 2026  \u00b7  "
           "Press time 00:00 UTC  \u00b7  25 stories  \u00b7  4 continents")
    d.text((MARGIN, y), src, font=f_src, fill=MUTED)
    y = y + 16

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print(f"wrote {out}  content bottom y={y}")


if __name__ == "__main__":
    main()
