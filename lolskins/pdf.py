"""Builds the PDF catalog: cover, champion roster, then a grid of splash art."""

import math
import os
import re
from datetime import date

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as pdfcanvas

from . import theme
from .theme import (
    BACKGROUND, GOLD, GOLD_DARK, PANEL, ROW_ODD, TEXT, TEXT_DIM, TIERS,
    TIER_COLOR, circular_image, diamond, draw_gem, page_background, page_frame,
    tracked_text,
)

SPLASH_RATIO = 717 / 1215
PROJECT_URL = "https://github.com/xlzipx/lol-skin-catalog"
FOOTER_NOTE = ("Generated with LoL Skin Catalog — a free, open-source tool "
               "for exporting the skins you own.")


def chroma_label(count):
    """'1 chroma' / '6 chromas'."""
    return f"{count} chroma" if count == 1 else f"{count} chromas"


def _display_name(profile):
    return (profile.get("gameName") or "SUMMONER").upper()


def _header_name(profile):
    """The in-game name can be spaced out ('Z I P E E K'); collapse it for headings
    so it does not fight with the tracking applied to the heading itself."""
    return re.sub(r"\s+", "", profile.get("gameName") or "SUMMONER").upper()


def _thumb_ratio(skins, default=SPLASH_RATIO):
    for skin in skins:
        if skin.get("thumb") and os.path.exists(skin["thumb"]):
            with Image.open(skin["thumb"]) as im:
                return im.height / im.width
    return default


# ---------------------------------------------------------------- cover ----


def _cover(c, W, H, skins, profile, tier_counts, icon, contents=None):
    page_background(c, W, H)
    page_frame(c, W, H, 12 * mm)

    y_icon = H - 52 * mm
    if icon:
        circular_image(c, icon, W / 2, y_icon, 17 * mm)
        y_badge = y_icon - 20 * mm
        diamond(c, W / 2, y_badge, 5 * mm, BACKGROUND)
        diamond(c, W / 2, y_badge, 5 * mm, GOLD, filled=False)
        c.setFillColorRGB(*GOLD)
        c.setFont(theme.FONT_DISPLAY_BOLD, 9)
        c.drawCentredString(W / 2, y_badge - 3.1, str(profile.get("level") or ""))
        y = y_badge - 14 * mm
    else:
        y = y_icon

    c.setFillColorRGB(*TEXT)
    tracked_text(c, W / 2, y, _display_name(profile), theme.FONT_DISPLAY_BOLD, 20, 5.5, "center")
    if profile.get("tagLine"):
        c.setFillColorRGB(*TEXT_DIM)
        c.setFont(theme.FONT, 9)
        c.drawCentredString(W / 2, y - 6.5 * mm, "#" + profile["tagLine"])

    y -= 18 * mm
    c.setFillColorRGB(*GOLD)
    tracked_text(c, W / 2, y, "LEAGUE OF LEGENDS", theme.FONT_DISPLAY_BOLD, 15, 3.2, "center")
    y -= 7.5 * mm
    c.setFillColorRGB(*TEXT_DIM)
    tracked_text(c, W / 2, y, "OWNED SKINS COLLECTION", theme.FONT, 9, 3.6, "center")

    # headline count
    y_circle = y - 36 * mm
    r = 24 * mm
    c.setFillColorRGB(*PANEL)
    c.circle(W / 2, y_circle, r, fill=1, stroke=0)
    c.setStrokeColorRGB(*GOLD)
    c.setLineWidth(1.2)
    c.circle(W / 2, y_circle, r, fill=0, stroke=1)
    c.setStrokeColorRGB(*GOLD_DARK)
    c.setLineWidth(0.4)
    c.circle(W / 2, y_circle, r + 2 * mm, fill=0, stroke=1)
    diamond(c, W / 2, y_circle + r + 2 * mm, 1.6 * mm, BACKGROUND)
    diamond(c, W / 2, y_circle + r + 2 * mm, 1.6 * mm, GOLD, filled=False)

    c.setFillColorRGB(*GOLD)
    c.setFont(theme.FONT_DISPLAY_BOLD, 40)
    c.drawCentredString(W / 2, y_circle + 1 * mm, str(len(skins)))
    c.setFillColorRGB(*TEXT)
    tracked_text(c, W / 2, y_circle - 9 * mm, "TOTAL SKINS", theme.FONT, 7.5, 2.2, "center")
    tracked_text(c, W / 2, y_circle - 13.5 * mm, "OWNED", theme.FONT, 7.5, 2.2, "center")

    # rarity strip
    y_gem = y_circle - r - 24 * mm
    step = min(24 * mm, (W - 60 * mm) / max(1, len(TIERS)))
    x0 = W / 2 - step * (len(TIERS) - 1) / 2
    for i, tier in enumerate(TIERS):
        x = x0 + i * step
        draw_gem(c, tier, x, y_gem, 5 * mm)
        c.setFillColorRGB(*TEXT)
        c.setFont(theme.FONT_DISPLAY_BOLD, 16)
        c.drawCentredString(x, y_gem - 13 * mm, str(tier_counts.get(tier, 0)))
        c.setFillColorRGB(*TEXT_DIM)
        c.setFont(theme.FONT, 7.2)
        c.drawCentredString(x, y_gem - 19 * mm, tier.upper())

    # secondary stats
    y_rule = y_gem - 27 * mm
    c.setStrokeColorRGB(*GOLD_DARK)
    c.setLineWidth(0.5)
    c.line(W / 2 - 48 * mm, y_rule, W / 2 + 48 * mm, y_rule)

    stats = [
        (str(len({s["champion"] for s in skins})), "CHAMPIONS WITH SKINS"),
        (str(profile.get("chromasOwned") or 0), "CHROMAS"),
        (str(profile.get("championsOwned") or 0), "CHAMPIONS OWNED"),
    ]
    step2 = 46 * mm
    x0 = W / 2 - step2 * (len(stats) - 1) / 2
    for i, (value, label) in enumerate(stats):
        x = x0 + i * step2
        c.setFillColorRGB(*GOLD)
        c.setFont(theme.FONT_DISPLAY_BOLD, 16)
        c.drawCentredString(x, y_rule - 10 * mm, value)
        c.setFillColorRGB(*TEXT_DIM)
        tracked_text(c, x, y_rule - 15.5 * mm, label, theme.FONT, 7, 1.1, "center")

    if contents:
        _cover_contents(c, W, margin=12 * mm, top=y_rule - 24 * mm, entries=contents)

    c.setFillColorRGB(*TEXT_DIM)
    c.setFont(theme.FONT, 7)
    c.drawCentredString(W / 2, 15 * mm,
                        "Generated " + date.today().strftime("%d. %m. %Y"))
    c.showPage()


def _cover_contents(c, W, margin, top, entries):
    """A row of plaques pointing at each section, echoing the client's tab bar.

    Every plaque is a live link, so the page number is also a jump target.
    """
    c.setStrokeColorRGB(*GOLD_DARK)
    c.setLineWidth(0.5)
    c.line(margin + 12 * mm, top, W / 2 - 14 * mm, top)
    c.line(W / 2 + 14 * mm, top, W - margin - 12 * mm, top)
    c.setFillColorRGB(*TEXT_DIM)
    tracked_text(c, W / 2, top - 1.2 * mm, "CONTENTS", theme.FONT, 6.5, 2.4, "center")

    # a fixed, narrower plaque keeps the row clear of the ornamental frame
    gap = 4 * mm
    width = 37 * mm
    height = 15 * mm
    total = len(entries) * width + (len(entries) - 1) * gap
    left = (W - total) / 2
    y = top - 6 * mm - height

    for i, (label, page, anchor) in enumerate(entries):
        x = left + i * (width + gap)
        c.setFillColorRGB(*PANEL)
        c.roundRect(x, y, width, height, 1.2 * mm, fill=1, stroke=0)
        c.setStrokeColorRGB(*GOLD_DARK)
        c.setLineWidth(0.5)
        c.roundRect(x, y, width, height, 1.2 * mm, fill=0, stroke=1)

        c.setFillColorRGB(*TEXT_DIM)
        tracked_text(c, x + width / 2, y + height - 5.5 * mm, label.upper(),
                     theme.FONT, 6, 1.0, "center")

        # "PAGE 3", not "3" - every other number on this cover is a count,
        # so a bare figure here reads as one
        number = str(page)
        word_w = c.stringWidth("PAGE", theme.FONT, 6) + 1.0 * 3
        number_w = c.stringWidth(number, theme.FONT_DISPLAY_BOLD, 13)
        start = x + width / 2 - (word_w + 1.6 * mm + number_w) / 2
        c.setFillColorRGB(*TEXT_DIM)
        tracked_text(c, start, y + 3.9 * mm, "PAGE", theme.FONT, 6, 1.0)
        c.setFillColorRGB(*GOLD)
        c.setFont(theme.FONT_DISPLAY_BOLD, 13)
        c.drawString(start + word_w + 1.6 * mm, y + 3.6 * mm, number)

        if anchor:
            c.linkAbsolute("", anchor, (x, y, x + width, y + height), thickness=0)


# ----------------------------------------------------------- page chrome ----


def _footer(c, W, H, margin):
    """Credit line at the very bottom of the last page, with a clickable link."""
    y = margin + 13 * mm
    c.setStrokeColorRGB(*GOLD_DARK)
    c.setLineWidth(0.5)
    c.line(W / 2 - 42 * mm, y, W / 2 - 3 * mm, y)
    c.line(W / 2 + 3 * mm, y, W / 2 + 42 * mm, y)
    diamond(c, W / 2, y, 1.3 * mm, GOLD, filled=False)

    c.setFillColorRGB(*TEXT_DIM)
    c.setFont(theme.FONT, 6.6)
    c.drawCentredString(W / 2, y - 6 * mm, FOOTER_NOTE)

    label = PROJECT_URL.replace("https://", "")
    c.setFillColorRGB(*GOLD)
    c.setFont(theme.FONT, 7.2)
    c.drawCentredString(W / 2, y - 11 * mm, label)

    width = c.stringWidth(label, theme.FONT, 7.2)
    c.linkURL(PROJECT_URL,
              (W / 2 - width / 2, y - 12.5 * mm, W / 2 + width / 2, y - 9.5 * mm),
              relative=0, thickness=0)


BACK_LINK_H = 9 * mm


def _back_link(c, W, margin):
    """Small link at the foot of a content page, back to the champion roster."""
    y = margin + 3 * mm
    label = "CHAMPION ROSTER · PAGE 2"
    size = 6.4
    width = sum(c.stringWidth(ch, theme.FONT, size) for ch in label) + 1.2 * (len(label) - 1)
    x = W / 2 - width / 2

    diamond(c, x - 4 * mm, y + 0.8 * mm, 1.1 * mm, GOLD, filled=False)
    diamond(c, x + width + 4 * mm, y + 0.8 * mm, 1.1 * mm, GOLD, filled=False)
    c.setFillColorRGB(*GOLD)
    tracked_text(c, x, y, label, theme.FONT, size, 1.2)

    c.linkAbsolute("", "section-roster",
                   (x - 6 * mm, y - 2 * mm, x + width + 6 * mm, y + 4 * mm),
                   thickness=0)


def _page_header(c, W, H, margin, name, page, total, section="COLLECTION"):
    page_background(c, W, H)
    c.setFillColorRGB(*GOLD)
    tracked_text(c, margin, H - margin - 5 * mm,
                 f"{name}'S {section}", theme.FONT_DISPLAY_BOLD, 10, 1.8)
    c.setFillColorRGB(*TEXT_DIM)
    c.setFont(theme.FONT, 7.5)
    c.drawRightString(W - margin, H - margin - 5 * mm, f"{page} / {total}")

    y = H - margin - 9.5 * mm
    c.setStrokeColorRGB(*GOLD_DARK)
    c.setLineWidth(0.5)
    c.line(margin, y, W / 2 - 3 * mm, y)
    c.line(W / 2 + 3 * mm, y, W - margin, y)
    diamond(c, W / 2, y, 1.4 * mm, GOLD, filled=False)


# ------------------------------------------------------- champion roster ----


def _roster(c, W, H, margin, skins, name, total_pages, champion_pages=None):
    """Every champion with the number of skins owned, in striped columns.

    Each row links to the page where that champion's skins begin. Rarity totals
    deliberately live on the cover only - repeating the gems here would just
    duplicate the page before.
    """
    champion_pages = champion_pages or {}
    _page_header(c, W, H, margin, name, 2, total_pages, "CHAMPION ROSTER")
    c.bookmarkPage("section-roster")
    c.addOutlineEntry("Champion roster", "section-roster", 0)

    counts = {}
    for skin in skins:
        counts[skin["champion"]] = counts.get(skin["champion"], 0) + 1
    names = sorted(counts, key=str.lower)

    c.setFillColorRGB(*TEXT)
    tracked_text(c, margin, H - margin - 21 * mm, "SKINS BY CHAMPION",
                 theme.FONT_DISPLAY_BOLD, 14, 2.6)
    c.setFillColorRGB(*TEXT_DIM)
    c.setFont(theme.FONT, 8.5)
    subtitle = f"{len(names)} champions · {len(skins)} skins owned"
    if champion_pages:
        subtitle += " · select a champion to jump to their skins"
    c.drawString(margin, H - margin - 27.5 * mm, subtitle)

    y_rule = H - margin - 32 * mm
    c.setStrokeColorRGB(*GOLD_DARK)
    c.setLineWidth(0.5)
    c.line(margin, y_rule, W - margin, y_rule)

    columns = 4
    col_w = (W - 2 * margin) / columns
    y_top = y_rule - 9 * mm
    bottom = margin + 4 * mm

    per_column = math.ceil(len(names) / columns)
    step = min(8 * mm, (y_top - bottom) / max(1, per_column - 1))
    # the type only shrinks when a very large collection needs tighter rows
    size = max(6.4, min(10.0, step / mm * 1.35))

    for i, champion in enumerate(names):
        col, row = divmod(i, per_column)
        x = margin + col * col_w
        y = y_top - row * step
        if row % 2 == 0:
            c.setFillColorRGB(*ROW_ODD)
            c.rect(x, y - step * 0.32, col_w - 3 * mm, step, fill=1, stroke=0)
        c.setFillColorRGB(*TEXT)
        c.setFont(theme.FONT, size)
        c.drawString(x + 2.5 * mm, y, champion)
        c.setFillColorRGB(*GOLD)
        c.setFont(theme.FONT_BOLD, size)
        c.drawRightString(x + col_w - 5.5 * mm, y, str(counts[champion]))

        page = champion_pages.get(champion)
        if page:
            c.linkAbsolute("", f"skins-page-{page}",
                           (x, y - step * 0.32, x + col_w - 3 * mm,
                            y - step * 0.32 + step), thickness=0)
    c.showPage()


# --------------------------------------------------- icons and ward skins ----

# tile geometry per collectible kind
LAYOUT = {
    "icons": {"columns": 8, "label": "SUMMONER ICONS",
              "header": "ICONS COLLECTION", "square": True},
    "wards": {"columns": 6, "label": "WARD SKINS",
              "header": "WARDS COLLECTION", "square": True},
}


def _geometry(W, margin, kind):
    """Tile size and row pitch for one collectible kind."""
    columns = LAYOUT[kind]["columns"]
    col_w = (W - 2 * margin) / columns
    tile = col_w - 4 * mm
    return columns, col_w, tile, tile + 4 * mm


def _plan_grid(count, columns, cell_h, first_page_h, other_page_h):
    """Splits a flat, date-ordered run of tiles into pages.

    Done before anything is drawn so the cover can print real page numbers.
    Items simply follow one another newest first - no per-year headings, which
    keeps the section a few pages shorter.
    """
    pages = []
    placed = 0
    while placed < count:
        available = first_page_h if not pages else other_page_h
        rows = max(1, int(available // cell_h))
        take = min(count - placed, rows * columns)
        pages.append((placed, take))
        placed += take
    return pages or [(0, 0)]


def _draw_collection(c, W, H, margin, kind, items, plan, name, first_page,
                     total_pages, footer=False):
    """Renders the planned pages for one collectible kind."""
    setup = LAYOUT[kind]
    columns, col_w, tile, cell_h = _geometry(W, margin, kind)
    title_h = 18 * mm

    for offset, (start, count) in enumerate(plan):
        page_no = first_page + offset
        _page_header(c, W, H, margin, name, page_no, total_pages, setup["header"])
        top = H - margin - 16 * mm

        if page_no != total_pages:
            _back_link(c, W, margin)
        if offset == 0:
            c.bookmarkPage(f"section-{kind}")
            c.addOutlineEntry(setup["label"].title(), f"section-{kind}", 0)
            c.setFillColorRGB(*TEXT)
            tracked_text(c, margin, top - 5 * mm, setup["label"],
                         theme.FONT_DISPLAY_BOLD, 14, 2.6)
            c.setFillColorRGB(*TEXT_DIM)
            c.setFont(theme.FONT, 8.5)
            c.drawString(margin, top - 11 * mm,
                         f"{len(items)} owned · newest first")
            c.setStrokeColorRGB(*GOLD_DARK)
            c.setLineWidth(0.5)
            c.line(margin, top - 14.5 * mm, W - margin, top - 14.5 * mm)
            top -= title_h

        for i in range(count):
            item = items[start + i]
            col, row = i % columns, i // columns
            x = margin + col * col_w
            y = top - row * cell_h

            c.setFillColorRGB(*PANEL)
            c.roundRect(x, y - tile, tile, tile, 1 * mm, fill=1, stroke=0)
            if item.get("thumb") and os.path.exists(item["thumb"]):
                with Image.open(item["thumb"]) as im:
                    ratio = im.height / im.width
                # fit inside the square tile and centre what is left over
                if ratio > 1:
                    h, w = tile, tile / ratio
                else:
                    w, h = tile, tile * ratio
                c.drawImage(item["thumb"],
                            x + (tile - w) / 2, y - tile + (tile - h) / 2,
                            width=w, height=h, mask="auto")
            c.setStrokeColorRGB(*GOLD_DARK)
            c.setLineWidth(0.4)
            c.rect(x, y - tile, tile, tile, fill=0, stroke=1)

        if footer and offset == len(plan) - 1:
            _footer(c, W, H, margin)
        c.showPage()


# ------------------------------------------------------------------ grid ----


def build(skins, profile, tier_counts, icon, path, icons=None, wards=None):
    theme.register_fonts()

    W, H = A4
    margin = 12 * mm
    columns = 3
    gap = 5 * mm
    header_h = 16 * mm
    padding = 1.8 * mm
    text_h = 9.5 * mm

    name = _header_name(profile)

    c = pdfcanvas.Canvas(path, pagesize=A4)
    c.setTitle(f"{profile.get('gameName', '')} - League of Legends collection")
    c.setAuthor(profile.get("gameName", ""))

    card_w = (W - 2 * margin - (columns - 1) * gap) / columns
    img_w = card_w - 2 * padding
    img_h = img_w * _thumb_ratio(skins)
    card_h = padding + img_h + text_h + padding

    available = H - margin - header_h - margin
    rows = max(1, int((available + gap) // (card_h + gap)))
    per_page = columns * rows
    grid_pages = (len(skins) + per_page - 1) // per_page

    # Plan the collectible sections before drawing anything, so the cover can
    # print the page each section really starts on.
    plans = {}
    collections = {"icons": icons or [], "wards": wards or []}
    # the foot of every page but the last carries the back link, so the grid
    # has to stop short of it
    body_h = H - margin - 16 * mm - margin - BACK_LINK_H
    for kind, items in collections.items():
        if not items:
            continue
        # distinct names: `columns` above belongs to the skin grid and must
        # survive this loop untouched
        tile_columns, _, _, cell_h = _geometry(W, margin, kind)
        plans[kind] = _plan_grid(len(items), tile_columns, cell_h,
                                 body_h - 18 * mm, body_h)

    total_pages = grid_pages + 2 + sum(len(p) for p in plans.values())

    contents = [("Champion roster", 2, "section-roster"),
                ("Skins", 3, "section-skins")]
    next_page = 3 + grid_pages
    for kind in ("icons", "wards"):
        if kind in plans:
            contents.append((LAYOUT[kind]["label"], next_page, f"section-{kind}"))
            next_page += len(plans[kind])

    # first page each champion appears on, so the roster can link to it
    champion_pages = {}
    for idx, skin in enumerate(skins):
        champion_pages.setdefault(skin["champion"], 3 + idx // per_page)

    _cover(c, W, H, skins, profile, tier_counts, icon, contents)
    _roster(c, W, H, margin, skins, name, total_pages, champion_pages)

    for idx, skin in enumerate(skins):
        slot = idx % per_page
        if slot == 0:
            page_no = idx // per_page + 3
            _page_header(c, W, H, margin, name, page_no, total_pages,
                         "SKINS COLLECTION")
            c.bookmarkPage(f"skins-page-{page_no}")
            if page_no != total_pages:
                _back_link(c, W, margin)
            if idx == 0:
                c.bookmarkPage("section-skins")
                c.addOutlineEntry("Skins", "section-skins", 0)

        col, row = slot % columns, slot // columns
        x = margin + col * (card_w + gap)
        y_top = H - margin - header_h - row * (card_h + gap)

        c.setFillColorRGB(*PANEL)
        c.roundRect(x, y_top - card_h, card_w, card_h, 1.2 * mm, fill=1, stroke=0)

        if skin.get("thumb") and os.path.exists(skin["thumb"]):
            c.drawImage(skin["thumb"], x + padding, y_top - padding - img_h,
                        width=img_w, height=img_h)
        else:
            c.setFillColorRGB(0.09, 0.13, 0.20)
            c.rect(x + padding, y_top - padding - img_h, img_w, img_h, fill=1, stroke=0)

        tier = skin.get("rarity", "")
        border = TIER_COLOR.get(tier)
        c.setStrokeColorRGB(*(border if border else GOLD_DARK))
        c.setLineWidth(0.7 if border else 0.4)
        c.rect(x + padding, y_top - padding - img_h, img_w, img_h, fill=0, stroke=1)

        y_text = y_top - padding - img_h - 4.4 * mm
        x_text = x + padding
        if tier:
            draw_gem(c, tier, x_text + 1.7 * mm, y_text + 0.9 * mm, 1.9 * mm)
        x_text += 5 * mm

        text_w = card_w - padding - (x_text - x)
        c.setFillColorRGB(*TEXT)
        c.setFont(theme.FONT_BOLD, 7.6)
        label = skin["skin"]
        while c.stringWidth(label, theme.FONT_BOLD, 7.6) > text_w and len(label) > 4:
            label = label[:-2]
        if label != skin["skin"]:
            label = label[:-1] + "…"
        c.drawString(x_text, y_text, label)

        c.setFillColorRGB(*TEXT_DIM)
        c.setFont(theme.FONT, 6.6)
        caption = skin["champion"]
        if skin.get("chromas"):
            caption += " · " + chroma_label(skin["chromas"])
        c.drawString(x_text, y_text - 3.6 * mm, caption)

        if idx == len(skins) - 1 and not plans:
            _footer(c, W, H, margin)
        if slot == per_page - 1 or idx == len(skins) - 1:
            c.showPage()

    page_no = 3 + grid_pages
    for kind in ("icons", "wards"):
        if kind not in plans:
            continue
        last = kind == ("wards" if "wards" in plans else "icons")
        _draw_collection(c, W, H, margin, kind, collections[kind], plans[kind],
                         name, page_no, total_pages, footer=last)
        page_no += len(plans[kind])

    c.save()
    return total_pages
