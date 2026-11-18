#!/usr/bin/env python3
"""Draw the news-image-20261118 entry: an editorial infographic summing up
Wednesday 18 November 2026's world news in one 1024x1024 PNG.

Stories verified from reporting published on 18 Nov 2026 (NY Post, SCMP,
DW, ANI, Arab News, Financial Times, Times of India). No network needed.
Run: python3 make_image.py  ->  writes entry.png next to this file.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (245, 241, 230)
INK = (20, 33, 61)
NAVY = (20, 33, 61)
GOLD = (233, 196, 106)
RED = (178, 34, 34)
GREY = (90, 90, 84)
CARD = (255, 255, 255)
BORDER = (216, 210, 192)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 38)
F_DATE = font("DejaVuSans-Bold.ttf", 27)
F_TAG = font("DejaVuSans-Bold.ttf", 19)
F_KICK = font("DejaVuSans-Bold.ttf", 20)
F_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_BODY = font("DejaVuSans.ttf", 20)
F_SRC = font("DejaVuSans.ttf", 15)
F_FOOT = font("DejaVuSans-Bold.ttf", 18)
F_FOOT2 = font("DejaVuSans.ttf", 14)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_globe(d, cx, cy, r, color, w=3):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=w)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=color, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=color, width=2)


def draw_bridge(d, x, y, s, color):
    # two towers, deck, suspension arc between the tower tops
    d.line([x, y + 0.62 * s, x + s, y + 0.62 * s], fill=color, width=5)
    for tx in (x + 0.18 * s, x + 0.72 * s):
        d.line([tx, y + 0.15 * s, tx, y + 0.62 * s], fill=color, width=5)
    d.arc([x + 0.18 * s, y - 0.35 * s, x + 0.72 * s, y + 0.75 * s], 0, 180,
          fill=color, width=4)
    for sx in (0.32, 0.45, 0.58):
        d.line([x + sx * s, y + 0.32 * s, x + sx * s, y + 0.62 * s],
               fill=color, width=2)


def draw_radar(d, x, y, s, color):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    d.ellipse([cx - r / 2, cy - r / 2, cx + r / 2, cy + r / 2],
              outline=color, width=2)
    d.line([cx, cy, cx + r * 0.8, cy - r * 0.6], fill=color, width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=color)
    for bx, by in ((cx - r * 0.55, cy + r * 0.3), (cx + r * 0.5, cy + r * 0.55)):
        d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=color)


def draw_flags(d, x, y, s, color):
    for i, fc in enumerate(((220, 60, 60), (40, 120, 200), (40, 160, 90),
                            (230, 180, 40))):
        px = x + (0.12 + 0.24 * i) * s
        d.line([px, y + 0.2 * s, px, y + 0.85 * s], fill=color, width=4)
        d.polygon([(px, y + 0.2 * s), (px + 0.2 * s, y + 0.3 * s),
                   (px, y + 0.42 * s)], fill=fc)


def draw_parliament(d, x, y, s, color):
    d.polygon([(x + 0.08 * s, y + 0.38 * s), (x + 0.5 * s, y + 0.08 * s),
               (x + 0.92 * s, y + 0.38 * s)], fill=color)
    for i in range(3):
        cx = x + (0.22 + 0.28 * i) * s
        d.rectangle([cx - 0.05 * s, y + 0.44 * s, cx + 0.05 * s, y + 0.78 * s],
                    fill=color)
    d.rectangle([x + 0.08 * s, y + 0.78 * s, x + 0.92 * s, y + 0.88 * s],
                fill=color)


def draw_euro(d, x, y, s, color):
    f = font("DejaVuSans-Bold.ttf", int(s * 0.85))
    d.text((x + s / 2, y + s / 2), "\u20ac", font=f, fill=color, anchor="mm")


def draw_cricket(d, x, y, s, color):
    # bat: rotated rounded rectangle; ball: red circle with seam
    bat = Image.new("RGBA", (int(s), int(s)), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bat)
    bd.rounded_rectangle([0.40 * s, 0.06 * s, 0.66 * s, 0.72 * s],
                         radius=int(0.07 * s), fill=(205, 155, 95))
    bd.rectangle([0.47 * s, 0.00 * s, 0.59 * s, 0.12 * s], fill=(120, 80, 40))
    bat = bat.rotate(32, resample=Image.BICUBIC, center=(s / 2, s / 2))
    d._image.paste(bat, (int(x), int(y)), bat)
    d.ellipse([x + 0.10 * s, y + 0.60 * s, x + 0.36 * s, y + 0.86 * s],
              fill=(178, 34, 34), outline=(255, 255, 255), width=2)


ICONS = {"bridge": draw_bridge, "radar": draw_radar, "flags": draw_flags,
         "parliament": draw_parliament, "euro": draw_euro,
         "cricket": draw_cricket}

STORIES = [
    dict(kick="UKRAINE  \u2022  WAR", color=(37, 99, 235), icon="bridge",
         head="Kerch Bridge hit for a second day in record drone barrage",
         body=("Ukraine fired 1,441 drones overnight \u2014 the biggest "
               "attack of the war. A road span of the Crimea bridge "
               "collapsed, severing the link."),
         src="NY Post  \u2022  SCMP  \u2022  DW"),
    dict(kick="MIDDLE EAST  \u2022  US\u2013IRAN", color=(220, 38, 38),
         icon="radar",
         head="Iran strikes US radar in Bahrain; US hits back",
         body=("Iranian drones hit a US military radar site in Bahrain. "
               "The US hit back with strikes on an IRGC missile site "
               "on Qeshm Island."),
         src="ANI  \u2022  Arab News"),
    dict(kick="ASIA  \u2022  DIPLOMACY", color=(13, 148, 136), icon="flags",
         head="Trump lands in Manila for Quad talks",
         body=("Trump arrived in Manila for Quad talks ahead of a China "
               "visit; PM Modi urged a peaceful Indo-Pacific "
               "at the East Asia Summit."),
         src="Times of India  \u2022  ANI"),
    dict(kick="ISRAEL  \u2022  POLITICS", color=(124, 58, 237),
         icon="parliament",
         head="Eisenkot tapped to form government, bypassing Netanyahu",
         body=("President Herzog asked ex-army chief Gadi Eisenkot to "
               "form the next government. The Knesset elected "
               "Matan Kahana as Speaker."),
         src="Arab News"),
    dict(kick="EUROPE  \u2022  ECONOMY", color=(217, 119, 6), icon="euro",
         head="EU to borrow \u20ac45bn to plug Ukraine's budget gap",
         body=("The European Commission plans to raise \u20ac45bn on "
               "capital markets to cover Ukraine's projected \u20ac70bn "
               "shortfall next year."),
         src="Financial Times"),
    dict(kick="SPORT  \u2022  CRICKET", color=(22, 163, 74), icon="cricket",
         head="Dhoni calls time on his IPL playing career",
         body=("MS Dhoni announced his retirement from the IPL and will "
               "become Chennai Super Kings' mentor."),
         src="Times of India"),
]

FOOTER = ("ALSO TODAY  \u2014  Cyclone Akvan strengthens  \u2022  Markets "
          "slide ahead of Nvidia results  \u2022  Canada\u2013China extend "
          "trade deals")
FOOTER2 = "Sources: NY Post, SCMP, DW, ANI, Arab News, Financial Times, Times of India"


def draw_panel(d, x, y, w, h, st):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                        outline=BORDER, width=1)
    # accent bar
    d.rounded_rectangle([x, y, x + w, y + 7], radius=3, fill=st["color"])
    d.rectangle([x, y + 4, x + w, y + 7], fill=st["color"])
    # icon box top-right (small, clear of the headline below it)
    ix, iy, isz = x + w - 66, y + 14, 48
    d.rounded_rectangle([ix, iy, ix + isz, iy + isz], radius=10,
                        fill=st["color"])
    ICONS[st["icon"]](d, ix + 5, iy + 5, isz - 10, (255, 255, 255))
    # kicker (kept clear of the icon)
    d.text((x + 18, y + 24), st["kick"], font=F_KICK, fill=st["color"])
    # headline (max 2 lines), starting below the icon row
    hl = wrap(d, st["head"], F_HEAD, w - 36)
    hy = y + 72
    for line in hl[:2]:
        d.text((x + 18, hy), line, font=F_HEAD, fill=INK)
        hy += 33
    # body (max 3 lines)
    bl = wrap(d, st["body"], F_BODY, w - 36)
    by = hy + 6
    for line in bl[:3]:
        d.text((x + 18, by), line, font=F_BODY, fill=(51, 51, 51))
        by += 26
    # source
    d.text((x + 18, y + h - 30), st["src"], font=F_SRC, fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 124], fill=NAVY)
    draw_globe(d, 968, 62, 30, GOLD)
    d.text((28, 20), "THE WORLD IN ONE PICTURE", font=F_TITLE, fill=(255, 255, 255))
    d.text((28, 76), "WEDNESDAY, 18 NOVEMBER 2026", font=F_DATE, fill=GOLD)
    d.text((718, 30), "6 STORIES THAT", font=F_TAG, fill=(200, 205, 220))
    d.text((718, 54), "DEFINED THE DAY", font=F_TAG, fill=(200, 205, 220))
    d.text((718, 84), "ONE DAY \u2022 ONE IMAGE", font=F_TAG, fill=GOLD)
    d.rectangle([0, 124, W, 130], fill=RED)
    # grid of panels
    mx, gap = 16, 12
    pw = (W - 2 * mx - gap) // 2
    top, bot = 146, 946
    ph = (bot - top - 2 * gap) // 3
    for i, st in enumerate(STORIES):
        cx = mx + (i % 2) * (pw + gap)
        cy = top + (i // 2) * (ph + gap)
        draw_panel(d, cx, cy, pw, ph, st)
    # footer (shrink ticker font until it fits)
    d.rectangle([0, 958, W, H], fill=NAVY)
    fsize = 18
    while fsize > 12:
        ff = font("DejaVuSans-Bold.ttf", fsize)
        if d.textlength(FOOTER, font=ff) <= W - 56:
            break
        fsize -= 1
    d.text((28, 968), FOOTER, font=ff, fill=(255, 255, 255))
    d.text((28, 996), FOOTER2, font=F_FOOT2, fill=(180, 185, 200))
    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
