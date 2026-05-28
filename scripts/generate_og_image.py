"""Generate 1200x630 Open Graph / Twitter share cards for cascadelocalseo.com.

2026-05-28: redesigned to match the new dark brand system —
- Bricolage Grotesque (display) + IBM Plex Sans (body) + JetBrains Mono (eyebrow/footer)
- Parchment + gold + ocean accents on deep forest gradient bg
- Engineering blueprint grid overlay (faint gold lines)
- Gold→ocean side stripe (matches dashboard hero)
- New ocean-bordered wave mark (via generate_favicon.draw_mark)
- Mono eyebrow per card + mono footer URL

One card per page (homepage + vertical landing pages).
"""
from __future__ import annotations
import os
from PIL import Image, ImageDraw, ImageFont
from generate_favicon import draw_mark
from generate_vertical_pages import VERTICALS

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "public")
FONTS_DIR = os.path.join(os.path.dirname(__file__), "fonts")
os.makedirs(OUT_DIR, exist_ok=True)

# Brand palette
BG = (6, 37, 20)              # #062514 deep forest (page bg)
BG_2 = (10, 61, 36)           # #0a3d24 elevated forest
INK = (239, 228, 204)         # #efe4cc parchment (primary type)
INK_SOFT = (182, 197, 184)    # #b6c5b8 sage (secondary type)
INK_FAINT = (122, 140, 130)   # #7a8c82
GOLD = (218, 190, 121)        # #dabe79 action accent
GOLD_SOFT = (244, 227, 181)   # #f4e3b5
OCEAN = (74, 196, 224)        # #4ac4e0 data accent

W, H = 1200, 630
PAD = 72

# Brand fonts (downloaded from Google Fonts to scripts/fonts/)
BRICOLAGE_BOLD = os.path.join(FONTS_DIR, "BricolageGrotesque-Bold.ttf")
PLEX_SANS = os.path.join(FONTS_DIR, "IBMPlexSans-Medium.ttf")
JET_MONO = os.path.join(FONTS_DIR, "JetBrainsMono-Medium.ttf")


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


def make_card(filename, eyebrow, headline, subline):
    img = Image.new("RGB", (W, H), BG)

    # 1) Diagonal gradient: darker top-left → BG_2 bottom-right
    grad = Image.new("RGB", (W, H))
    gpx = grad.load()
    for y in range(H):
        for x in range(W):
            t = (x / W + y / H) / 2
            gpx[x, y] = (
                int(BG[0] * (1 - t) + BG_2[0] * t),
                int(BG[1] * (1 - t) + BG_2[1] * t),
                int(BG[2] * (1 - t) + BG_2[2] * t),
            )
    img.paste(grad, (0, 0))

    # 2) Engineering blueprint grid overlay (faint gold lines every 96px)
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    grid_color = (GOLD[0], GOLD[1], GOLD[2], 14)  # ~5% alpha
    for x in range(0, W, 96):
        gd.line([(x, 0), (x, H)], fill=grid_color, width=1)
    for y in range(0, H, 96):
        gd.line([(0, y), (W, y)], fill=grid_color, width=1)
    img.paste(grid, (0, 0), grid)

    # 3) Soft gold radial glow at bottom-right (dashboard hero accent)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_d = ImageDraw.Draw(glow)
    # Approximate radial glow with a series of concentric ellipses fading out
    cx, cy = int(W * 0.92), int(H * 1.05)
    for r, a in [(700, 12), (550, 18), (380, 24), (240, 30)]:
        glow_d.ellipse([cx - r, cy - int(r * 0.7), cx + r, cy + int(r * 0.7)],
                       fill=(GOLD[0], GOLD[1], GOLD[2], a))
    img.paste(glow, (0, 0), glow)

    # 4) Right-edge stripe: gold→ocean gradient (matches dashboard hero side stripe)
    stripe_w = 8
    stripe = Image.new("RGB", (stripe_w, H))
    spx = stripe.load()
    for y in range(H):
        t = y / max(1, H - 1)
        spx[0, y] = (
            int(GOLD[0] * (1 - t) + OCEAN[0] * t),
            int(GOLD[1] * (1 - t) + OCEAN[1] * t),
            int(GOLD[2] * (1 - t) + OCEAN[2] * t),
        )
    for x in range(1, stripe_w):
        for y in range(H):
            spx[x, y] = spx[0, y]
    img.paste(stripe, (W - stripe_w, 0))

    d = ImageDraw.Draw(img)

    # 5) Header row: mark + wordmark
    mark_size = 84
    mark = draw_mark(mark_size)
    img.paste(mark, (PAD, PAD), mark)
    word_f = font(BRICOLAGE_BOLD, 32)
    wm_y = PAD + (mark_size - 32) // 2 - 2
    # Cascade Local SEO. with gold period
    d.text((PAD + mark_size + 20, wm_y), "Cascade Local SEO", font=word_f, fill=INK)
    word_w = d.textlength("Cascade Local SEO", font=word_f)
    d.text((PAD + mark_size + 20 + word_w, wm_y), ".", font=word_f, fill=GOLD)

    # 6) Mono eyebrow (with leading gold rule, mimicking the homepage compositor mark)
    eyebrow_f = font(JET_MONO, 18)
    eb_y = PAD + mark_size + 50
    rule_len = 36
    rule_x = PAD
    rule_y = eb_y + 10
    d.line([(rule_x, rule_y), (rule_x + rule_len, rule_y)], fill=GOLD, width=1)
    d.text((PAD + rule_len + 14, eb_y), eyebrow.upper(), font=eyebrow_f, fill=GOLD)

    # 7) Headline (Bricolage Bold, large, wrapped, tight letter-spacing implicit in font)
    head_f = font(BRICOLAGE_BOLD, 78)
    lines = wrap(d, headline, head_f, W - 2 * PAD - 60)
    line_h = 88
    y = eb_y + 50
    for ln in lines:
        d.text((PAD, y), ln, font=head_f, fill=INK)
        y += line_h

    # 8) Subline (Plex Sans Medium, sage)
    sub_f = font(PLEX_SANS, 28)
    sub_lines = wrap(d, subline, sub_f, W - 2 * PAD - 60)
    y += 12
    for ln in sub_lines:
        d.text((PAD, y), ln, font=sub_f, fill=INK_SOFT)
        y += 40

    # 9) Footer: domain in mono, ocean color
    foot_f = font(JET_MONO, 22)
    d.text((PAD, H - PAD - 22), "cascadelocalseo.com", font=foot_f, fill=OCEAN)

    out = os.path.join(OUT_DIR, filename)
    img.save(out, "PNG")
    print(f"wrote {filename} {img.size}")


def main():
    # 2026-05-28: subline rewritten honest. The old "60-day plan / no pitch attached" line
    # over-promised — the auto audit gives 3 moves, and the page does have pricing teasers.
    make_card(
        "og-default.png",
        eyebrow="Free local SEO audit",
        headline="A free, specific local SEO audit.",
        subline="Real data on your rank, ratings, and the top 3 competitors — plus what to fix first.",
    )
    # One card per vertical, driven by the same source of truth as the pages.
    for slug, v in VERTICALS.items():
        # Eyebrow uses nav_meta if available (e.g. "Local SEO for med spas"), else a default.
        eb = v.get("nav_meta") or v.get("og_headline", "Local SEO")
        make_card(f"og-{slug}.png", eyebrow=eb, headline=v["og_headline"], subline=v["og_subline"])


if __name__ == "__main__":
    main()
