"""Generate Cascade Local SEO brand mark + favicon set.

Mark: rounded-square in deep evergreen with a bold cream "C" whose inner
edge has three stepped notches — reads as the letter C, an audio/ranking
signal, and a cascading waterfall depending on size.
"""
from __future__ import annotations
import os
from PIL import Image, ImageDraw

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "public")
os.makedirs(OUT_DIR, exist_ok=True)

# Brand palette (matches public/index.html CSS vars)
GREEN_DARK = (10, 61, 36, 255)      # #0a3d24
GREEN_DARKER = (6, 37, 20, 255)     # #062514
CREAM = (247, 245, 240, 255)        # #f7f5f0
TRANSPARENT = (0, 0, 0, 0)


def draw_mark(size: int) -> Image.Image:
    """Render the mark at the given square pixel size with crisp edges via 4x supersampling."""
    s = size * 4
    img = Image.new("RGBA", (s, s), TRANSPARENT)
    d = ImageDraw.Draw(img)

    # Rounded-square background with vertical gradient (darker top → lighter bottom)
    radius = int(s * 0.22)
    bg = Image.new("RGBA", (s, s), TRANSPARENT)
    bg_draw = ImageDraw.Draw(bg)
    bg_draw.rounded_rectangle([(0, 0), (s - 1, s - 1)], radius=radius, fill=GREEN_DARK)

    # Vertical gradient overlay (darker at top)
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

    # "C" mark: an annular arc with the right side opened up.
    # Outer ellipse fills 64% of canvas, centered.
    cx, cy = s // 2, s // 2
    outer_r = int(s * 0.32)
    stroke_w = int(s * 0.13)

    # Draw annular C by drawing an outer disc, then punching an inner disc and a right-side opening
    c_layer = Image.new("RGBA", (s, s), TRANSPARENT)
    c_draw = ImageDraw.Draw(c_layer)
    c_draw.ellipse([cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r], fill=CREAM)
    inner_r = outer_r - stroke_w
    c_draw.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r], fill=TRANSPARENT)

    # Cut the right side open to form a C — wedge from about 5 o'clock to 1 o'clock
    wedge = Image.new("L", (s, s), 0)
    wd = ImageDraw.Draw(wedge)
    # Pieslice: bounds, start_angle, end_angle (degrees, 0 = right, clockwise+ in Pillow)
    wedge_r = outer_r + stroke_w  # bigger than the disc so we cleanly cut through
    wd.pieslice([cx - wedge_r, cy - wedge_r, cx + wedge_r, cy + wedge_r], start=-50, end=50, fill=255)
    # erase the wedge from c_layer
    px = c_layer.load()
    wmask = wedge.load()
    for y in range(s):
        for x in range(s):
            if wmask[x, y] > 0:
                px[x, y] = TRANSPARENT

    img = Image.alpha_composite(img, c_layer)
    return img.resize((size, size), Image.LANCZOS)


def main():
    sizes = [16, 32, 48, 64, 96, 128, 180, 192, 256, 512]
    images = {}
    for sz in sizes:
        im = draw_mark(sz)
        images[sz] = im

    # PNGs
    images[180].save(os.path.join(OUT_DIR, "apple-touch-icon.png"))
    images[192].save(os.path.join(OUT_DIR, "icon-192.png"))
    images[512].save(os.path.join(OUT_DIR, "icon-512.png"))
    images[32].save(os.path.join(OUT_DIR, "favicon-32.png"))
    images[16].save(os.path.join(OUT_DIR, "favicon-16.png"))

    # Multi-resolution ICO
    ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
    images[64].save(
        os.path.join(OUT_DIR, "favicon.ico"),
        format="ICO",
        sizes=ico_sizes,
    )

    print("wrote:", sorted(os.listdir(OUT_DIR)))


if __name__ == "__main__":
    main()
