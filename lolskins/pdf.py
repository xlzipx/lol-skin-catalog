"""Builds the PDF catalog: cover, summary, then a grid of splash art."""

import math
import os
import re
from datetime import date

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as pdfcanvas

from . import i18n, theme
from .theme import (
    BACKGROUND, GOLD, GOLD_DARK, PANEL, ROW_ODD, TEXT, TEXT_DIM, TIERS,
    TIER_COLOR, circular_image, diamond, draw_gem, page_background, page_frame,
    tracked_text,
)

SPLASH_RATIO = 717 / 1215


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


def _cover(c, W, H, skins, profile, tier_counts, icon):
    page_background(c, W, H)

    # soft glow along the top edge
    for i in range(60):
        k = 1 - i / 60
        c.setFillColorRGB(BACKGROUND[0] + 0.05 * k,
                          BACKGROUND[1] + 0.06 * k,
                          BACKGROUND[2] + 0.08 * k)
        c.rect(0, H - (i + 1) * H / 140, W, H / 140 + 0.6, fill=1, stroke=0)

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
    tracked_text(c, W / 2, y, i18n.t("pdf_game"), theme.FONT_DISPLAY_BOLD, 15, 3.2, "center")
    y -= 7.5 * mm
    c.setFillColorRGB(*TEXT_DIM)
    tracked_text(c, W / 2, y, i18n.t("pdf_subtitle"), theme.FONT, 9, 3.6, "center")

    # headline count
    y_circle = y - 40 * mm
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
    tracked_text(c, W / 2, y_circle - 9 * mm, i18n.t("pdf_total_1"), theme.FONT, 7.5, 2.2, "center")
    tracked_text(c, W / 2, y_circle - 13.5 * mm, i18n.t("pdf_total_2"), theme.FONT, 7.5, 2.2, "center")

    # rarity strip
    y_gem = y_circle - r - 26 * mm
    step = min(24 * mm, (W - 60 * mm) / max(1, len(TIERS)))
    x0 = W / 2 - step * (len(TIERS) - 1) / 2
    for i, tier in enumerate(TIERS):
        x = x0 + i * step
        draw_gem(c, tier, x, y_gem, 4.6 * mm)
        c.setFillColorRGB(*TEXT)
        c.setFont(theme.FONT_DISPLAY_BOLD, 12)
        c.drawCentredString(x, y_gem - 12 * mm, str(tier_counts.get(tier, 0)))
        c.setFillColorRGB(*TEXT_DIM)
        c.setFont(theme.FONT, 5.6)
        c.drawCentredString(x, y_gem - 16.5 * mm, tier.upper())

    # secondary stats
    y_rule = y_gem - 30 * mm
    c.setStrokeColorRGB(*GOLD_DARK)
    c.setLineWidth(0.5)
    c.line(W / 2 - 48 * mm, y_rule, W / 2 + 48 * mm, y_rule)

    stats = [
        (str(len({s["champion"] for s in skins})), i18n.t("pdf_champions")),
        (str(profile.get("chromasOwned") or 0), i18n.t("pdf_chromas")),
        (str(profile.get("championsOwned") or 0), i18n.t("pdf_champs_owned")),
    ]
    step2 = 38 * mm
    x0 = W / 2 - step2 * (len(stats) - 1) / 2
    for i, (value, label) in enumerate(stats):
        x = x0 + i * step2
        c.setFillColorRGB(*GOLD)
        c.setFont(theme.FONT_DISPLAY_BOLD, 16)
        c.drawCentredString(x, y_rule - 10 * mm, value)
        c.setFillColorRGB(*TEXT_DIM)
        tracked_text(c, x, y_rule - 15.5 * mm, label, theme.FONT, 7, 1.1, "center")

    c.setFillColorRGB(*TEXT_DIM)
    c.setFont(theme.FONT, 7)
    c.drawCentredString(W / 2, 18 * mm,
                        i18n.t("pdf_generated", date=date.today().strftime("%d. %m. %Y")))
    c.showPage()


# ----------------------------------------------------------- page chrome ----


def _page_header(c, W, H, margin, name, page, total):
    page_background(c, W, H)
    c.setFillColorRGB(*GOLD)
    tracked_text(c, margin, H - margin - 5 * mm,
                 i18n.t("pdf_header", name=name), theme.FONT_DISPLAY_BOLD, 10, 1.8)
    c.setFillColorRGB(*TEXT_DIM)
    c.setFont(theme.FONT, 7.5)
    c.drawRightString(W - margin, H - margin - 5 * mm, f"{page} / {total}")

    y = H - margin - 9.5 * mm
    c.setStrokeColorRGB(*GOLD_DARK)
    c.setLineWidth(0.5)
    c.line(margin, y, W / 2 - 3 * mm, y)
    c.line(W / 2 + 3 * mm, y, W - margin, y)
    diamond(c, W / 2, y, 1.4 * mm, GOLD, filled=False)


# --------------------------------------------------------------- summary ----


def _summary(c, W, H, margin, skins, tier_counts, name, total_pages):
    _page_header(c, W, H, margin, name, 2, total_pages)
    c.setFillColorRGB(*TEXT)
    tracked_text(c, margin, H - margin - 20 * mm, i18n.t("pdf_summary"),
                 theme.FONT_DISPLAY_BOLD, 12, 2.4)

    label_y = H - margin - 27 * mm
    c.setFillColorRGB(*TEXT_DIM)
    c.setFont(theme.FONT, 7.5)
    c.drawString(margin, label_y, i18n.t("pdf_by_rarity"))

    # ---- rarity rows ----
    row_h = 8.5 * mm
    y = H - margin - 34 * mm
    rarity_w = 46 * mm
    rows = [(tier, tier_counts.get(tier, 0)) for tier in TIERS]
    rows.append((None, tier_counts.get("", 0)))

    for i, (tier, count) in enumerate(rows):
        if i % 2 == 0:
            c.setFillColorRGB(*ROW_ODD)
            c.rect(margin - 1.5 * mm, y - row_h / 2 - 1.2 * mm,
                   rarity_w + 3 * mm, row_h, fill=1, stroke=0)
        if tier:
            draw_gem(c, tier, margin + 3 * mm, y, 3.2 * mm)
            c.setFillColorRGB(*TEXT)
            c.setFont(theme.FONT_BOLD, 8.5)
            c.drawString(margin + 9 * mm, y - 2.6, tier)
            c.setFillColorRGB(*GOLD)
        else:
            c.setFillColorRGB(*TEXT_DIM)
            c.setFont(theme.FONT, 8.5)
            c.drawString(margin + 9 * mm, y - 2.6, i18n.t("pdf_no_tier"))
        c.drawRightString(margin + rarity_w, y - 2.6, str(count))
        y -= row_h

    # ---- champion table, three striped columns ----
    counts = {}
    for skin in skins:
        counts[skin["champion"]] = counts.get(skin["champion"], 0) + 1
    names = sorted(counts, key=str.lower)

    columns = 3
    x_start = margin + 56 * mm
    col_w = (W - margin - x_start) / columns
    y_top = H - margin - 34 * mm

    c.setFillColorRGB(*TEXT_DIM)
    c.setFont(theme.FONT, 7.5)
    c.drawString(x_start, label_y, i18n.t("pdf_by_champion", count=len(names)))

    per_column = math.ceil(len(names) / columns)
    step = min(6.2 * mm, (y_top - margin - 8 * mm) / max(1, per_column - 1))

    for i, champion in enumerate(names):
        col, row = divmod(i, per_column)
        x = x_start + col * col_w
        y = y_top - row * step
        if row % 2 == 0:
            c.setFillColorRGB(*ROW_ODD)
            c.rect(x - 1.5 * mm, y - 1.9 * mm, col_w - 3 * mm, step, fill=1, stroke=0)
        c.setFillColorRGB(*TEXT)
        c.setFont(theme.FONT, 7.2)
        c.drawString(x, y, champion)
        c.setFillColorRGB(*GOLD)
        c.drawRightString(x + col_w - 6 * mm, y, str(counts[champion]))
    c.showPage()


# ------------------------------------------------------------------ grid ----


def build(skins, profile, tier_counts, icon, path):
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
    c.setTitle(f"{profile.get('gameName', '')} - League of Legends owned skins")
    c.setAuthor(profile.get("gameName", ""))

    card_w = (W - 2 * margin - (columns - 1) * gap) / columns
    img_w = card_w - 2 * padding
    img_h = img_w * _thumb_ratio(skins)
    card_h = padding + img_h + text_h + padding

    available = H - margin - header_h - margin
    rows = max(1, int((available + gap) // (card_h + gap)))
    per_page = columns * rows
    grid_pages = (len(skins) + per_page - 1) // per_page
    total_pages = grid_pages + 2

    _cover(c, W, H, skins, profile, tier_counts, icon)
    _summary(c, W, H, margin, skins, tier_counts, name, total_pages)

    for idx, skin in enumerate(skins):
        slot = idx % per_page
        if slot == 0:
            _page_header(c, W, H, margin, name, idx // per_page + 3, total_pages)

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
            caption += " · " + i18n.chromas(skin["chromas"])
        c.drawString(x_text, y_text - 3.6 * mm, caption)

        if slot == per_page - 1 or idx == len(skins) - 1:
            c.showPage()

    c.save()
    return total_pages
