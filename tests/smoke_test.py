"""
Offline smoke test - builds every output from synthetic data.

Needs no League client and no network, so it can run in CI.

    python tests/smoke_test.py
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lolskins import i18n, pdf, sheet, theme  # noqa: E402

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


def test_translations():
    print("translations")
    missing = [
        f"{key}:{lang}"
        for key, value in i18n.STRINGS.items()
        for lang in i18n.LANGUAGES
        if not value.get(lang)
    ]
    check("every string exists in all languages", not missing, missing[:5])
    check("t() falls back for unknown keys", i18n.t("definitely_not_a_key") == "definitely_not_a_key")


def test_chromas():
    print("chroma wording")
    for lang in i18n.LANGUAGES:
        i18n.set_language(lang)
        check(f"[{lang}] singular", i18n.chromas(1) == "1 chroma", i18n.chromas(1))
        check(f"[{lang}] plural", i18n.chromas(6) == "6 chromas", i18n.chromas(6))
        check(f"[{lang}] no declined form", "chromat" not in i18n.chromas(5).lower())


def test_language_detection():
    print("language detection")
    original = i18n._locale_candidates
    cases = [
        (["cs_CZ"], "cs"), (["cs-CZ"], "cs"), (["Czech_Czechia"], "cs"),
        (["cs_CZ.UTF-8"], "cs"), (["en_US"], "en"), (["de_DE"], "en"),
        (["sk_SK"], "en"), ([], "en"),
    ]
    try:
        for candidates, expected in cases:
            i18n._locale_candidates = lambda c=candidates: c
            result = i18n.detect_language()
            check(f"{candidates or '(none)'} -> {expected}", result == expected, result)
    finally:
        i18n._locale_candidates = original


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


def test_outputs():
    print("document build")
    skins = fake_skins()
    counts = {}
    for skin in skins:
        counts[skin["rarity"]] = counts.get(skin["rarity"], 0) + 1

    for lang in i18n.LANGUAGES:
        i18n.set_language(lang)
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = os.path.join(tmp, "skins.csv")
            xlsx_path = os.path.join(tmp, "Skins.xlsx")
            pdf_path = os.path.join(tmp, "Skins.pdf")

            sheet.write_csv(skins, csv_path)
            sheet.write_xlsx(skins, FAKE_PROFILE, counts, xlsx_path)
            pages = pdf.build(skins, FAKE_PROFILE, counts, None, pdf_path)

            check(f"[{lang}] CSV written", os.path.getsize(csv_path) > 0)
            check(f"[{lang}] XLSX written", os.path.getsize(xlsx_path) > 0)
            check(f"[{lang}] PDF written", os.path.getsize(pdf_path) > 0)
            check(f"[{lang}] cover + summary + grid", pages >= 3, pages)


def test_imports():
    print("imports")
    from lolskins import assets, client, paths  # noqa: F401

    check("client module imports", hasattr(client, "fetch_inventory"))
    check("assets module imports", hasattr(assets, "download_splashes"))
    check("safe_filename strips separators", "/" not in paths.safe_filename("a/b:c"))


if __name__ == "__main__":
    for test in (test_imports, test_translations, test_chromas,
                 test_language_detection, test_gems, test_outputs):
        test()

    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)} check(s)")
        for name in FAILURES:
            print("  -", name)
        sys.exit(1)
    print("All checks passed.")
