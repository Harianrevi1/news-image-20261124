#!/usr/bin/env python3
"""Render 'The World Today' — Tuesday 24 November 2026.
Vintage broadsheet, 1024x1024 JPEG. Drawn from scratch with PIL:
masthead, one lead story, five story panels, one numbers box.
All six stories verified against Reuters / AP / CNN / Le Monde / WSJ
on 24 Nov 2026 before drawing.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (242, 232, 208)
INK = (26, 23, 18)
RED = (140, 29, 24)
GREEN = (30, 92, 46)
ORANGE = (176, 84, 20)
GREY = (110, 104, 88)
BLUE = (38, 68, 110)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, max_w, leading, color=INK, max_lines=None):
    x, y = xy
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def headline(draw, xy, text, fnt, max_w, leading):
    return para(draw, xy, text, fnt, max_w, leading, color=INK, max_lines=2)


def kicker(draw, xy, text):
    f = font(SANS_B, 13)
    draw.text(xy, text.upper(), font=f, fill=RED)


def rule(draw, x0, y, x1, width=2):
    draw.line([(x0, y), (x1, y)], fill=INK, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- outer frame ----
d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=2)
d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

M = 34  # inner margin

# ---- masthead ----
title = "THE WORLD TODAY"
tf = font(SERIF_B, 76)
tw = d.textlength(title, font=tf)
d.text(((W - tw) / 2, 30), title, font=tf, fill=INK)
rule(d, M, 122, W - M, 3)
rule(d, M, 128, W - M, 1)
date = "TUESDAY, 24 NOVEMBER 2026"
df = font(SERIF_B, 30)
dw = d.textlength(date, font=df)
d.text(((W - dw) / 2, 138), date, font=df, fill=RED)
rule(d, M, 182, W - M, 3)
rule(d, M, 188, W - M, 1)

# ================= LEAD PANEL =================
lx, ly, lw, lh = M, 200, W - 2 * M, 236
d.rectangle([lx, ly, lx + lw, ly + lh], outline=INK, width=2)
kicker(d, (lx + 16, ly + 12), "The Lead  •  Markets")
lead_head = "HUANG IS BACK AT NVIDIA"
hf_size = 40
hf = font(SERIF_B, hf_size)
while d.textlength(lead_head, font=hf) > 578 and hf_size > 28:
    hf_size -= 2
    hf = font(SERIF_B, hf_size)
d.text((lx + 16, ly + 38), lead_head, font=hf, fill=INK)
lead_body = (
    "Nvidia's board reinstated Jensen Huang as chief executive on Monday, "
    "eleven days after he resigned. Shares leapt 31.5% — their best day "
    "since 2003 — adding $952 billion of market value in a single session."
)
para(d, (lx + 16, ly + 92), lead_body, font(SERIF, 17), 560, 22, max_lines=4)

# lead illustration: rising chart + chip, right side
ix0, iy0 = lx + 610, ly + 30
ix1, iy1 = lx + lw - 18, ly + lh - 16
d.rectangle([ix0, iy0, ix1, iy1], outline=GREY, width=1)
# grid lines
for gy in range(iy0 + 30, iy1, 30):
    d.line([(ix0, gy), (ix1, gy)], fill=(200, 188, 160), width=1)
pts = [
    (ix0 + 14, iy1 - 26), (ix0 + 70, iy1 - 52), (ix0 + 120, iy1 - 44),
    (ix0 + 170, iy1 - 78), (ix0 + 215, iy1 - 66), (ix0 + 258, iy1 - 118),
    (ix0 + 300, iy1 - 150),
]
d.line(pts, fill=GREEN, width=5, joint="curve")
# arrowhead
d.polygon([(ix0 + 300, iy1 - 150), (ix0 + 282, iy1 - 146),
           (ix0 + 296, iy1 - 132)], fill=GREEN)
# chip
cx, cy = ix0 + 22, iy0 + 16
d.rectangle([cx, cy, cx + 52, cy + 40], outline=INK, width=2, fill=(210, 198, 170))
d.rectangle([cx + 14, cy + 11, cx + 38, cy + 29], outline=INK, width=1)
for px in range(cx + 6, cx + 48, 10):
    d.line([(px, cy), (px, cy - 7)], fill=INK, width=2)
    d.line([(px, cy + 40), (px, cy + 47)], fill=INK, width=2)
lbl = font(SANS_B, 22)
d.text((ix0 + 92, iy0 + 18), "+31.5%", font=lbl, fill=GREEN)
d.text((ix0 + 92, iy0 + 46), "IN ONE DAY", font=font(SANS_B, 12), fill=INK)

# ================= GRID =================
gx0, gy0 = M, 452
col_w, col_h, gut = 314, 258, 12
col_x = [gx0, gx0 + col_w + gut, gx0 + 2 * (col_w + gut)]
col_w3 = W - M - col_x[2]  # last column width
widths = [col_w, col_w, col_w3]
row_y = [gy0, gy0 + col_h + gut]


def panel(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    return x + 14, y + 10, w - 28


def story_panel(x, y, w, h, kick, head, body, draw_art):
    px, py, pw = panel(x, y, w, h)
    kicker(d, (px, py), kick)
    headline(d, (px, py + 24), head, font(SERIF_B, 23), pw, 27)
    art_y = y + 88
    draw_art(x + 14, art_y, w - 28, 54)
    para(d, (px, art_y + 62), body, font(SERIF, 13.5), pw, 17, max_lines=6)


# --- art helpers ---
def art_chip_ban(x, y, w, h):
    # chip with red prohibition ring
    cx, cy = x + 40, y + h // 2
    d.rectangle([cx - 26, cy - 20, cx + 26, cy + 20], outline=INK, width=2,
                fill=(210, 198, 170))
    for px in range(cx - 18, cx + 20, 9):
        d.line([(px, cy - 20), (px, cy - 27)], fill=INK, width=2)
        d.line([(px, cy + 20), (px, cy + 27)], fill=INK, width=2)
    d.ellipse([cx - 34, cy - 30, cx + 34, cy + 30], outline=RED, width=4)
    d.line([(cx - 24, cy + 24), (cx + 24, cy - 24)], fill=RED, width=4)
    # small containers
    for i, bx in enumerate([x + 110, x + 160, x + 210]):
        d.rectangle([bx, y + 12 + i * 6, bx + 42, y + 44 + i * 6],
                    outline=INK, width=2, fill=(196, 182, 148))
        d.line([(bx, y + 28 + i * 6), (bx + 42, y + 28 + i * 6)], fill=INK, width=1)


def art_fire(x, y, w, h):
    # factory + flames + smoke
    d.rectangle([x + 10, y + 30, x + 120, y + h - 4], outline=INK, width=2,
                fill=(196, 182, 148))
    d.rectangle([x + 130, y + 8, x + 150, y + h - 4], outline=INK, width=2,
                fill=(180, 166, 132))
    for wx in range(x + 22, x + 112, 26):
        d.rectangle([wx, y + 40, wx + 14, y + 54], outline=INK, width=1)
    # flames
    for fx, fh in [(x + 26, 26), (x + 58, 34), (x + 92, 24)]:
        d.polygon([(fx, y + 32), (fx + 8, y + 32 - fh), (fx + 16, y + 32)],
                  fill=ORANGE)
    # smoke
    for sx, sy, sr in [(x + 140, y + 12, 9), (x + 168, y + 6, 11),
                       (x + 200, y + 10, 10), (x + 232, y + 16, 8)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], outline=GREY, width=2)


def art_ship(x, y, w, h):
    # sea + sinking corvette + drone boat
    for wy in [y + 44, y + 52, y + 60]:
        d.line([(x + 6, wy), (x + w - 6, wy)], fill=BLUE, width=2)
    # hull tilted, bow down
    d.polygon([(x + 60, y + 34), (x + 210, y + 22), (x + 230, y + 34),
               (x + 210, y + 44), (x + 70, y + 46)], fill=(120, 110, 88),
              outline=INK)
    d.line([(x + 150, y + 22), (x + 150, y + 4)], fill=INK, width=2)
    d.polygon([(x + 150, y + 4), (x + 172, y + 12), (x + 150, y + 14)],
              fill=RED)
    # smoke plume
    for sx, sy, sr in [(x + 110, y + 10, 7), (x + 128, y + 4, 9),
                       (x + 148, y + 10, 6)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], outline=GREY, width=2)
    # small drone boat
    d.polygon([(x + 20, y + 48), (x + 44, y + 48), (x + 38, y + 56),
               (x + 24, y + 56)], fill=INK)


def art_missiles(x, y, w, h):
    # three impact markers + missile streaks
    d.rectangle([x + 6, y + 6, x + w - 6, y + h - 6], outline=GREY, width=1)
    for mx, my in [(x + 70, y + 26), (x + 150, y + 16), (x + 225, y + 28)]:
        d.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=RED, outline=INK)
        d.ellipse([mx - 12, my - 12, mx + 12, my + 12], outline=RED, width=2)
    # streaks
    d.line([(x + 30, y + 8), (x + 62, y + 20)], fill=INK, width=3)
    d.line([(x + 110, y + 6), (x + 142, y + 12)], fill=INK, width=3)
    d.line([(x + 185, y + 10), (x + 217, y + 22)], fill=INK, width=3)
    d.text((x + 8, y + h - 14), "NOWY LIPOWIEC  •  RUDNIK  •  MOLODYCZ",
           font=font(SANS_B, 9), fill=INK)


def art_blast(x, y, w, h):
    # building facade + starburst blast
    d.rectangle([x + 14, y + 22, x + 120, y + h - 4], outline=INK, width=2,
                fill=(196, 182, 148))
    for wx in range(x + 26, x + 112, 24):
        d.rectangle([wx, y + 30, wx + 12, y + 44], outline=INK, width=1)
    d.rectangle([x + 52, y + 46, x + 82, y + h - 4], outline=INK, width=1)
    # starburst
    bx, by = x + 190, y + 30
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 8, 26
        a = math.radians(ang)
        d.line([(bx + r1 * math.cos(a), by + r1 * math.sin(a)),
                (bx + r2 * math.cos(a), by + r2 * math.sin(a))],
               fill=ORANGE, width=3)
    d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=ORANGE, outline=RED)


# ---- row 1 ----
story_panel(col_x[0], row_y[0], widths[0], col_h,
            "Chips & Sanctions",
            "U.S. BLACKLISTS MEGASPEED",
            "Washington put Singapore cloud firm Megaspeed and six affiliates "
            "in South-East Asia on its Entity List on Monday, over the alleged "
            "diversion of advanced Nvidia AI chips to China.",
            art_chip_ban)
story_panel(col_x[1], row_y[0], widths[1], col_h,
            "Indonesia",
            "26 DEAD IN CANDY FACTORY FIRE",
            "Rescuers in Cikande, Serang, confirmed 26 workers dead after "
            "Saturday's blaze at the PT Fonusa Agung Mulia factory. Eight more "
            "were still missing on Tuesday.",
            art_fire)

story_panel(col_x[2], row_y[0], widths[2], col_h,
            "Ukraine • Libya",
            "KYIV SINKS RUSSIAN WARSHIP OFF LIBYA",
            "Seven Ukrainian sea drones sank the corvette Merkury in Benghazi "
            "harbour on Sunday, Kyiv said. Zelensky also urged four-party peace "
            "talks with Russia, the U.S. and Europe 'as soon as possible'.",
            art_ship)

# ---- row 2 ----
story_panel(col_x[0], row_y[1], widths[0], col_h,
            "Poland • NATO",
            "RUSSIAN MISSILES LAND IN POLAND",
            "Three Russian Kh-101 cruise missiles came down in south-east "
            "Poland on 20 November, prosecutors confirmed. Warsaw called the "
            "incursion a provocation; NATO allies were due to meet on Monday.",
            art_missiles)

story_panel(col_x[1], row_y[1], widths[1], col_h,
            "Colombia",
            "CAR BOMB AND DRONE ATTACKS ROCK COLOMBIA",
            "A car bomb outside the Meta governor's office in Villavicencio "
            "wounded 23 people on Monday night, hours after explosive drones "
            "struck a police base in Cucuta, wounding three civilians.",
            art_blast)

# ---- numbers box ----
nx, ny, nw, nh = col_x[2], row_y[1], widths[2], col_h
d.rectangle([nx, ny, nx + nw, ny + nh], outline=INK, width=2)
d.rectangle([nx, ny, nx + nw, ny + 34], fill=INK)
d.text((nx + 14, ny + 8), "THE DAY IN NUMBERS", font=font(SANS_B, 14),
       fill=PAPER)
nums = [
    ("+31.5%", "Nvidia shares in one day"),
    ("$952bn", "of market value added"),
    ("26", "dead in the Serang fire"),
    ("3", "Kh-101 missiles in Poland"),
    ("23", "wounded in Villavicencio"),
    ("7", "drones sank the Merkury"),
]
yy = ny + 46
for big, small in nums:
    d.text((nx + 14, yy), big, font=font(SERIF_B, 19), fill=RED)
    label_lines = wrap(d, small, font(SERIF, 13.5), nw - 28 - 96)
    ly2 = yy + 3
    for ln in label_lines[:2]:
        d.text((nx + 110, ly2), ln, font=font(SERIF, 13.5), fill=INK)
        ly2 += 16
    yy += 33

# ---- footer ----
foot = ("All stories first reported or confirmed on Tuesday 24 November 2026  •  "
        "Sources: Reuters, AP, CNN, Le Monde, WSJ")
ff = font(SERIF_I, 13)
fw = d.textlength(foot, font=ff)
d.text(((W - fw) / 2, H - 34), foot, font=ff, fill=GREY)

img.save("entry.png", "JPEG", quality=88, optimize=True)
print("saved entry.png")
