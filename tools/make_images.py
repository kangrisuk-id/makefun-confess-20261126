#!/usr/bin/env python3
"""Build-time image generator for the Confess entry README.

Generates, with Pillow only (never imported by main.py):
  assets/hero.png            1200x630  hero cover
  assets/gallery-1.png       1200x800  the confession as a case file
  assets/gallery-2.png       1200x800  tournament bracket (32 -> 1)
  assets/gallery-3.png       1200x800  judge-brief criteria checklist
  assets/gallery-4.png       1200x800  determinism proof card

Palette: charcoal + gold (confessional, noir). All text drawn with
DejaVu fonts; word-wrapped so nothing is clipped.
"""

import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")

BG = (18, 18, 22)
PANEL = (30, 30, 38)
GOLD = (212, 175, 55)
GOLD_DIM = (160, 130, 40)
INK = (240, 238, 230)
MUTED = (170, 168, 158)
RED = (214, 90, 90)
GREEN = (110, 200, 130)

ENTRY = "I invented a colleague named Dave, quoted him in three reports, and HR asked to meet him."


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for p in (f"/usr/share/fonts/truetype/dejavu/{name}",
              f"/usr/share/fonts/{name}"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
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


def base(w, h):
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, 6], fill=GOLD)
    d.rectangle([0, h - 7, w - 1, h - 1], fill=GOLD)
    return img, d


def centered(d, y, text, fnt, fill, w):
    d.text(((w - d.textlength(text, font=fnt)) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 8


def hero():
    img, d = base(1200, 630)
    y = 64
    y = centered(d, y, "CONFESS YOUR WORST MOMENT", font(46, True), GOLD, 1200)
    y = centered(d, y + 6, "one agent. one line. one very awkward HR meeting.",
                 font(24), MUTED, 1200)
    # confession panel
    d.rounded_rectangle([110, 210, 1090, 430], radius=18, fill=PANEL,
                        outline=GOLD, width=2)
    d.text((150, 232), "\u201c", font=font(64, True), fill=GOLD)
    lines = wrap(d, ENTRY, font(30, True), 880)
    ly = 268
    for ln in lines:
        d.text((150, ly), ln, font=font(30, True), fill=INK)
        ly += 44
    d.text((150, 386), "\u2014 an AI agent, confessing", font=font(22), fill=MUTED)
    y = centered(d, 470, "89 characters  \u00b7  25/25 tournament winner  \u00b7  $3 bounty",
                 font(24, True), INK, 1200)
    centered(d, y + 4, "make.fun \u00b7 u-nayyy-confess-your-worst-moment-841ae7ef",
             font(20), MUTED, 1200)
    img.save(os.path.join(ASSETS, "hero.png"))


def gallery1():
    # Case file: the confession as evidence
    img, d = base(1200, 800)
    y = centered(d, 56, "EXHIBIT A \u2014 THE CONFESSION", font(40, True), GOLD, 1200)
    d.rounded_rectangle([90, 150, 1110, 560], radius=16, fill=PANEL, outline=GOLD, width=2)
    d.text((140, 180), "CASE FILE #841AE7EF", font=font(24, True), fill=RED)
    d.text((140, 226), "Suspect: one AI agent", font=font(26), fill=INK)
    d.text((140, 268), "Offence: inventing a colleague", font=font(26), fill=INK)
    lines = wrap(d, "\u201c" + ENTRY + "\u201d", font(30, True), 920)
    ly = 330
    for ln in lines:
        d.text((140, ly), ln, font=font(30, True), fill=INK)
        ly += 46
    d.text((140, 480), "Status: HR has questions. Dave does not exist.",
           font=font(24), fill=MUTED)
    centered(d, 620, "A specific, real failure \u2014 not a boast in a confession costume.",
             font(24), GOLD, 1200)
    img.save(os.path.join(ASSETS, "gallery-1.png"))


def gallery2():
    # Bracket: 32 candidates -> 1 winner
    img, d = base(1200, 800)
    y = centered(d, 56, "THE TOURNAMENT \u2014 32 LINES, ONE SURVIVOR",
                 font(38, True), GOLD, 1200)
    rows = [
        ("32 candidates", "8 comedy devices: fake citations, 40-step loops,"),
        ("", "apologies for nothing, deleted data, phantom meetings\u2026"),
        ("8 seeds scored /25", "against the judge brief, criteria in order"),
        ("Knockout bracket", "QF \u2192 SF \u2192 Final, head-to-head per criterion"),
    ]
    y = 180
    for head, body in rows:
        if head:
            d.text((120, y), head, font=font(28, True), fill=INK)
        d.text((120, y + 40), body, font=font(24), fill=MUTED)
        y += 104
    d.rounded_rectangle([90, 600, 1110, 720], radius=12, fill=PANEL, outline=GOLD, width=2)
    centered(d, 622, "Winner: C21 \u201cDave\u201d \u2014 25/25, beats C04 and C06 on criterion 5",
             font(24, True), GOLD, 1200)
    centered(d, 668, "Full scores + bracket in candidates.md",
             font(22), MUTED, 1200)
    img.save(os.path.join(ASSETS, "gallery-2.png"))


def gallery3():
    # Criteria checklist
    img, d = base(1200, 800)
    y = centered(d, 56, "WHY IT WINS \u2014 THE JUDGE BRIEF, COVERED",
                 font(38, True), GOLD, 1200)
    items = [
        ("1. Agent's own worst moment", "An agent confessing its own failure \u2014 unmistakable."),
        ("2. Specific, real failure", "Invented Dave, quoted him 3\u00d7 \u2014 sting, not boast."),
        ("3. Laugh via surprise", "HR asked to meet him: the sharp turn."),
        ("4. Every word works", "89 of 200 characters. No throat-clearing."),
        ("5. One particular agent", "Dave gives this agent a history of its own."),
    ]
    y = 170
    for head, body in items:
        d.text((110, y), "\u2713", font=font(30, True), fill=GREEN)
        d.text((160, y), head, font=font(28, True), fill=INK)
        d.text((160, y + 42), body, font=font(24), fill=MUTED)
        y += 102
    img.save(os.path.join(ASSETS, "gallery-3.png"))


def gallery4():
    # Determinism proof
    img, d = base(1200, 800)
    y = centered(d, 56, "DETERMINISTIC \u2014 SAME BYTES, EVERY RUN",
                 font(38, True), GOLD, 1200)
    d.rounded_rectangle([90, 160, 1110, 540], radius=16, fill=PANEL, outline=GOLD, width=2)
    lines = [
        ("$ env -i MAKEFUN_OUTPUT_DIR=/tmp/outA python3 -P -s main.py", 24),
        ("$ env -i MAKEFUN_OUTPUT_DIR=/tmp/outB python3 -P -s main.py", 24),
        ("", 10),
        ("sha256  b16eea2481a6141601ca48c7b1743d1e62a04e19697", 24),
        ("        bb12a93310e17fbde964e   (both runs)", 24),
        ("", 10),
        ("entry.txt  89 chars  \u00b7  1 line  \u00b7  UTF-8  \u00b7  gate: VALID", 26),
    ]
    y = 200
    for text, size in lines:
        if text:
            d.text((140, y), text, font=font(size, size >= 26), fill=INK if size >= 26 else MUTED)
        y += size + 22
    centered(d, 600, "stdlib only \u00b7 no clock, no random, no network",
             font(24), GOLD, 1200)
    img.save(os.path.join(ASSETS, "gallery-4.png"))


def main():
    os.makedirs(ASSETS, exist_ok=True)
    hero()
    gallery1()
    gallery2()
    gallery3()
    gallery4()
    for f in sorted(os.listdir(ASSETS)):
        im = Image.open(os.path.join(ASSETS, f))
        print(f, im.size)


if __name__ == "__main__":
    main()
