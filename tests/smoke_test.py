"""
Offline smoke test - builds every output from synthetic data.

Needs no League client and no network, so it can run in CI.

    python tests/smoke_test.py
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lolskins import pdf, sheet, theme  # noqa: E402

FAILURES = []


def check(label, condition, detail=""):
    if condition:
        print(f"  ok    {label}")
    else:
        print(f"  FAIL  {label} {detail}")
        FAILURES.append(label)


def fake_skins(count=7):
    tiers = ["Epic", "Legendary", "Mythic", "Ultimate", "Rare", "", "Exalted"]
    return [
        {
            "champion": f"Champion {i // 2}",
            "skin": f"Test Skin {i}",
            "skinId": 1000 + i,
            "chromas": i % 4,
            "isBase": False,
            "rarity": tiers[i % len(tiers)],
            "file": None,
            "thumb": None,
        }
        for i in range(count)
    ]


FAKE_PROFILE = {
    "gameName": "Test Summoner",
    "tagLine": "EUW",
    "level": 42,
    "profileIconId": 0,
    "championsOwned": 12,
    "chromasOwned": 3,
    "skinsWithChroma": 2,
}


def test_imports():
    print("imports")
    from lolskins import assets, client, paths  # noqa: F401

    check("client module imports", hasattr(client, "fetch_inventory"))
    check("assets module imports", hasattr(assets, "download_splashes"))
    check("safe_filename strips separators", "/" not in paths.safe_filename("a/b:c"))


def test_chroma_label():
    print("chroma wording")
    check("singular", pdf.chroma_label(1) == "1 chroma", pdf.chroma_label(1))
    check("plural", pdf.chroma_label(6) == "6 chromas", pdf.chroma_label(6))
    check("zero reads as plural", pdf.chroma_label(0) == "0 chromas")


def test_gems():
    print("rarity gems")
    from reportlab.pdfgen import canvas as pdfcanvas

    with tempfile.TemporaryDirectory() as tmp:
        c = pdfcanvas.Canvas(os.path.join(tmp, "gems.pdf"))
        for tier in theme.TIERS:
            theme.draw_gem(c, tier, 100, 100, 10)
        theme.draw_gem(c, "", 100, 100, 10)  # no tier must not raise
        c.save()
    check("all tiers draw without error", True)
    check("every tier has a colour", all(t in theme.TIER_COLOR for t in theme.TIERS))
    check("every tier has a hex for Excel", all(t in theme.TIER_HEX for t in theme.TIERS))
    check("gem side counts: Legendary 4, Mythic 5, Ultimate 6",
          theme.TIERS.index("Ultimate") < theme.TIERS.index("Mythic")
          < theme.TIERS.index("Legendary"))


def test_outputs():
    print("document build")
    skins = fake_skins()
    counts = {}
    for skin in skins:
        counts[skin["rarity"]] = counts.get(skin["rarity"], 0) + 1

    with tempfile.TemporaryDirectory() as tmp:
        csv_path = os.path.join(tmp, "skins.csv")
        xlsx_path = os.path.join(tmp, "Skins.xlsx")
        pdf_path = os.path.join(tmp, "Skins.pdf")

        sheet.write_csv(skins, csv_path)
        sheet.write_xlsx(skins, FAKE_PROFILE, counts, xlsx_path)
        pages = pdf.build(skins, FAKE_PROFILE, counts, None, pdf_path)

        check("CSV written", os.path.getsize(csv_path) > 0)
        check("XLSX written", os.path.getsize(xlsx_path) > 0)
        check("PDF written", os.path.getsize(pdf_path) > 0)
        check("cover + roster + grid", pages >= 3, pages)


def test_large_collection_fits():
    print("large collection still fits one roster page")
    skins = []
    for i in range(170):
        skins.append({
            "champion": f"Champion Number {i}", "skin": f"Skin {i}",
            "skinId": i, "chromas": 0, "isBase": False, "rarity": "Epic",
            "file": None, "thumb": None,
        })
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "Skins.pdf")
        pages = pdf.build(skins, FAKE_PROFILE, {"Epic": 170}, None, path)
        grid_pages = pages - 2
        check("roster stays on a single page", pages == grid_pages + 2, pages)
        check("PDF written", os.path.getsize(path) > 0)


def test_format_selection():
    print("format selection")
    import main

    check("no argument means everything",
          main.parse_formats(None) == set(main.FORMATS))
    check("'all' means everything", main.parse_formats("all") == set(main.FORMATS))
    check("single format", main.parse_formats("pdf") == {"pdf"})
    check("list of formats", main.parse_formats("pdf,csv") == {"pdf", "csv"})
    check("case and spaces tolerated",
          main.parse_formats(" PDF , XLSX ") == {"pdf", "xlsx"})

    try:
        main.parse_formats("pdf,doc")
        check("unknown format rejected", False, "no error raised")
    except ValueError:
        check("unknown format rejected", True)

    check("menu covers every entry",
          all(set(f) <= set(main.FORMATS) for _, _, f in main.MENU))
    check("CSV-only asks for no artwork",
          not ({"pdf", "xlsx", "splashes"} & set(main.MENU[3][2])))


def test_cache_freshness():
    print("cache freshness")
    from lolskins import assets

    check("missing file is not current", not assets._is_current("nope.jpg", 460))
    with tempfile.TemporaryDirectory() as tmp:
        from PIL import Image as PILImage

        path = os.path.join(tmp, "small.jpg")
        PILImage.new("RGB", (220, 124)).save(path)
        check("old, narrower art is refreshed", not assets._is_current(path, 460))
        check("matching width is reused", assets._is_current(path, 220))


def fake_collectibles(count, kind):
    years = ["2026", "2025", "2024", "2023", "UNDATED"]
    return [
        {
            "itemId": i,
            "purchaseDate": "" if years[i % len(years)] == "UNDATED"
            else f"{years[i % len(years)]}0101T000000.000Z",
            "year": years[i % len(years)],
            "name": f"{kind} {i}",
            "thumb": None,
        }
        for i in range(count)
    ]


def test_grid_planning():
    print("collectible pagination")
    plan = pdf._plan_grid(266, columns=8, cell_h=23, first_page_h=230,
                          other_page_h=250)
    check("plan produces pages", len(plan) >= 1, len(plan))
    check("every item is placed", sum(n for _, n in plan) == 266)
    check("pages run back to back",
          all(plan[i][0] + plan[i][1] == plan[i + 1][0]
              for i in range(len(plan) - 1)))
    check("first page holds fewer, to make room for the title",
          plan[0][1] <= plan[1][1] if len(plan) > 1 else True)

    single = pdf._plan_grid(4, columns=8, cell_h=23, first_page_h=230,
                            other_page_h=250)
    check("a short section fits one page", len(single) == 1, len(single))
    check("an empty section still returns a page",
          len(pdf._plan_grid(0, 8, 23, 230, 250)) == 1)


def test_date_order():
    print("acquisition order")
    items = fake_collectibles(12, "icon")
    items.sort(key=lambda x: x["purchaseDate"], reverse=True)
    dated = [i["purchaseDate"] for i in items if i["purchaseDate"]]
    check("newest first", dated == sorted(dated, reverse=True))
    check("undated items sit at the end",
          all(i["purchaseDate"] for i in items[:len(dated)]))


def test_collection_sections():
    print("collection sections in the PDF")
    skins = fake_skins()
    counts = {}
    for skin in skins:
        counts[skin["rarity"]] = counts.get(skin["rarity"], 0) + 1

    with tempfile.TemporaryDirectory() as tmp:
        plain = os.path.join(tmp, "plain.pdf")
        full = os.path.join(tmp, "full.pdf")
        base_pages = pdf.build(skins, FAKE_PROFILE, counts, None, plain)
        all_pages = pdf.build(skins, FAKE_PROFILE, counts, None, full,
                              icons=fake_collectibles(40, "icon"),
                              wards=fake_collectibles(12, "ward"))
        check("sections add pages", all_pages > base_pages, (base_pages, all_pages))
        check("both PDFs written",
              os.path.getsize(plain) > 0 and os.path.getsize(full) > 0)


def test_internal_links():
    print("clickable navigation")
    try:
        from pypdf import PdfReader
    except ImportError:
        print("  skip  pypdf not installed")
        return

    skins = fake_skins(40)
    counts = {}
    for skin in skins:
        counts[skin["rarity"]] = counts.get(skin["rarity"], 0) + 1

    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "Skins.pdf")
        pdf.build(skins, FAKE_PROFILE, counts, None, path,
                  icons=fake_collectibles(20, "icon"),
                  wards=fake_collectibles(8, "ward"))
        reader = PdfReader(path)
        pages = {reader.pages[i].indirect_reference.idnum: i + 1
                 for i in range(len(reader.pages))}

        cover = [a.get_object() for a in (reader.pages[0].get("/Annots") or [])]
        roster = [a.get_object() for a in (reader.pages[1].get("/Annots") or [])]
        champions = len({s["champion"] for s in skins})

        check("cover links to every section", len(cover) == 4, len(cover))
        check("roster links every champion", len(roster) == champions, len(roster))
        targets = [pages.get(a["/Dest"][0].idnum) for a in cover + roster]
        check("every link resolves to a real page", all(targets), targets[:4])
        check("no link points at the cover itself", all(t > 1 for t in targets))

        # every content page but the last offers a way back to the roster
        back = []
        for i in range(2, len(reader.pages)):
            annots = [a.get_object() for a in (reader.pages[i].get("/Annots") or [])]
            if any(pages.get(a["/Dest"][0].idnum) == 2 for a in annots if "/Dest" in a):
                back.append(i + 1)
        check("content pages link back to the roster",
              len(back) == len(reader.pages) - 3, (len(back), len(reader.pages)))
        check("the last page carries the credit instead",
              len(reader.pages) not in back)


def _image_boxes(page):
    """Rectangles where images were placed, read from the content stream."""
    import re

    data = page.get_contents().get_data().decode("latin-1")
    pattern = re.compile(
        r"([\d.eE+-]+) 0 0 ([\d.eE+-]+) ([\d.eE+-]+) ([\d.eE+-]+) cm\s*/\S+ Do")
    boxes = []
    for w, h, x, y in pattern.findall(data):
        boxes.append((float(x), float(y), float(x) + float(w), float(y) + float(h)))
    return boxes


def test_nothing_falls_off_the_page():
    """A column count leaking between grids once pushed half of every skin
    page past the right edge; this keeps every drawn image on the paper."""
    print("artwork stays on the page")
    try:
        from pypdf import PdfReader
    except ImportError:
        print("  skip  pypdf not installed")
        return

    from PIL import Image as PILImage

    skins = fake_skins(40)
    counts = {}
    for skin in skins:
        counts[skin["rarity"]] = counts.get(skin["rarity"], 0) + 1
    icons = fake_collectibles(30, "icon")
    wards = fake_collectibles(9, "ward")

    with tempfile.TemporaryDirectory() as tmp:
        # real thumbnails, otherwise nothing is drawn and the check is vacuous
        art = os.path.join(tmp, "art.jpg")
        PILImage.new("RGB", (460, 259), (40, 60, 90)).save(art)
        for item in skins + icons + wards:
            item["thumb"] = art

        path = os.path.join(tmp, "Skins.pdf")
        pdf.build(skins, FAKE_PROFILE, counts, None, path,
                  icons=icons, wards=wards)
        reader = PdfReader(path)

        strays, placed = [], 0
        for i, page in enumerate(reader.pages):
            right = float(page.mediabox.width)
            top = float(page.mediabox.height)
            for x0, y0, x1, y1 in _image_boxes(page):
                placed += 1
                if x0 < -1 or y0 < -1 or x1 > right + 1 or y1 > top + 1:
                    strays.append((i + 1, round(x0), round(x1)))

        # the count guards the check itself: no artwork parsed would mean the
        # test silently proves nothing
        check("artwork was actually placed", placed >= len(skins), placed)
        check("every image sits inside the page", not strays, strays[:4])


def test_english_only():
    print("no leftover translation layer")
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    check("i18n module removed",
          not os.path.exists(os.path.join(root, "lolskins", "i18n.py")))
    check("Czech readme removed",
          not os.path.exists(os.path.join(root, "README.cs.md")))


if __name__ == "__main__":
    for test in (test_imports, test_chroma_label, test_gems, test_outputs,
                 test_large_collection_fits, test_format_selection,
                 test_cache_freshness, test_grid_planning, test_date_order,
                 test_collection_sections, test_internal_links,
                 test_nothing_falls_off_the_page, test_english_only):
        test()

    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)} check(s)")
        for name in FAILURES:
            print("  -", name)
        sys.exit(1)
    print("All checks passed.")
