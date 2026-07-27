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

FORMATS = ("pdf", "xlsx", "csv", "splashes")

# what the interactive menu offers, in order
MENU = [
    ("Everything", "PDF, Excel, CSV and the splash art folder", FORMATS),
    ("PDF only", "just the catalog", ("pdf",)),
    ("Excel only", "just the spreadsheet", ("xlsx",)),
    ("CSV only", "fastest, downloads no images at all", ("csv",)),
]


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        prog="lol-skin-catalog",
        description="Export the League of Legends skins you own into PDF, XLSX and CSV.",
    )
    p.add_argument("--formats", metavar="LIST",
                   help="comma-separated: pdf, xlsx, csv, splashes, or all "
                        "(default: ask, or all when not asked)")
    p.add_argument("--output", metavar="DIR", help="where to write the results")
    p.add_argument("--lockfile", metavar="PATH",
                   help="path to the client's lockfile (only for odd installs)")
    p.add_argument("--no-pause", action="store_true",
                   help="do not wait for Enter when finished")
    p.add_argument("--no-open", action="store_true",
                   help="do not open the PDF when finished")
    return p.parse_args(argv)


def parse_formats(value):
    """'pdf,csv' or 'all' -> a set of format names. Raises ValueError on junk."""
    if not value:
        return set(FORMATS)
    wanted = {part.strip().lower() for part in value.split(",") if part.strip()}
    if "all" in wanted:
        return set(FORMATS)
    unknown = wanted - set(FORMATS)
    if unknown:
        raise ValueError(
            f"unknown format(s): {', '.join(sorted(unknown))}. "
            f"Choose from: {', '.join(FORMATS)}, all"
        )
    return wanted


def ask_formats():
    """Menu for people who double-clicked the executable."""
    print("What should I create?\n")
    for i, (title, hint, _) in enumerate(MENU, 1):
        print(f"  [{i}] {title:<12} {hint}")
    try:
        answer = input(f"\nChoice [1-{len(MENU)}], Enter for 1: ").strip()
    except Exception:
        return set(FORMATS)
    if answer.isdigit() and 1 <= int(answer) <= len(MENU):
        return set(MENU[int(answer) - 1][2])
    return set(FORMATS)


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

    try:
        formats = parse_formats(args.formats)
    except ValueError as e:
        print(f"{e}\n")
        pause(wait, 2)
    # only ask when nothing was requested and somebody is actually watching
    if not args.formats and wait and sys.stdin and sys.stdin.isatty():
        formats = ask_formats()
        print()

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
    needs_art = bool(formats & {"pdf", "xlsx", "splashes"})
    print("\n[2/2] " + ("Downloading splash art and building the export…"
                        if needs_art else "Building the export…"))
    if needs_art:
        print("      (the first run takes a few minutes, then images are cached)")
    print()
    try:
        written = build_catalog(skins, profile, out, formats)
    except Exception as e:
        print(f"\nExport failed: {e}")
        traceback.print_exc()
        pause(wait, 1)

    print("\n" + RULE)
    print("  DONE")
    print(RULE + "\n")
    print("Created:")
    for path in written:
        if os.path.isdir(path):
            count = len([f for f in os.listdir(path) if f.endswith(".jpg")])
            print(f"  {os.path.basename(path) + '/':<14} {count} images")
        elif os.path.exists(path):
            name = os.path.basename(path)
            print(f"  {name:<14} {os.path.getsize(path) / 1048576:.1f} MB")

    catalog = os.path.join(out, "Skins.pdf")
    if not args.no_open and "pdf" in formats and os.path.exists(catalog):
        try:
            os.startfile(catalog)  # noqa: S606
        except Exception:
            pass
    pause(wait, 0)


def build_catalog(all_skins, profile, out, formats=None):
    """Writes the requested outputs. Returns the paths that were created."""
    formats = set(formats or FORMATS)
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

    keep_full = "splashes" in formats
    need_thumbs = bool(formats & {"pdf", "xlsx"})
    icon = None
    if keep_full or need_thumbs:
        print("Downloading splash art…")
        assets.download_splashes(skins, out, keep_full=keep_full,
                                 need_thumbs=need_thumbs)
    else:
        assets.download_splashes(skins, out, keep_full=False, need_thumbs=False)
    if "pdf" in formats:
        icon = assets.fetch_profile_icon(profile.get("profileIconId"), out)

    written = []
    if "csv" in formats:
        print("Writing CSV…")
        path = os.path.join(out, "skins.csv")
        sheet.write_csv(skins, path)
        written.append(path)
    if "xlsx" in formats:
        print("Writing XLSX…")
        path = os.path.join(out, "Skins.xlsx")
        sheet.write_xlsx(skins, profile, tier_counts, path)
        written.append(path)
    if "pdf" in formats:
        print("Writing PDF…")
        path = os.path.join(out, "Skins.pdf")
        pdf.build(skins, profile, tier_counts, icon, path)
        written.append(path)
    if keep_full:
        written.append(paths.splash_dir(out))
    return written


if __name__ == "__main__":
    main()
