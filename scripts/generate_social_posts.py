"""Generate the Cascade Local SEO Instagram launch set.

Feed tiles + carousel slides (1080x1080) + story frames (1080x1920), all on the
dark brand system from generate_og_image.py:
- deep forest gradient bg + faint blueprint grid + gold glow + gold->ocean stripe
- Bricolage Grotesque (display) / IBM Plex Sans (body) / JetBrains Mono (eyebrow + CTA)
- the ocean-bordered wave mark (generate_favicon.draw_mark)

No emoji in any baked text (these TTFs have no emoji glyphs); add IG stickers in-app.
Outputs to ../social-assets/ (NOT public/, so they are not served by the site).
"""
from __future__ import annotations
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from PIL import Image, ImageDraw, ImageFont
from generate_favicon import draw_mark

FONTS_DIR = os.path.join(HERE, "fonts")
OUT_DIR = os.path.join(HERE, "..", "social-assets")
os.makedirs(OUT_DIR, exist_ok=True)

BG = (6, 37, 20)
BG_2 = (10, 61, 36)
INK = (239, 228, 204)
INK_SOFT = (182, 197, 184)
INK_FAINT = (122, 140, 130)
GOLD = (218, 190, 121)
OCEAN = (74, 196, 224)
GOLD_DARK = (6, 37, 20)

PAD = 90

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


def base_bg(w, h):
    img = Image.new("RGB", (w, h), BG)
    grad = Image.new("RGB", (w, h)); gpx = grad.load()
    for y in range(h):
        for x in range(w):
            t = (x / w + y / h) / 2
            gpx[x, y] = (int(BG[0] * (1 - t) + BG_2[0] * t),
                         int(BG[1] * (1 - t) + BG_2[1] * t),
                         int(BG[2] * (1 - t) + BG_2[2] * t))
    img.paste(grad, (0, 0))
    grid = Image.new("RGBA", (w, h), (0, 0, 0, 0)); gd = ImageDraw.Draw(grid)
    gc = (GOLD[0], GOLD[1], GOLD[2], 14)
    for x in range(0, w, 108):
        gd.line([(x, 0), (x, h)], fill=gc, width=1)
    for y in range(0, h, 108):
        gd.line([(0, y), (w, y)], fill=gc, width=1)
    img.paste(grid, (0, 0), grid)
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0)); gld = ImageDraw.Draw(glow)
    cx, cy = int(w * 0.9), int(h * 1.02)
    for r, a in [(760, 12), (560, 18), (380, 24), (240, 30)]:
        gld.ellipse([cx - r, cy - int(r * 0.8), cx + r, cy + int(r * 0.8)],
                    fill=(GOLD[0], GOLD[1], GOLD[2], a))
    img.paste(glow, (0, 0), glow)
    sh = 10; stripe = Image.new("RGB", (w, sh)); spx = stripe.load()
    for x in range(w):
        t = x / max(1, w - 1)
        spx[x, 0] = (int(GOLD[0] * (1 - t) + OCEAN[0] * t),
                     int(GOLD[1] * (1 - t) + OCEAN[1] * t),
                     int(GOLD[2] * (1 - t) + OCEAN[2] * t))
    for y in range(1, sh):
        for x in range(w):
            spx[x, y] = spx[x, 0]
    img.paste(stripe, (0, h - sh))
    return img


def header(d, img, top):
    ms = 96; mark = draw_mark(ms); img.paste(mark, (PAD, top), mark)
    wf = font(BRICOLAGE_BOLD, 38); wy = top + (ms - 38) // 2 - 2
    d.text((PAD + ms + 22, wy), "Cascade Local SEO", font=wf, fill=INK)
    ww = d.textlength("Cascade Local SEO", font=wf)
    d.text((PAD + ms + 22 + ww, wy), ".", font=wf, fill=GOLD)
    return top + ms


def eyebrow_row(d, text, y, max_w):
    ef = font(JET_MONO, 22)
    d.line([(PAD, y + 13), (PAD + 44, y + 13)], fill=GOLD, width=2)
    d.text((PAD + 58, y), text.upper(), font=ef, fill=GOLD)


def corner_mark(d, img):
    ms = 60; mark = draw_mark(ms); img.paste(mark, (1080 - PAD - ms, PAD - 4), mark)


def footer(d, w, h, accent, swipe=True):
    ff = font(JET_MONO, 22)
    if swipe:
        d.text((PAD, h - PAD - 22), "SWIPE →", font=ff, fill=accent)
    dom = "cascadelocalseo.com"; dw = d.textlength(dom, font=ff)
    d.text((w - PAD - dw, h - PAD - 22), dom, font=ff, fill=OCEAN)


def make_tile(filename, eyebrow, headline, subline, cta, accent=GOLD):
    W = H = 1080
    img = base_bg(W, H); d = ImageDraw.Draw(img)
    header(d, img, PAD)
    eby = PAD + 96 + 60
    eyebrow_row(d, eyebrow, eby, W - 2 * PAD)
    hf = font(BRICOLAGE_BOLD, 78); lh = 88
    y = eby + 66
    for ln in wrap(d, headline, hf, W - 2 * PAD):
        d.text((PAD, y), ln, font=hf, fill=INK); y += lh
    y += 10
    d.line([(PAD, y), (PAD + 120, y)], fill=accent, width=4); y += 36
    sf = font(PLEX_SANS, 34); slh = 46
    for ln in wrap(d, subline, sf, W - 2 * PAD):
        d.text((PAD, y), ln, font=sf, fill=INK_SOFT); y += slh
    cf = font(JET_MONO, 24); ctext = cta.upper()
    tw = d.textlength(ctext, font=cf)
    px = PAD; py = H - PAD - 60
    d.rectangle([px, py, px + tw + 56, py + 56], fill=accent)
    d.text((px + 28, py + 15), ctext, font=cf, fill=GOLD_DARK)
    df = font(JET_MONO, 22); dom = "cascadelocalseo.com"
    dw = d.textlength(dom, font=df)
    d.text((W - PAD - dw, py + 17), dom, font=df, fill=OCEAN)
    out = os.path.join(OUT_DIR, filename); img.save(out, "PNG")
    print(f"wrote {out} {img.size}")


def make_slide(filename, kicker, index_label, title, body, accent=GOLD):
    """Numbered carousel point slide (1080x1080)."""
    W = H = 1080
    img = base_bg(W, H); d = ImageDraw.Draw(img)
    eyebrow_row(d, kicker, PAD, W - 2 * PAD)
    corner_mark(d, img)
    idxf = font(BRICOLAGE_BOLD, 150)
    d.text((PAD, PAD + 62), index_label, font=idxf, fill=accent)
    tf = font(BRICOLAGE_BOLD, 60); ty = PAD + 62 + 168
    for ln in wrap(d, title, tf, W - 2 * PAD):
        d.text((PAD, ty), ln, font=tf, fill=INK); ty += 70
    ty += 14
    d.line([(PAD, ty), (PAD + 100, ty)], fill=accent, width=4); ty += 34
    bf = font(PLEX_SANS, 34); blh = 46
    for ln in wrap(d, body, bf, W - 2 * PAD):
        d.text((PAD, ty), ln, font=bf, fill=INK_SOFT); ty += blh
    footer(d, W, H, accent)
    out = os.path.join(OUT_DIR, filename); img.save(out, "PNG")
    print(f"wrote {out} {img.size}")


def make_list_slide(filename, kicker, title, items, accent=GOLD):
    """Title + bulleted list carousel slide (1080x1080)."""
    W = H = 1080
    img = base_bg(W, H); d = ImageDraw.Draw(img)
    eyebrow_row(d, kicker, PAD, W - 2 * PAD)
    corner_mark(d, img)
    tf = font(BRICOLAGE_BOLD, 66); ty = PAD + 96
    for ln in wrap(d, title, tf, W - 2 * PAD):
        d.text((PAD, ty), ln, font=tf, fill=INK); ty += 76
    ty += 30
    itf = font(PLEX_SANS, 40)
    for it in items:
        d.rectangle([PAD, ty + 14, PAD + 18, ty + 32], fill=accent)
        d.text((PAD + 42, ty), it, font=itf, fill=INK); ty += 72
    footer(d, W, H, accent)
    out = os.path.join(OUT_DIR, filename); img.save(out, "PNG")
    print(f"wrote {out} {img.size}")


def make_cta_slide(filename, kicker, title, body, cta, accent=GOLD):
    """Closing CTA carousel slide (1080x1080)."""
    W = H = 1080
    img = base_bg(W, H); d = ImageDraw.Draw(img)
    eyebrow_row(d, kicker, PAD, W - 2 * PAD)
    corner_mark(d, img)
    tf = font(BRICOLAGE_BOLD, 72); ty = PAD + 130
    for ln in wrap(d, title, tf, W - 2 * PAD):
        d.text((PAD, ty), ln, font=tf, fill=INK); ty += 82
    ty += 14
    d.line([(PAD, ty), (PAD + 120, ty)], fill=accent, width=4); ty += 36
    bf = font(PLEX_SANS, 34); blh = 46
    for ln in wrap(d, body, bf, W - 2 * PAD):
        d.text((PAD, ty), ln, font=bf, fill=INK_SOFT); ty += blh
    cf = font(JET_MONO, 24); ctext = cta.upper(); tw = d.textlength(ctext, font=cf)
    px = PAD; py = H - PAD - 60
    d.rectangle([px, py, px + tw + 56, py + 56], fill=accent)
    d.text((px + 28, py + 15), ctext, font=cf, fill=GOLD_DARK)
    df = font(JET_MONO, 22); dom = "cascadelocalseo.com"; dw = d.textlength(dom, font=df)
    d.text((W - PAD - dw, py + 17), dom, font=df, fill=OCEAN)
    out = os.path.join(OUT_DIR, filename); img.save(out, "PNG")
    print(f"wrote {out} {img.size}")


def make_story(filename, eyebrow, headline, body, cue, accent=GOLD):
    W, H = 1080, 1920
    img = base_bg(W, H); d = ImageDraw.Draw(img)
    top = 150
    header(d, img, top)
    eby = top + 96 + 64
    eyebrow_row(d, eyebrow, eby, W - 2 * PAD)
    hf = font(BRICOLAGE_BOLD, 80); lh = 90
    y = eby + 70
    for ln in wrap(d, headline, hf, W - 2 * PAD):
        d.text((PAD, y), ln, font=hf, fill=INK); y += lh
    y += 12
    d.line([(PAD, y), (PAD + 120, y)], fill=accent, width=4); y += 40
    bf = font(PLEX_SANS, 38); blh = 52
    for ln in wrap(d, body, bf, W - 2 * PAD):
        d.text((PAD, y), ln, font=bf, fill=INK_SOFT); y += blh
    cf = font(JET_MONO, 26)
    d.text((PAD, 1500), cue.upper(), font=cf, fill=accent)
    df = font(JET_MONO, 22)
    d.text((PAD, 1560), "cascadelocalseo.com", font=df, fill=OCEAN)
    out = os.path.join(OUT_DIR, filename); img.save(out, "PNG")
    print(f"wrote {out} {img.size}")


def make_profile_circle(filename, w=1080):
    """Borderless full-bleed mark for the IG profile pic. The ocean-bordered icon
    gets its corners + border clipped by IG's circle crop; this fills the circle
    cleanly: forest field + faint center glow + the gold wave centered."""
    from generate_favicon import cubic_bezier
    img = Image.new("RGB", (w, w), BG); px = img.load()
    for y in range(w):
        for x in range(w):
            t = (x / w + y / w) / 2
            px[x, y] = (int(BG[0] * (1 - t) + BG_2[0] * t),
                        int(BG[1] * (1 - t) + BG_2[1] * t),
                        int(BG[2] * (1 - t) + BG_2[2] * t))
    glow = Image.new("RGBA", (w, w), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    cx = cy = w // 2
    for r, a in [(520, 8), (380, 10), (240, 13)]:
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(GOLD[0], GOLD[1], GOLD[2], a))
    img.paste(glow, (0, 0), glow)
    d = ImageDraw.Draw(img)
    k = (w * 0.62) / 22.0          # wave spans ~62% width, well inside the circle
    ox = w / 2 - 13 * k; oy = w / 2 - 13 * k
    def P(x, y):
        return (ox + x * k, oy + y * k)
    pts = cubic_bezier(P(2, 18), P(7, 8), P(11, 8), P(13, 13), steps=60) + \
          cubic_bezier(P(13, 13), P(15, 18), P(19, 18), P(24, 8), steps=60)[1:]
    sw = int(w * 0.062)
    d.line(pts, fill=GOLD, width=sw, joint="curve")
    r = sw // 2
    for ex, ey in [pts[0], pts[-1]]:
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=GOLD)
    out = os.path.join(OUT_DIR, filename); img.save(out, "PNG")
    print(f"wrote {out} {img.size}")


def make_fiverr_cover(filename, eyebrow, headline, sub, badge, accent=GOLD, wordmark=True):
    """1280x769 Fiverr gig gallery cover. NO url/domain (Fiverr bans external contact on gig images).
    wordmark=False draws the mark only (for off-brand gigs that shouldn't carry the SEO wordmark)."""
    W, H = 1280, 769
    img = base_bg(W, H); d = ImageDraw.Draw(img)
    if wordmark:
        header(d, img, PAD)
    else:
        ms = 96; mk = draw_mark(ms); img.paste(mk, (PAD, PAD), mk)
    eby = PAD + 96 + 50
    eyebrow_row(d, eyebrow, eby, W - 2 * PAD)
    hf = font(BRICOLAGE_BOLD, 82); lh = 90
    y = eby + 58
    for ln in wrap(d, headline, hf, W - 2 * PAD):
        d.text((PAD, y), ln, font=hf, fill=INK); y += lh
    y += 14
    d.line([(PAD, y), (PAD + 120, y)], fill=accent, width=4); y += 36
    sf = font(PLEX_SANS, 34); slh = 46
    for ln in wrap(d, sub, sf, W - 2 * PAD - 80):
        d.text((PAD, y), ln, font=sf, fill=INK_SOFT); y += slh
    cf = font(JET_MONO, 26); bt = badge.upper(); tw = d.textlength(bt, font=cf)
    px = PAD; py = H - PAD - 58
    d.rectangle([px, py, px + tw + 56, py + 58], fill=accent)
    d.text((px + 28, py + 16), bt, font=cf, fill=GOLD_DARK)
    out = os.path.join(OUT_DIR, filename); img.save(out, "PNG")
    print(f"wrote {out} {img.size}")


def main():
    # --- 3 feed tiles / carousel COVERS (1080x1080) ---
    make_tile("ig-1-positioning.png", "Found and recommended",
              "Getting found isn't enough anymore.",
              "Now you have to get recommended, by the map pack and the AI answers your customers ask.",
              "Free audit · link in bio", accent=GOLD)
    make_tile("ig-2-mappack.png", "Local SEO playbook",
              "4 reasons you're #4 on the map.",
              "The top 3 take 70%+ of local clicks. Here's what quietly keeps service businesses out of it.",
              "Swipe for the fixes →", accent=OCEAN)
    make_tile("ig-3-aishift.png", "The AI shift",
              "Your next customer may never see the blue links.",
              "They ask AI who's best near them and take the answer. We make sure that answer is you.",
              "Swipe →", accent=GOLD)

    # --- Post 2 carousel inner slides (cover = ig-2-mappack) ---
    K2 = "4 reasons you're #4"
    make_slide("ig-2-slide-01.png", K2, "01", "Your Google profile is thin or stale.",
               "Half-filled categories, no services listed, old hours. Google can't recommend what it can't read.", OCEAN)
    make_slide("ig-2-slide-02.png", K2, "02", "Fewer and older reviews than the top 3.",
               "Volume and recency both count. The businesses above you usually have more reviews, and fresher ones.", OCEAN)
    make_slide("ig-2-slide-03.png", K2, "03", "No recent photos or posts.",
               "An active profile signals an active business. Quiet profiles quietly slide down the pack.", OCEAN)
    make_slide("ig-2-slide-04.png", K2, "04", "Your site never says which city you serve.",
               "If your pages don't name your service area, Google guesses. Guessing costs you the map pack.", OCEAN)
    make_cta_slide("ig-2-slide-05-cta.png", K2, "Fix these, and #4 becomes top 3.",
                   "The free audit shows which one is costing you the most calls right now.",
                   "Free audit · link in bio", OCEAN)

    # --- Post 3 carousel inner slides (cover = ig-3-aishift) ---
    K3 = "The AI shift"
    make_slide("ig-3-slide-01.png", K3, "01", "They're asking AI, not scrolling Google.",
               "'Best med spa near me?' now gets answered by ChatGPT and Google's AI summary, before anyone scrolls.", GOLD)
    make_slide("ig-3-slide-02.png", K3, "02", "AI names a few. Not ten links.",
               "You're either in the short list it reads back, or you're invisible. There is no page 2 in an AI answer.", GOLD)
    make_list_slide("ig-3-slide-03-list.png", K3, "What gets you named:",
                    ["Strong, recent reviews", "A complete, consistent profile",
                     "Same name, address, phone everywhere", "Content that answers real questions"], GOLD)
    make_cta_slide("ig-3-slide-04-cta.png", K3, "We build for found AND recommended.",
                   "Your free audit includes an AI-readiness score, so you know where you stand.",
                   "Free audit · link in bio", GOLD)

    # --- Post 4 (Mon): your GBP is 80% of local SEO (education carousel) ---
    make_tile("ig-4-gbp.png", "Local SEO playbook",
              "Your Google profile is 80% of local SEO.",
              "And most owners fill out barely half of it. Here's the part that quietly costs you the map pack.",
              "Swipe for the gaps →", accent=GOLD)
    K4 = "Your GBP, the 40% you skip"
    make_slide("ig-4-slide-01.png", K4, "01", "List every service you offer.",
               "Google matches searches to the services you list. An empty Services section makes you invisible for half the work you do.", GOLD)
    make_slide("ig-4-slide-02.png", K4, "02", "Fill in Products and menu.",
               "Photos, items, and prices feed both the map pack and what AI reads back about you. Most profiles leave it blank.", GOLD)
    make_slide("ig-4-slide-03.png", K4, "03", "Seed your own Q&A.",
               "You can ask AND answer questions on your own profile. Leave it empty and random guesses rank instead of your real answers.", GOLD)
    make_slide("ig-4-slide-04.png", K4, "04", "Post weekly, keep it fresh.",
               "An active profile signals an active business. Quiet profiles slide down the pack while competitors keep posting.", GOLD)
    make_cta_slide("ig-4-slide-05-cta.png", K4, "You're using maybe 40% of your profile.",
                   "The free audit shows exactly which fields are empty and which ones move the map pack first.",
                   "Free audit · link in bio", GOLD)

    # --- Post 5 (Wed): what the top 3 on the map have in common (honest leaderboard proof) ---
    make_tile("ig-5-top3.png", "Proof, done honestly",
              "What the top 3 on the map have in common.",
              "We rank 1,000+ local markets in public. The pattern is the same almost everywhere, and it isn't a prettier website.",
              "Swipe →", accent=OCEAN)
    K5 = "What the top 3 share"
    make_slide("ig-5-slide-01.png", K5, "01", "More reviews, fresher ones.",
               "Volume and recency both count. The top 3 keep a steady drip of new reviews. The spots below them went quiet.", OCEAN)
    make_slide("ig-5-slide-02.png", K5, "02", "A complete, consistent profile.",
               "Categories, services, hours, and photos all filled in. Google ranks the listing it can fully read with more confidence.", OCEAN)
    make_slide("ig-5-slide-03.png", K5, "03", "Same name, address, phone everywhere.",
               "When your details match across the web, Google trusts you more. Mismatches quietly cost you the map pack.", OCEAN)
    make_cta_slide("ig-5-slide-04-cta.png", K5, "See your market on the live board.",
                   "Our public Google Maps Power Rankings, no login and no pitch. Look up what the top 3 in your category have that you don't.",
                   "Link in bio · /rankings", OCEAN)

    # --- Post 6 (Fri): the agent-run model (founder single) ---
    make_tile("ig-6-agents.png", "How this works",
              "I run this agency with AI agents.",
              "They find the businesses, run the audits, and draft the fixes. A human approves before anything sends, so the savings reach you, not an agency markup.",
              "Curious? DM me.", accent=OCEAN)

    # --- 3 story frames (1080x1920) --- add IG stickers over the clear lower third ---
    make_story("ig-story-1-poll.png", "Welcome",
               "We get local businesses found AND recommended.",
               "On Google's map pack and the AI answers your customers now ask. Map pack. Google. ChatGPT.",
               "Vote below ↓  do you know what you rank for?", accent=GOLD)
    make_story("ig-story-2-tip.png", "Quick win",
               "Add 3 photos to your Google profile this week.",
               "Profiles with fresh photos get more calls and direction requests. Two minutes, real impact.",
               "Try it this week", accent=OCEAN)
    make_story("ig-story-3-audit.png", "Free audit",
               "Where do you stand on Google + AI?",
               "A free, specific audit: your rank, ratings, top 3 competitors, and an AI-readiness score. No signup.",
               "Tap the link ↓", accent=GOLD)

    # --- 6 more story frames (added 2026-05-31): rotating stock so stories don't repeat ---
    make_story("ig-story-4-tip-reviews.png", "Quick win",
               "Reply to every review, even the 5-star ones.",
               "Google reads your replies as a ranking signal, and it shows future customers you're paying attention. Two minutes each.",
               "Reply to 5 this week", accent=OCEAN)
    make_story("ig-story-5-tip-category.png", "Quick win",
               "Pick the most specific primary category.",
               "Your primary Google category moves the map pack more than almost anything. Most owners pick something vague and leave money on the table.",
               "Check yours today", accent=GOLD)
    make_story("ig-story-6-tip-services.png", "Quick win",
               "List every service you offer.",
               "Google can only rank you for the services you actually list. An empty Services section makes you invisible for half your work.",
               "Add 3 services today", accent=OCEAN)
    make_story("ig-story-7-found-recommended.png", "The wedge",
               "Found is not the same as recommended.",
               "Found is showing up in the map pack. Recommended is the AI naming you when someone asks who's best. You need both gates open.",
               "Which are you missing?", accent=GOLD)
    make_story("ig-story-8-proof-board.png", "Proof, in public",
               "We rank 1,000+ local markets in public.",
               "Real Google Maps standings, no login and no pitch. Look up your category and see what the top 3 actually have.",
               "Find your market ↓", accent=OCEAN)
    make_story("ig-story-9-building.png", "Building in public",
               "Month 1, building this in public.",
               "Solo founder, AI agents doing the grunt work, zero clients yet. Everything here is real data or best practice, never invented results.",
               "Follow the build", accent=GOLD)

    # --- 4 Reel hook/cover frames (1080x1920); B-roll = screen recordings per cascade-ig-reels.md ---
    make_story("ig-reel-1-cover.png", "Reel · The AI shift",
               "I asked AI for the best dentist near me.",
               "Watch who it actually named. It wasn't page one of Google.",
               "Is that you? Free audit in bio", accent=GOLD)
    make_story("ig-reel-2-cover.png", "Reel · 30-second fix",
               "The one Google setting most owners get wrong.",
               "Primary vs secondary categories, and why it quietly tanks your map-pack spot.",
               "Fix yours today", accent=OCEAN)
    make_story("ig-reel-3-cover.png", "Reel · Real data",
               "We rank local businesses in public.",
               "Watch me pull a live board and show what the top 3 actually look like.",
               "Find your market ↓", accent=GOLD)
    make_story("ig-reel-4-cover.png", "Reel · Behind the scenes",
               "An agency that runs on AI agents.",
               "Watch an audit build itself, with a human approval gate before anything sends.",
               "Follow the build", accent=OCEAN)

    # --- IG profile picture (borderless, circle-crop friendly) ---
    make_profile_circle("ig-profile-circle.png")


if __name__ == "__main__":
    main()
