"""Colors, rarity tiers, fonts and the vector gem shapes used in the PDF."""

import math

from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ------------------------------------------------------------- palette ----

BACKGROUND = (0.012, 0.063, 0.102)   # #03101a - deep hextech teal
BACKGROUND_TOP = (0.012, 0.122, 0.173)  # #031f2c - the page fades up into this
PANEL = (0.024, 0.145, 0.204)
ROW_ODD = (0.020, 0.118, 0.161)      # subtle zebra stripe
GOLD = (0.784, 0.667, 0.431)         # #C8AA6E
GOLD_DARK = (0.310, 0.259, 0.169)
TEXT = (0.941, 0.945, 0.949)
TEXT_DIM = (0.494, 0.545, 0.588)

# Ordered like the rarity strip in the client (rarest first).
TIERS = ["Exalted", "Transcendent", "Ultimate", "Mythic", "Legendary", "Epic", "Rare"]

TIER_COLOR = {
    "Exalted": (0.898, 0.878, 0.941),
    "Transcendent": (0.722, 0.878, 0.290),
    "Ultimate": (0.878, 0.529, 0.227),
    "Mythic": (0.816, 0.251, 0.878),
    "Legendary": (0.878, 0.227, 0.227),
    "Epic": (0.227, 0.816, 0.784),
    "Rare": (0.290, 0.565, 0.878),
}

TIER_HEX = {
    "Exalted": "E5E0F0",
    "Transcendent": "B8E04A",
    "Ultimate": "E0873A",
    "Mythic": "D040E0",
    "Legendary": "E03A3A",
    "Epic": "3AD0C8",
    "Rare": "4A90E0",
}

# Community Dragon rarity enum -> displayed tier name.
RARITY_ENUM = {
    "kNoRarity": "",
    "kRare": "Rare",
    "kEpic": "Epic",
    "kLegendary": "Legendary",
    "kMythic": "Mythic",
    "kUltimate": "Ultimate",
    "kTranscendent": "Transcendent",
    "kExalted": "Exalted",
}

# --------------------------------------------------------------- fonts ----

FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_DISPLAY = "Helvetica"
FONT_DISPLAY_BOLD = "Helvetica-Bold"


def register_fonts():
    """Segoe UI for text, Georgia for display headings. Falls back to Helvetica."""
    global FONT, FONT_BOLD, FONT_DISPLAY, FONT_DISPLAY_BOLD
    wanted = [
        ("UI", r"C:\Windows\Fonts\segoeui.ttf", "FONT"),
        ("UIB", r"C:\Windows\Fonts\seguisb.ttf", "FONT_BOLD"),
        ("D", r"C:\Windows\Fonts\georgia.ttf", "FONT_DISPLAY"),
        ("DB", r"C:\Windows\Fonts\georgiab.ttf", "FONT_DISPLAY_BOLD"),
    ]
    found = {}
    for name, path, key in wanted:
        try:
            pdfmetrics.registerFont(TTFont(name, path))
            found[key] = name
        except Exception:
            pass
    FONT = found.get("FONT", FONT)
    FONT_BOLD = found.get("FONT_BOLD", FONT_BOLD)
    FONT_DISPLAY = found.get("FONT_DISPLAY", FONT_DISPLAY)
    FONT_DISPLAY_BOLD = found.get("FONT_DISPLAY_BOLD", FONT_DISPLAY_BOLD)


# -------------------------------------------------------------- shapes ----


def _star(cx, cy, points, r_outer, r_inner, rotation=0.0):
    out = []
    for i in range(points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = rotation + i * math.pi / points
        out.append((cx + r * math.sin(a), cy + r * math.cos(a)))
    return out


def _polygon(c, pts, color, stroke=None, stroke_width=0.4):
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    c.setFillColorRGB(*color)
    if stroke:
        c.setStrokeColorRGB(*stroke)
        c.setLineWidth(stroke_width)
        c.drawPath(p, fill=1, stroke=1)
    else:
        c.drawPath(p, fill=1, stroke=0)


def _lighter(color, k=0.35):
    return tuple(min(1.0, x + (1.0 - x) * k) for x in color)


def _darker(color, k=0.4):
    return tuple(x * (1 - k) for x in color)


def _regular_polygon(cx, cy, r, sides, rotation=0.0):
    """Vertices of a regular polygon with one vertex pointing up."""
    return [
        (cx + r * math.sin(rotation + 2 * math.pi * i / sides),
         cy + r * math.cos(rotation + 2 * math.pi * i / sides))
        for i in range(sides)
    ]


def draw_gem(c, tier, cx, cy, r):
    """
    Draws the rarity mark; the silhouette matches that tier in the client.

    Side counts follow the gems in game: Legendary has four, Mythic five and
    Ultimate six.
    """
    color = TIER_COLOR.get(tier)
    if not color:
        return
    light, dark = _lighter(color), _darker(color)

    if tier == "Exalted":
        _polygon(c, _star(cx, cy, 8, r, r * 0.34), color)
        _polygon(c, _star(cx, cy, 4, r * 0.62, r * 0.16), light)

    elif tier == "Transcendent":
        _polygon(c, _star(cx, cy, 4, r, r * 0.26), color)
        _polygon(c, _star(cx, cy, 4, r * 0.55, r * 0.14), light)

    elif tier == "Ultimate":
        # six sides
        top, ur, lr, bottom, ll, ul = (
            (cx, cy + r),
            (cx + r * 0.87, cy + r * 0.45),
            (cx + r * 0.87, cy - r * 0.45),
            (cx, cy - r),
            (cx - r * 0.87, cy - r * 0.45),
            (cx - r * 0.87, cy + r * 0.45),
        )
        _polygon(c, [top, ur, lr, bottom, ll, ul], color)
        _polygon(c, [top, ur, (cx, cy), ul], light)
        _polygon(c, [bottom, lr, (cx, cy), ll], dark)

    elif tier == "Mythic":
        # five sides
        top, right, lower_right, lower_left, left = _regular_polygon(cx, cy, r, 5)
        _polygon(c, [top, right, lower_right, lower_left, left], color)
        _polygon(c, [top, right, (cx, cy), left], light)
        _polygon(c, [(cx, cy), lower_right, lower_left], dark)

    elif tier == "Legendary":
        # four sides, as wide as it is tall
        rhombus = [(cx, cy + r), (cx + r, cy), (cx, cy - r), (cx - r, cy)]
        _polygon(c, rhombus, color)
        _polygon(c, [(cx, cy + r), (cx + r, cy), (cx, cy)], light)
        _polygon(c, [(cx, cy - r), (cx - r, cy), (cx, cy)], dark)

    elif tier == "Epic":
        triangle = [(cx, cy + r), (cx + r * 0.92, cy - r * 0.72), (cx - r * 0.92, cy - r * 0.72)]
        _polygon(c, triangle, color)
        _polygon(c, [(cx, cy + r), (cx, cy - r * 0.72), (cx - r * 0.92, cy - r * 0.72)], light)

    elif tier == "Rare":
        _polygon(c, [(cx, cy + r * 0.9), (cx + r * 0.75, cy),
                     (cx, cy - r * 0.9), (cx - r * 0.75, cy)], color)
        _polygon(c, [(cx, cy + r * 0.9), (cx + r * 0.75, cy), (cx, cy)], light)


def diamond(c, cx, cy, r, color, filled=True):
    pts = [(cx, cy + r), (cx + r, cy), (cx, cy - r), (cx - r, cy)]
    if filled:
        _polygon(c, pts, color)
        return
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    c.setStrokeColorRGB(*color)
    c.setLineWidth(0.6)
    c.drawPath(p, fill=0, stroke=1)


def tracked_text(c, x, y, text, font, size, tracking, align="left"):
    """reportlab has no letter-spacing, so glyphs are placed one by one."""
    c.setFont(font, size)
    width = sum(c.stringWidth(ch, font, size) for ch in text) + tracking * (len(text) - 1)
    if align == "center":
        x -= width / 2
    elif align == "right":
        x -= width
    for ch in text:
        c.drawString(x, y, ch)
        x += c.stringWidth(ch, font, size) + tracking
    return width


GRADIENT_BANDS = 280


def page_background(c, W, H):
    """Vertical fade, lighter teal at the top easing down into near black.

    Drawn as thin bands rather than an embedded image: it stays vector, keeps
    the file small and prints without resampling.
    """
    band = H / GRADIENT_BANDS
    for i in range(GRADIENT_BANDS):
        t = (i / (GRADIENT_BANDS - 1)) ** 0.75
        c.setFillColorRGB(*(a + (b - a) * t
                            for a, b in zip(BACKGROUND_TOP, BACKGROUND)))
        # a hair of overlap so no seam shows between bands
        c.rect(0, H - (i + 1) * band, W, band + 0.5, fill=1, stroke=0)


def page_frame(c, W, H, margin):
    """Double gold border with diamonds in the corners and at the top centre."""
    c.setStrokeColorRGB(*GOLD_DARK)
    c.setLineWidth(0.9)
    c.rect(margin, margin, W - 2 * margin, H - 2 * margin, fill=0, stroke=1)
    c.setLineWidth(0.35)
    inset = 1.8 * mm
    c.rect(margin + inset, margin + inset,
           W - 2 * (margin + inset), H - 2 * (margin + inset), fill=0, stroke=1)

    for x, y in ((margin, margin), (W - margin, margin),
                 (margin, H - margin), (W - margin, H - margin)):
        diamond(c, x, y, 1.5 * mm, BACKGROUND)
        diamond(c, x, y, 1.5 * mm, GOLD, filled=False)
    for y in (H - margin, margin):
        diamond(c, W / 2, y, 1.7 * mm, BACKGROUND)
        diamond(c, W / 2, y, 1.7 * mm, GOLD, filled=False)


def circular_image(c, path, cx, cy, r):
    """Image clipped to a circle with a gold ring."""
    c.saveState()
    p = c.beginPath()
    p.circle(cx, cy, r)
    c.clipPath(p, stroke=0)
    c.drawImage(path, cx - r, cy - r, width=2 * r, height=2 * r, mask="auto")
    c.restoreState()
    c.setStrokeColorRGB(*GOLD)
    c.setLineWidth(1.6)
    c.circle(cx, cy, r, fill=0, stroke=1)
    c.setStrokeColorRGB(*GOLD_DARK)
    c.setLineWidth(0.5)
    c.circle(cx, cy, r + 1.4 * mm, fill=0, stroke=1)
