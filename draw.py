#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper summary of the world news of
Thursday 19 November 2026. Pure Pillow drawing, no downloaded assets,
so the image is fully our own work. Run: python3 draw.py
Writes entry.png next to this file (1024x1024, well under 1 MiB)."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 24, 39)
RED = (185, 28, 28)
MUTED = (90, 96, 110)
CARD = (255, 255, 255)
LINE = (214, 208, 194)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


F_KICKER = font("DejaVuSans-Bold.ttf", 24)
F_DATE = font("DejaVuSans-Bold.ttf", 54)
F_SUB = font("DejaVuSans.ttf", 23)
F_TAG = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 30)
F_BODY = font("DejaVuSans.ttf", 21)
F_FOOT = font("DejaVuSans.ttf", 18)
F_NUM = font("DejaVuSans-Bold.ttf", 34)

# (tag, colour, headline, summary) -- every fact checked against
# news reports of 19 Nov 2026 (AP, Reuters, Japan Times, Le Monde, NASA).
STORIES = [
    ("DIPLOMACY", (29, 78, 216),
     "Trump, Xi and Putin meet in Shenzhen",
     "First-ever trilateral summit at APEC ends with a joint "
     "\u201cpeace declaration\u201d after 90 minutes of talks."),
    ("JUSTICE", (124, 58, 237),
     "World court: Myanmar committed genocide",
     "The ICJ rules Myanmar guilty of genocide against the Rohingya "
     "\u2014 the UN top court's first verdict of its kind."),
    ("CONFLICT", (185, 28, 28),
     "Houthi missile hits Riyadh's tallest tower",
     "The PIF Tower is damaged as Saudi Arabia reports a new wave "
     "of Houthi attacks launched from Yemen."),
    ("WAR IN EUROPE", (154, 52, 18),
     "Ukraine strikes the Crimea bridge again",
     "Russia says Kyiv attacked the Crimean Bridge for the third "
     "time this week as the war grinds on."),
    ("CULTURE", (4, 120, 87),
     "GTA VI launches after a 13-year wait",
     "Rockstar's blockbuster hits PS5 and Xbox worldwide, scoring "
     "a near-perfect 99 on Metacritic."),
    ("SPACE", (14, 116, 144),
     "Voyager 1 now a light-day from Earth",
     "NASA marks the 1977 probe reaching 16 billion miles out "
     "\u2014 the farthest any human-made object has flown."),
]


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` px."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead band -------------------------------------------------
    d.rectangle([0, 0, W, 158], fill=INK)
    d.rectangle([0, 158, W, 164], fill=RED)
    d.text((48, 20), "THE WORLD IN ONE DAY", font=F_KICKER, fill=(248, 113, 113))
    date_text = "THURSDAY, 19 NOVEMBER 2026"
    date_font = F_DATE
    while d.textlength(date_text, font=date_font) > W - 96 and date_font.size > 40:
        date_font = font("DejaVuSans-Bold.ttf", date_font.size - 2)
    d.text((48, 48), date_text, font=date_font, fill=(255, 255, 255))
    d.text((48, 118), "Six stories that defined the day \u2014 from Shenzhen to deep space",
           font=F_SUB, fill=(203, 213, 225))

    # ---- Story cards ---------------------------------------------------
    top, row_h, gap = 180, 128, 7
    x0, x1 = 48, W - 48
    for i, (tag, colour, head, body) in enumerate(STORIES):
        y0 = top + i * (row_h + gap)
        y1 = y0 + row_h
        d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD,
                            outline=LINE, width=1)
        d.rectangle([x0, y0 + 10, x0 + 8, y1 - 10], fill=colour)
        # Number badge
        cx, cy, r = x0 + 52, y0 + row_h // 2, 30
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
        num = str(i + 1)
        tw = d.textlength(num, font=F_NUM)
        th = d.textbbox((0, 0), num, font=F_NUM)[3]
        d.text((cx - tw / 2, cy - th / 2 - 2), num, font=F_NUM,
               fill=(255, 255, 255))
        # Tag + headline + summary
        tx = x0 + 104
        d.text((tx, y0 + 13), tag, font=F_TAG, fill=colour)
        d.text((tx, y0 + 39), head, font=F_HEAD, fill=INK)
        lines = wrap(d, body, F_BODY, x1 - tx - 24)
        ly = y0 + 79
        for line in lines[:2]:
            d.text((tx, ly), line, font=F_BODY, fill=(55, 65, 81))
            ly += 25

    # ---- Footer --------------------------------------------------------
    foot = "Events of 19 November 2026, all time zones  \u00b7  Sources: AP, Reuters, The Japan Times, Le Monde, NASA"
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, H - 24), foot, font=F_FOOT, fill=MUTED)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
