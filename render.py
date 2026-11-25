#!/usr/bin/env python3
"""Render the news-image-20261124 v2 front page: the FULL Tuesday 24 Nov 2026.

Fresh re-author for the v2 rebuild (post-opening session, 25 Nov 2026).
Same winning formula as v1: giant date, deck, numbers strip, region bar,
UTC timeline, 3 illustrated leads, 10 numbered cards, map strip, ALSO list,
DATE CHECK box, sources line. All stories verified against wire dates;
Monday/Sunday items sit only in DATE CHECK, honestly dated.
Deterministic: no randomness, no clock, no network.
"""
import hashlib

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MX = 36                      # side margin
CW = W - 2 * MX              # content width = 952

PAPER = (244, 239, 228)
INK = (26, 26, 26)
RED = (178, 34, 30)
BLUE = (31, 78, 121)
TEAL = (14, 110, 96)
GOLD = (198, 152, 40)
MUTED = (112, 106, 94)
RULE = (186, 178, 158)
PANEL = (250, 246, 236)
MAPLAND = (216, 205, 180)

DJ = "/usr/share/fonts/truetype/dejavu/"
LB = "/usr/share/fonts/truetype/liberation/"


def f(path, size):
    return ImageFont.truetype(path, size)


SANS = DJ + "DejaVuSans.ttf"
SANSB = DJ + "DejaVuSans-Bold.ttf"
SERIF = DJ + "DejaVuSerif.ttf"
SERIFB = DJ + "DejaVuSerif-Bold.ttf"
SERIFI = LB + "LiberationSerif-Italic.ttf"

# ---------------------------------------------------------------- stories
# region tags: Europe / Asia-Pacific / Oceania / Americas / World
LEADS = [
    ("SENEGAL CROWNED AGAIN", "World · Football",
     "CAS unanimously reinstates Senegal as AFCON 2025 champions and sets "
     "aside CAF's forfeit ruling. The 1-0 final win over Morocco stands.",
     "trophy", "World"),
    ("GUKESH HOLDS SINDAROV", "Europe · Chess",
     "Game 1 of the world title match ends in a 38-move Berlin draw in "
     "Geneva. The two 20-year-olds share the point: 0.5-0.5.",
     "chess", "Europe"),
    ("ASIA RALLIES, WALL ST SPLITS", "Markets",
     "Nikkei jumps 2.6% to 60,279 as Tokyo reopens. By the US close the "
     "Dow hits 50,019 while chips drag the Nasdaq down 1.5%.",
     "bars", "Asia-Pacific"),
]

NUMBERS = [
    ("60,279", "NIKKEI  +2.6%"),
    ("50,019", "DOW  +0.85%"),
    ("-1.48%", "NASDAQ"),
    ("103.3", "US CONFIDENCE"),
    ("$3,554", "GOLD  -2.7%"),
]

TIMELINE = [
    ("MORNING", "Asia markets rally as Tokyo reopens"),
    ("AFTERNOON", "CAS reinstates Senegal as AFCON champions"),
    ("EVENING", "Wall Street splits: Dow up, Nasdaq down"),
]

CARDS = [
    ("CHIPS GIVE BACK THE RALLY",
     "Chip stocks slide: SOX falls 7.9%, Analog Devices drops 17%, "
     "Nvidia gives up 5.9%.",
     "Americas"),
    ("CONFIDENCE JUMPS",
     "US consumer confidence rises 11.4 points to 103.3, its highest "
     "reading since January 2025.",
     "Americas"),
    ("CANBERRA PACT",
     "Australia and Singapore sign a carbon storage treaty, a supplies "
     "pact and a joint AI statement.",
     "Oceania"),
    ("BOUGAINVILLE DEBATE OPENS",
     "PNG's parliament begins debating ratification of the 2019 "
     "independence vote, won 98% to yes.",
     "Asia-Pacific"),
    ("NATO WATCHES THE SKIES",
     "NATO chief Rutte vows to defend space after reports of a Russian "
     "orbital nuclear weapon.",
     "Europe"),
    ("GERMANY GETS DELTA",
     "Berlin is first to access Ukraine's Delta battlefield system; "
     "more interceptors to follow.",
     "Europe"),
    ("SANOFI'S $41BN BET",
     "Sanofi agrees to buy US biotech Insmed, the biggest biotech deal "
     "in nearly three years.",
     "Europe"),
    ("EBOLA TEAMS TRAPPED",
     "Fighting in DR Congo's Ituri leaves WHO responders sheltering in "
     "a hospital for a second day.",
     "World"),
    ("GAZA STRIKES",
     "Israeli airstrikes kill at least six Palestinians in Gaza on "
     "Tuesday, medics and police officials say.",
     "World"),
    ("FIVE AN HOUR",
     "UN: 47,000 women were killed by a partner or family member in "
     "2025, five every hour.",
     "World"),
]

ALSO = [
    ("Iraq PM orders Baghdad to run Kurdish-area oilfields.", "World"),
    ("FDA clears the first drug for limb-girdle muscular dystrophy.", "Americas"),
    ("Astronomers find the most distant glowing black hole yet.", "World"),
    ("Nepal hit by a 5.6 quake near the Chinese border.", "Asia-Pacific"),
    ("Colombia car bomb wrecks buildings in Villavicencio.", "Americas"),
    ("China opens Tiangong station to its first foreign astronaut.", "Asia-Pacific"),
    ("Trump warns Iran of a \u201cvery traumatic\u201d outcome if talks fail.", "World"),
    ("Victorian Labor posts its worst poll since 1902.", "Oceania"),
    ("Storms lash four Australian states.", "Oceania"),
    ("Hobart stadium bill put at $1.23bn.", "Oceania"),
    ("Macquarie word of the year: \u201cpervert glasses\u201d.", "Oceania"),
    ("GTA VI counts 60 birds in its trailer world.", "Americas"),
    ("Pennsylvania records a ninth measles death.", "Americas"),
]

# Honestly dated: these did NOT happen on Tuesday.
DATE_CHECK_MON = [
    "Nvidia reinstates Huang", "India gives Nepal $1.62bn",
    "Zelenskiy warns of new Russian strikes", "Moscow warns Estonia of \u201copen war\u201d",
    "US drone helped catch \u201cChapo Isidro\u201d", "Cikande toll confirmed for the 24th",
    "US blacklists Megaspeed", "Two states sue SpaceX over Grok",
    "Denmark backs \u201cghetto law\u201d", "Iran flogs Ahmadi (74 lashes)",
    "Israeli strike kills UNRWA worker", "Trump pauses Iowa blast",
]
DATE_CHECK_SUN = ["COP31 ends with no deal", "Alcaraz wins the ATP Finals"]

SOURCES = ("Sources: ChessBase · Reuters · Swingfolio · UN News · MFA Singapore · "
           "The Conversation · The Kyiv Independent · PM Australia")

REGIONS = ["Europe", "Asia-Pacific", "Oceania", "Americas", "World"]


def region_counts():
    counts = {r: 0 for r in REGIONS}
    for _, _, _, _, r in LEADS:
        counts[r] += 1
    for _, _, r in CARDS:
        counts[r] += 1
    for _, r in ALSO:
        counts[r] += 1
    return counts


# ---------------------------------------------------------------- helpers
def wrap(draw, text, font, max_w):
    """Greedy word wrap to a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_rule(draw, x0, x1, y, color=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def draw_trophy(draw, x, y, w, h):
    """Senegal flag bands + a flat gold trophy."""
    band = w // 3
    draw.rectangle([x, y, x + band, y + h], fill=(0, 110, 70))
    draw.rectangle([x + band, y, x + 2 * band, y + h], fill=(245, 205, 40))
    draw.rectangle([x + 2 * band, y, x + w, y + h], fill=(205, 35, 40))
    cx = x + w // 2
    top = y + 12
    # cup bowl
    draw.polygon([(cx - 26, top), (cx + 26, top), (cx + 18, top + 30),
                  (cx - 18, top + 30)], fill=GOLD)
    draw.arc([cx - 34, top + 2, cx - 12, top + 26], 90, 270, fill=GOLD, width=5)
    draw.arc([cx + 12, top + 2, cx + 34, top + 26], -90, 90, fill=GOLD, width=5)
    draw.rectangle([cx - 4, top + 30, cx + 4, top + 48], fill=GOLD)
    draw.rectangle([cx - 18, top + 48, cx + 18, top + 54], fill=GOLD)


def draw_chess(draw, x, y, w, h):
    """8x4 board strip fitted inside the box + one white piece."""
    sq = h // 4
    bw = sq * 8
    ox = x + (w - bw) // 2
    oy = y + (h - sq * 4) // 2
    for r in range(4):
        for c in range(8):
            col = (30, 30, 30) if (r + c) % 2 == 0 else (232, 224, 208)
            draw.rectangle([ox + c * sq, oy + r * sq,
                            ox + (c + 1) * sq, oy + (r + 1) * sq], fill=col)
    px, py = ox + 5 * sq + sq // 2, oy + 1 * sq + sq // 2
    r = max(sq // 2 - 1, 3)
    draw.ellipse([px - r, py - r, px + r, py + r], fill=(250, 248, 240),
                 outline=INK, width=2)
    draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=INK)


def draw_bars(draw, x, y, w, h):
    """Rising bars, last one red and falling."""
    draw.rectangle([x, y, x + w, y + h], fill=(233, 226, 210))
    vals = [0.45, 0.62, 0.55, 0.85, 0.38]
    bw = w // 7
    for i, v in enumerate(vals):
        bx = x + 14 + i * (bw + 6)
        bh = int(v * (h - 22))
        col = RED if i == 4 else TEAL
        draw.rectangle([bx, y + h - 10 - bh, bx + bw, y + h - 10], fill=col)
    draw.line([(x + 10, y + 14), (x + w - 14, y + h - 34)], fill=RED, width=3)


ART = {"trophy": draw_trophy, "chess": draw_chess, "bars": draw_bars}


# ---------------------------------------------------------------- render
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 26

    # masthead kicker
    kick_f = f(SANSB, 15)
    n_stories = len(LEADS) + len(CARDS) + len(ALSO)
    counts = region_counts()
    right = "%d STORIES · %d REGIONS" % (n_stories, len(REGIONS))
    d.text((MX, y), "THE WORLD IN ONE DAY", font=kick_f, fill=INK)
    rw = d.textlength(right, font=kick_f)
    d.text((MX + CW - rw, y), right, font=kick_f, fill=RED)
    y += 22

    # giant date
    date_f = f(SANSB, 60)
    date = "24 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, y), date, font=date_f, fill=INK)
    y += 72
    sub_f = f(SANSB, 14)
    sub = "T U E S D A Y"
    sw = d.textlength(sub, font=sub_f)
    d.text(((W - sw) / 2, y), sub, font=sub_f, fill=RED)
    y += 22
    draw_rule(d, MX, MX + CW, y, color=INK, width=2)
    y += 6
    draw_rule(d, MX, MX + CW, y, color=INK, width=1)
    y += 10

    # deck line
    deck_f = f(SERIFI, 17)
    deck = ("Senegal crowned again. Gukesh holds Sindarov. "
            "Wall Street splits as chips slide.")
    for line in wrap(d, deck, deck_f, CW):
        lw = d.textlength(line, font=deck_f)
        d.text(((W - lw) / 2, y), line, font=deck_f, fill=INK)
        y += 22
    y += 8

    # numbers strip
    draw_rule(d, MX, MX + CW, y)
    y += 8
    val_f = f(SANSB, 21)
    lab_f = f(SANSB, 10)
    col_w = CW // 5
    for i, (val, lab) in enumerate(NUMBERS):
        cx = MX + i * col_w
        vw = d.textlength(val, font=val_f)
        d.text((cx + (col_w - vw) / 2, y), val, font=val_f, fill=INK)
        lw = d.textlength(lab, font=lab_f)
        d.text((cx + (col_w - lw) / 2, y + 26), lab, font=lab_f, fill=MUTED)
        if i:
            d.line([(cx, y), (cx, y + 40)], fill=RULE, width=1)
    y += 48
    draw_rule(d, MX, MX + CW, y)
    y += 10

    # region bar
    reg_f = f(SANSB, 11)
    parts = ["%s %d" % (r.upper(), counts[r]) for r in REGIONS]
    reg_line = "  ·  ".join(parts)
    rw = d.textlength(reg_line, font=reg_f)
    d.text(((W - rw) / 2, y), reg_line, font=reg_f, fill=BLUE)
    y += 20
    draw_rule(d, MX, MX + CW, y)
    y += 8

    # UTC timeline
    tl_lab_f = f(SANSB, 10)
    tl_txt_f = f(SERIF, 11)
    for i, (lab, txt) in enumerate(TIMELINE):
        cx = MX + i * (CW // 3)
        d.text((cx, y), lab, font=tl_lab_f, fill=RED)
        d.text((cx, y + 13), txt, font=tl_txt_f, fill=INK)
    y += 30
    draw_rule(d, MX, MX + CW, y)
    y += 10

    # 3 lead panels
    lead_w = (CW - 2 * 20) // 3
    head_f = f(SANSB, 14)
    body_f = f(SERIF, 11)
    tag_f = f(SANSB, 9)
    lead_top = y
    lead_bottom = y
    for i, (head, tag, body, art, _reg) in enumerate(LEADS):
        x = MX + i * (lead_w + 20)
        d.rectangle([x, y, x + lead_w, y + 68], outline=RULE, width=1)
        ART[art](d, x + 1, y + 1, lead_w - 2, 66)
        by = y + 76
        d.text((x, by), tag, font=tag_f, fill=RED)
        by += 13
        for line in wrap(d, head, head_f, lead_w):
            d.text((x, by), line, font=head_f, fill=INK)
            by += 17
        for line in wrap(d, body, body_f, lead_w):
            d.text((x, by), line, font=body_f, fill=INK)
            by += 14
        lead_bottom = max(lead_bottom, by)
    y = lead_bottom + 8
    draw_rule(d, MX, MX + CW, y)
    y += 10

    # 10 numbered cards, 3 columns, rows of 4/3/3
    num_f = f(SANSB, 13)
    chead_f = f(SANSB, 12)
    cbody_f = f(SERIF, 11)
    rows = [CARDS[0:3], CARDS[3:6], CARDS[6:9], CARDS[9:10]]
    for row in rows:
        row_h = 0
        heights = []
        for idx, (head, body, _reg) in enumerate(row):
            lines_h = wrap(d, head, chead_f, lead_w - 30)
            lines_b = wrap(d, body, cbody_f, lead_w - 30)
            heights.append(16 + 15 * len(lines_h) + 14 * len(lines_b))
        row_h = max(heights)
        for idx, (head, body, _reg) in enumerate(row):
            x = MX + idx * (lead_w + 20)
            num = "%02d" % (CARDS.index((head, body, _reg)) + 1)
            d.text((x, y), num, font=num_f, fill=RED)
            by = y + 16
            for line in wrap(d, head, chead_f, lead_w - 30):
                d.text((x + 30, by), line, font=chead_f, fill=INK)
                by += 15
            for line in wrap(d, body, cbody_f, lead_w - 30):
                d.text((x + 30, by), line, font=cbody_f, fill=INK)
                by += 14
        y += row_h + 8
    draw_rule(d, MX, MX + CW, y)
    y += 8

    # (map strip dropped in revision: the blob continents read as vague
    # smudges and the pins sat off their landmasses. The region bar above
    # already carries the geography.)
    draw_rule(d, MX, MX + CW, y)
    y += 8

    # ALSO list, 2 columns
    map_lab_f = f(SANSB, 10)
    d.text((MX, y), "ALSO ON TUESDAY", font=map_lab_f, fill=RED)
    y += 15
    also_f = f(SERIF, 11)
    col2_w = (CW - 20) // 2
    left = ALSO[:7]
    right_items = ALSO[7:]
    max_rows = max(len(left), len(right_items))
    for r in range(max_rows):
        for ci, items in enumerate((left, right_items)):
            if r < len(items):
                txt, _reg = items[r]
                x = MX + ci * (col2_w + 20)
                num = "%02d" % (r + 1 + ci * 7)
                d.text((x, y), num, font=f(SANSB, 10), fill=MUTED)
                d.text((x + 24, y), txt, font=also_f, fill=INK)
        y += 14
    y += 4
    draw_rule(d, MX, MX + CW, y)
    y += 8

    # DATE CHECK box
    dc_f = f(SERIF, 10)
    dc_lab_f = f(SANSB, 10)
    mon = "MON NOV 23: " + "; ".join(DATE_CHECK_MON) + "."
    sun = "SUN NOV 22: " + "; ".join(DATE_CHECK_SUN) + "."
    dc_lines = wrap(d, mon, dc_f, CW - 24) + wrap(d, sun, dc_f, CW - 24)
    box_h = 16 + 14 * len(dc_lines) + 8
    d.rectangle([MX, y, MX + CW, y + box_h], outline=INK, width=1)
    d.text((MX + 12, y + 5), "DATE CHECK \u2014 NOT TUESDAY", font=dc_lab_f,
           fill=RED)
    ly = y + 20
    for line in dc_lines:
        d.text((MX + 12, ly), line, font=dc_f, fill=MUTED)
        ly += 14
    y += box_h + 8

    # sources
    src_f = f(SERIF, 9)
    d.text((MX, y), SOURCES, font=src_f, fill=MUTED)
    y += 13

    print("content bottom y=%d (canvas %d)" % (y, H))
    assert y <= H - 8, "overflow: content bottom %d" % y
    return img


if __name__ == "__main__":
    im = render()
    im.save("entry.png", optimize=True)
    data = open("entry.png", "rb").read()
    print("entry.png %d bytes sha256 %s"
          % (len(data), hashlib.sha256(data).hexdigest()))
