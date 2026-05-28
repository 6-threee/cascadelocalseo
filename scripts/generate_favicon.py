"""Generate Cascade Local SEO brand mark + favicon set.

2026-05-28 redesign: matches the screenshot Jonathan provided —
- Rounded-square canvas
- Ocean-blue border (#4ac4e0) wrapping the mark
- Deep forest green interior (#062514)
- Gold (#dabe79) contour-wave squiggle (the same shape as the homepage SVG
  logo: `M 2 18 C 7 8, 11 8, 13 13 S 19 18, 24 8` on a 26-unit canvas)

The wave is rasterized by sampling each cubic-Bezier segment as points,
connecting them with rounded line strokes. 4x supersampling + LANCZOS
downsample keeps edges crisp at tiny sizes.
"""
from __future__ import annotations
import os
from PIL import Image, ImageDraw

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "public")
os.makedirs(OUT_DIR, exist_ok=True)

# Brand palette (matches the live site)
FOREST = (6, 37, 20, 255)        # #062514 — deep forest interior
GOLD = (218, 190, 121, 255)      # #dabe79 — wave stroke
OCEAN = (74, 196, 224, 255)      # #4ac4e0 — outer border
TRANSPARENT = (0, 0, 0, 0)


def cubic_bezier(p0, p1, p2, p3, steps=40):
    """Sample `steps` points along a cubic Bezier curve. p0..p3 are (x,y)."""
    out = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        x = (u**3) * p0[0] + 3 * (u**2) * t * p1[0] + 3 * u * (t**2) * p2[0] + (t**3) * p3[0]
        y = (u**3) * p0[1] + 3 * (u**2) * t * p1[1] + 3 * u * (t**2) * p2[1] + (t**3) * p3[1]
        out.append((x, y))
    return out


def wave_points(s):
    """Return the gold wave as a list of pixel coordinates, scaled into the inner
    safe-area of a canvas of size s. Mirrors the homepage SVG logo path:
        M 2 18 C 7 8, 11 8, 13 13 S 19 18, 24 8
    On a 26-unit viewBox. We pad inset so the wave sits inside the ocean border.
    """
    # Inset the wave inside the ocean border + a bit of inner padding for breathing room.
    pad = s * 0.22          # leaves room for the border + breathing room around the wave
    span = s - 2 * pad      # the wave fits in span x span
    sx = span / 26.0
    off_x = pad
    # Mark uses y from ~8 to ~18 on a 26-unit canvas, so the wave occupies the mid 38% vertically.
    # Center it vertically with a slight upward bias.
    sy = span / 26.0
    off_y = pad + (span - sy * 26) / 2

    def P(x, y):
        return (off_x + x * sx, off_y + y * sy)

    # Segment 1: M (2,18) C (7,8) (11,8) (13,13)
    seg1 = cubic_bezier(P(2, 18), P(7, 8), P(11, 8), P(13, 13), steps=42)
    # Segment 2 (smooth-cubic S 19 18, 24 8): first control = reflection of previous control
    # previous control was (11,8); end was (13,13); reflection across end is 2*end - prev_ctrl
    # = (2*13 - 11, 2*13 - 8) = (15, 18). second control = (19,18). end = (24,8).
    seg2 = cubic_bezier(P(13, 13), P(15, 18), P(19, 18), P(24, 8), steps=42)
    # Avoid duplicating the join point
    return seg1 + seg2[1:]


def draw_mark(size: int) -> Image.Image:
    """Render the brand mark at the requested square pixel size with 4x supersampling."""
    s = size * 4
    img = Image.new("RGBA", (s, s), TRANSPARENT)

    # Border thickness + corner radius scale with size
    border_w = max(2, int(s * 0.075))
    radius = int(s * 0.20)

    # 1) Outer ocean-blue rounded-square (this is the border)
    border_layer = ImageDraw.Draw(img)
    border_layer.rounded_rectangle([(0, 0), (s - 1, s - 1)], radius=radius, fill=OCEAN)

    # 2) Inner forest-green panel, inset by border_w
    inner_radius = max(1, radius - border_w)
    border_layer.rounded_rectangle(
        [(border_w, border_w), (s - 1 - border_w, s - 1 - border_w)],
        radius=inner_radius, fill=FOREST,
    )

    # 3) Gold wave stroke
    pts = wave_points(s)
    stroke_w = max(2, int(s * 0.082))  # bold wave, scales with canvas
    wave_layer = ImageDraw.Draw(img)
    wave_layer.line(pts, fill=GOLD, width=stroke_w, joint="curve")
    # Round line caps (PIL line caps are butted by default; emulate round caps with circles at endpoints)
    r = stroke_w // 2
    x0, y0 = pts[0]
    x1, y1 = pts[-1]
    wave_layer.ellipse([x0 - r, y0 - r, x0 + r, y0 + r], fill=GOLD)
    wave_layer.ellipse([x1 - r, y1 - r, x1 + r, y1 + r], fill=GOLD)

    # Downsample to final size with LANCZOS for crisp anti-aliased edges
    return img.resize((size, size), Image.LANCZOS)


def main():
    # Build every size we use across favicons + app icons
    sizes = [16, 32, 48, 64, 96, 128, 180, 192, 256, 512]
    images = {sz: draw_mark(sz) for sz in sizes}

    # Standalone PNGs
    images[180].save(os.path.join(OUT_DIR, "apple-touch-icon.png"))
    images[192].save(os.path.join(OUT_DIR, "icon-192.png"))
    images[512].save(os.path.join(OUT_DIR, "icon-512.png"))
    images[32].save(os.path.join(OUT_DIR, "favicon-32.png"))
    images[16].save(os.path.join(OUT_DIR, "favicon-16.png"))

    # Multi-resolution .ico (Chrome/Edge/Safari all consume this for the tab icon)
    ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
    images[64].save(
        os.path.join(OUT_DIR, "favicon.ico"),
        format="ICO",
        sizes=ico_sizes,
    )

    print("wrote favicon set →")
    for f in ("favicon.ico", "favicon-16.png", "favicon-32.png", "apple-touch-icon.png", "icon-192.png", "icon-512.png"):
        path = os.path.join(OUT_DIR, f)
        sz = os.path.getsize(path)
        print(f"  {f:24s} {sz:>7,} bytes")


if __name__ == "__main__":
    main()
