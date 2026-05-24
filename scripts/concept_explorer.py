"""Render 4 brand-mark concepts side by side at preview size for Jonathan to compare."""
from __future__ import annotations
import os
from PIL import Image, ImageDraw

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "public", "_concepts")
os.makedirs(OUT_DIR, exist_ok=True)

GREEN_DARK = (10, 61, 36, 255)
GREEN_DARKER = (6, 37, 20, 255)
GREEN = (10, 107, 63, 255)
CREAM = (247, 245, 240, 255)
GOLD = (218, 190, 121, 255)
TRANSPARENT = (0, 0, 0, 0)


def make_background(s: int, radius_pct: float = 0.22) -> Image.Image:
    img = Image.new("RGBA", (s, s), TRANSPARENT)
    radius = int(s * radius_pct)
    grad = Image.new("RGBA", (s, s), TRANSPARENT)
    for y in range(s):
        t = y / max(1, s - 1)
        r = int(GREEN_DARKER[0] * (1 - t) + GREEN_DARK[0] * t)
        g = int(GREEN_DARKER[1] * (1 - t) + GREEN_DARK[1] * t)
        b = int(GREEN_DARKER[2] * (1 - t) + GREEN_DARK[2] * t)
        ImageDraw.Draw(grad).line([(0, y), (s, y)], fill=(r, g, b, 255))
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), (s - 1, s - 1)], radius=radius, fill=255)
    img.paste(grad, (0, 0), mask)
    return img


def concept_clean_c(size: int) -> Image.Image:
    s = size * 4
    img = make_background(s)
    cx, cy = s // 2, s // 2
    outer_r = int(s * 0.34)
    stroke_w = int(s * 0.135)
    c = Image.new("RGBA", (s, s), TRANSPARENT)
    cd = ImageDraw.Draw(c)
    cd.ellipse([cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r], fill=CREAM)
    inner_r = outer_r - stroke_w
    cd.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r], fill=TRANSPARENT)
    # right-side wedge to open the C
    wedge = Image.new("L", (s, s), 0)
    wd = ImageDraw.Draw(wedge)
    wr = outer_r + stroke_w
    wd.pieslice([cx - wr, cy - wr, cx + wr, cy + wr], start=-50, end=50, fill=255)
    px = c.load(); wm = wedge.load()
    for y in range(s):
        for x in range(s):
            if wm[x, y] > 0:
                px[x, y] = TRANSPARENT
    img = Image.alpha_composite(img, c)
    return img.resize((size, size), Image.LANCZOS)


def concept_mountains(size: int) -> Image.Image:
    """Three overlapping triangular peaks — Cascade Range silhouette."""
    s = size * 4
    img = make_background(s)
    layer = Image.new("RGBA", (s, s), TRANSPARENT)
    d = ImageDraw.Draw(layer)
    base_y = int(s * 0.78)
    # Back peak (smallest, cream)
    d.polygon([
        (int(s * 0.18), base_y),
        (int(s * 0.42), int(s * 0.30)),
        (int(s * 0.66), base_y),
    ], fill=CREAM)
    # Front peak (larger, cream — overlaps the back peak)
    d.polygon([
        (int(s * 0.34), base_y),
        (int(s * 0.60), int(s * 0.22)),
        (int(s * 0.86), base_y),
    ], fill=CREAM)
    # Snowcap on front peak (gold accent)
    d.polygon([
        (int(s * 0.55), int(s * 0.32)),
        (int(s * 0.60), int(s * 0.22)),
        (int(s * 0.65), int(s * 0.32)),
        (int(s * 0.62), int(s * 0.36)),
        (int(s * 0.58), int(s * 0.36)),
    ], fill=GOLD)
    # Ground line
    d.rectangle([(0, base_y), (s, base_y + int(s * 0.02))], fill=CREAM)
    img = Image.alpha_composite(img, layer)
    return img.resize((size, size), Image.LANCZOS)


def concept_cascade_bars(size: int) -> Image.Image:
    """Five rising bars — rank growth + cascade step pattern."""
    s = size * 4
    img = make_background(s)
    layer = Image.new("RGBA", (s, s), TRANSPARENT)
    d = ImageDraw.Draw(layer)
    n = 5
    pad = int(s * 0.18)
    avail_w = s - 2 * pad
    bar_w = int(avail_w / (n + (n - 1) * 0.35))
    gap = int(bar_w * 0.35)
    max_h = int(s * 0.55)
    min_h = int(s * 0.18)
    base_y = int(s * 0.78)
    for i in range(n):
        x = pad + i * (bar_w + gap)
        h = int(min_h + (max_h - min_h) * (i / (n - 1)))
        # rising bars
        color = CREAM if i < n - 1 else GOLD
        d.rounded_rectangle(
            [(x, base_y - h), (x + bar_w, base_y)],
            radius=int(bar_w * 0.15),
            fill=color,
        )
    img = Image.alpha_composite(img, layer)
    return img.resize((size, size), Image.LANCZOS)


def concept_pin_c(size: int) -> Image.Image:
    """Map pin silhouette whose negative space inside reads as a C."""
    s = size * 4
    img = make_background(s)
    # Pin = teardrop shape: circle on top, triangle pointing down
    layer = Image.new("RGBA", (s, s), TRANSPARENT)
    d = ImageDraw.Draw(layer)
    cx = s // 2
    head_cy = int(s * 0.40)
    head_r = int(s * 0.28)
    # Triangle from circle bottom corners down to pin tip
    tip_y = int(s * 0.86)
    # Tangent points on circle at ~30° below horizontal
    import math
    angle = math.radians(40)
    lx = cx - int(head_r * math.cos(angle))
    rx = cx + int(head_r * math.cos(angle))
    ly = head_cy + int(head_r * math.sin(angle))
    # Pin body polygon
    d.polygon([(lx, ly), (rx, ly), (cx, tip_y)], fill=CREAM)
    d.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], fill=CREAM)
    # Inner C cutout: smaller ring with wedge opening
    inner_r = int(head_r * 0.55)
    stroke = int(head_r * 0.28)
    cutout = Image.new("L", (s, s), 0)
    cd = ImageDraw.Draw(cutout)
    cd.ellipse([cx - inner_r, head_cy - inner_r, cx + inner_r, head_cy + inner_r], fill=255)
    # Subtract inner-inner to leave a ring
    cd.ellipse(
        [cx - (inner_r - stroke), head_cy - (inner_r - stroke),
         cx + (inner_r - stroke), head_cy + (inner_r - stroke)],
        fill=0,
    )
    # Open the right side
    wedge = Image.new("L", (s, s), 0)
    wd = ImageDraw.Draw(wedge)
    wr = inner_r + stroke
    wd.pieslice([cx - wr, head_cy - wr, cx + wr, head_cy + wr], start=-45, end=45, fill=255)
    # Apply cutout to layer: where cutout=255 and wedge=0, knock out the cream
    px = layer.load()
    cm = cutout.load(); wm = wedge.load()
    for y in range(s):
        for x in range(s):
            if cm[x, y] > 0 and wm[x, y] == 0:
                px[x, y] = TRANSPARENT
    img = Image.alpha_composite(img, layer)
    return img.resize((size, size), Image.LANCZOS)


def main():
    size = 256
    concepts = [
        ("A_clean_c", concept_clean_c(size)),
        ("B_mountains", concept_mountains(size)),
        ("C_cascade_bars", concept_cascade_bars(size)),
        ("D_pin_c", concept_pin_c(size)),
    ]
    for name, im in concepts:
        im.save(os.path.join(OUT_DIR, f"{name}.png"))

    # Also save a side-by-side comparison strip
    strip_w = size * 4 + 30
    strip_h = size + 20
    strip = Image.new("RGBA", (strip_w, strip_h), (247, 245, 240, 255))
    x = 10
    for _, im in concepts:
        strip.paste(im, (x, 10), im)
        x += size + 10
    strip.save(os.path.join(OUT_DIR, "comparison.png"))
    print("wrote concepts to:", OUT_DIR)


if __name__ == "__main__":
    main()
