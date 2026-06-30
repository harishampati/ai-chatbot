"""
Creates a clean, bold aria_icon.ico — simple shapes that stay sharp at small sizes.
"""
from PIL import Image, ImageDraw
import os, math

def draw_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size / 256  # scale factor

    def sc(v): return int(v * s)

    # ── Rounded square background (orange) ──
    radius = sc(52)
    d.rounded_rectangle([0, 0, size-1, size-1], radius=radius, fill="#f6a623")

    # ── Robot head (dark, large, centered) ──
    hx1, hy1, hx2, hy2 = sc(36), sc(68), sc(220), sc(210)
    d.rounded_rectangle([hx1, hy1, hx2, hy2], radius=sc(30), fill="#1a0c00")

    # ── Antenna ──
    ax = sc(128)
    d.rectangle([ax - sc(7), sc(20), ax + sc(7), hy1], fill="#1a0c00")
    d.ellipse([ax - sc(18), sc(4), ax + sc(18), sc(40)], fill="#ff6b00")
    d.ellipse([ax - sc(8), sc(12), ax + sc(8), sc(32)], fill="#ffcc80")

    # ── LEFT eye (big, white circle + coloured iris) ──
    ex1, ey = sc(64), sc(104)
    er = sc(36)
    d.ellipse([ex1 - er, ey - er, ex1 + er, ey + er], fill="#ffffff")
    d.ellipse([ex1 - sc(22), ey - sc(22), ex1 + sc(22), ey + sc(22)], fill="#ff6b00")
    d.ellipse([ex1 - sc(11), ey - sc(11), ex1 + sc(11), ey + sc(11)], fill="#1a0c00")
    # shine
    d.ellipse([ex1 - sc(20), ey - sc(24), ex1 - sc(6), ey - sc(10)], fill="#ffffff")

    # ── RIGHT eye ──
    ex2 = sc(192)
    d.ellipse([ex2 - er, ey - er, ex2 + er, ey + er], fill="#ffffff")
    d.ellipse([ex2 - sc(22), ey - sc(22), ex2 + sc(22), ey + sc(22)], fill="#ff6b00")
    d.ellipse([ex2 - sc(11), ey - sc(11), ex2 + sc(11), ey + sc(11)], fill="#1a0c00")
    d.ellipse([ex2 - sc(20), ey - sc(24), ex2 - sc(6), ey - sc(10)], fill="#ffffff")

    # ── Smile ──
    smile_pts = []
    cx, cy, r = sc(128), sc(172), sc(44)
    for angle in range(15, 166, 8):
        rad = math.radians(angle)
        smile_pts.append((cx + r * math.cos(rad), cy + r * math.sin(rad)))
    for i in range(len(smile_pts) - 1):
        d.line([smile_pts[i], smile_pts[i+1]], fill="#f6a623", width=max(sc(10), 2))

    # ── Ears (small orange circles on sides) ──
    ear_r = sc(18)
    for ex, ey2 in [(hx1, sc(140)), (hx2, sc(140))]:
        d.ellipse([ex - ear_r, ey2 - ear_r, ex + ear_r, ey2 + ear_r], fill="#f6a623")

    return img

def make_icon():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aria_icon.ico")
    sizes = [16, 32, 48, 64, 128, 256]
    images = [draw_icon(s) for s in sizes]
    images[0].save(
        out, format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=images[1:]
    )
    print(f"Icon saved: {out}")

if __name__ == "__main__":
    make_icon()
