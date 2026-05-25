"""Generate 1200x630 Open Graph / Twitter share cards for cascadelocalseo.com.

One branded card per page (homepage + vertical landing pages). Reuses the
Cascade "C" mark from generate_favicon.py and the site's brand palette so the
share image matches the site exactly.
"""
from __future__ import annotations
import os
from PIL import Image, ImageDraw, ImageFont
from generate_favicon import draw_mark
from generate_vertical_pages import VERTICALS

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "public")
os.makedirs(OUT_DIR, exist_ok=True)

# Brand palette (matches public/cascade.css)
GREEN_DARK = (10, 61, 36)       # #0a3d24
GREEN_DARKER = (6, 37, 20)      # #062514
CREAM = (247, 245, 240)         # #f7f5f0
CREAM_SOFT = (201, 218, 201)    # #c9dac9
GOLD = (218, 190, 121)          # #dabe79
MINT = (182, 226, 197)          # #b6e2c5

W, H = 1200, 630
PAD = 80

GEORGIA_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


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


def make_card(filename, headline, subline):
    img = Image.new("RGB", (W, H), GREEN_DARK)

    # Diagonal gradient: darker top-left -> base green bottom-right
    grad = Image.new("RGB", (W, H))
    gpx = grad.load()
    for y in range(H):
        for x in range(W):
            t = (x / W + y / H) / 2
            gpx[x, y] = (
                int(GREEN_DARKER[0] * (1 - t) + GREEN_DARK[0] * t),
                int(GREEN_DARKER[1] * (1 - t) + GREEN_DARK[1] * t),
                int(GREEN_DARKER[2] * (1 - t) + GREEN_DARK[2] * t),
            )
    img.paste(grad, (0, 0))
    d = ImageDraw.Draw(img)

    # Gold accent rule along the bottom
    d.rectangle([0, H - 10, W, H], fill=GOLD)

    # Header: C mark + wordmark
    mark_size = 92
    mark = draw_mark(mark_size)
    img.paste(mark, (PAD, PAD), mark)
    word_f = font(ARIAL_BOLD, 34)
    wm_y = PAD + (mark_size - 34) // 2 - 4
    d.text((PAD + mark_size + 22, wm_y), "Cascade Local SEO", font=word_f, fill=CREAM)

    # Headline (Georgia bold, large, wrapped)
    head_f = font(GEORGIA_BOLD, 76)
    lines = wrap(d, headline, head_f, W - 2 * PAD)
    line_h = 88
    block_h = len(lines) * line_h
    y = PAD + mark_size + 70
    for ln in lines:
        d.text((PAD, y), ln, font=head_f, fill=CREAM)
        y += line_h

    # Subline (Arial, soft cream)
    sub_f = font(ARIAL, 30)
    sub_lines = wrap(d, subline, sub_f, W - 2 * PAD)
    y += 14
    for ln in sub_lines:
        d.text((PAD, y), ln, font=sub_f, fill=CREAM_SOFT)
        y += 42

    # Footer: domain
    dom_f = font(ARIAL_BOLD, 28)
    d.text((PAD, H - 10 - 28 - 34), "cascadelocalseo.com", font=dom_f, fill=MINT)

    out = os.path.join(OUT_DIR, filename)
    img.save(out, "PNG")
    print("wrote", filename, img.size)


def main():
    make_card(
        "og-default.png",
        "A free, specific local SEO audit.",
        "Where you actually rank, your three biggest gaps, and a 60-day plan. No pitch attached.",
    )
    # One card per vertical, driven by the same source of truth as the pages.
    for slug, v in VERTICALS.items():
        make_card(f"og-{slug}.png", v["og_headline"], v["og_subline"])


if __name__ == "__main__":
    main()
