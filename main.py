"""
LoL Skin Catalog - entry point.

Usage:
    python main.py                     write next to the current folder
    python main.py --output D:\\export  write somewhere else
    python main.py --lockfile "..."    point at the client manually
"""

import argparse
import json
import os
import sys
import traceback

if os.name == "nt":
    try:
        import ctypes

        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
    except Exception:
        pass
for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from lolskins import assets, client, paths, pdf, sheet  # noqa: E402

RULE = "─" * 58


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        prog="lol-skin-catalog",
        description="Export the League of Legends skins you own into PDF, XLSX and CSV.",
    )
    p.add_argument("--output", metavar="DIR", help="where to write the results")
    p.add_argument("--lockfile", metavar="PATH",
                   help="path to the client's lockfile (only for odd installs)")
    p.add_argument("--no-pause", action="store_true",
                   help="do not wait for Enter when finished")
    p.add_argument("--no-open", action="store_true",
                   help="do not open the PDF when finished")
    return p.parse_args(argv)


def pause(enabled, code=0):
    if enabled:
        try:
            input("\nPress Enter to close…")
        except Exception:
            pass
    sys.exit(code)


def main(argv=None):
    args = parse_args(argv)

    out = os.path.abspath(args.output) if args.output else paths.output_dir()
    os.makedirs(out, exist_ok=True)
    wait = not args.no_pause

    print(RULE)
    print("  LEAGUE OF LEGENDS SKIN CATALOG")
    print(RULE)
    print("\nOutput will be saved to:\n  " + out + "\n")

    # ------------------------------------------------------------ step 1 --
    print("[1/2] Reading data from the running client…")
    try:
        skins, profile = client.fetch_inventory(args.lockfile)
    except client.ClientNotFound as e:
        print("\n" + str(e))
        pause(wait, 1)
    except Exception as e:
        print(f"\nCould not read data from the client: {e}")
        print("Make sure the League client is running and you are logged in.")
        pause(wait, 1)

    client.save(skins, profile, out)

    # ------------------------------------------------------------ step 2 --
    print("\n[2/2] Downloading splash art and building the catalog…")
    print("      (the first run takes a few minutes, then images are cached)\n")
    try:
        catalog = build_catalog(skins, profile, out)
    except Exception as e:
        print(f"\nExport failed: {e}")
        traceback.print_exc()
        pause(wait, 1)

    print("\n" + RULE)
    print("  DONE")
    print(RULE + "\n")
    print("Created:")
    for name in ("Skins.pdf", "Skins.xlsx", "skins.csv"):
        path = os.path.join(out, name)
        if os.path.exists(path):
            print(f"  {name:<14} {os.path.getsize(path) / 1048576:.1f} MB")
    print("  splashes/      folder with splash art")

    if not args.no_open and os.path.exists(catalog):
        try:
            os.startfile(catalog)  # noqa: S606
        except Exception:
            pass
    pause(wait, 0)


def build_catalog(all_skins, profile, out):
    """Downloads art and writes every output. Returns the path to the PDF."""
    skins = [s for s in all_skins if not s["isBase"]]
    skins.sort(key=lambda x: (x["champion"].lower(), x["skin"].lower()))
    print(f"Skins to export: {len(skins)}")

    rarities = assets.fetch_rarities()
    for skin in skins:
        skin["rarity"] = rarities.get(skin["skinId"], "")

    tier_counts = {}
    for skin in skins:
        tier_counts[skin["rarity"]] = tier_counts.get(skin["rarity"], 0) + 1
    readable = {k or "No tier": v for k, v in tier_counts.items()}
    print("Rarities: " + json.dumps(readable))

    print("Downloading splash art…")
    assets.download_splashes(skins, out)
    icon = assets.fetch_profile_icon(profile.get("profileIconId"), out)

    print("Writing CSV…")
    sheet.write_csv(skins, os.path.join(out, "skins.csv"))
    print("Writing XLSX…")
    sheet.write_xlsx(skins, profile, tier_counts, os.path.join(out, "Skins.xlsx"))
    print("Writing PDF…")
    catalog = os.path.join(out, "Skins.pdf")
    pdf.build(skins, profile, tier_counts, icon, catalog)
    return catalog


if __name__ == "__main__":
    main()
