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
import shutil
import subprocess
import sys
import time
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

FORMATS = ("pdf", "xlsx", "csv", "splashes", "data")

# what the interactive menu offers, in order
MENU = [
    ("Everything", "PDF, Excel, CSV, splash art and the raw data", FORMATS),
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
                   help="comma-separated: pdf, xlsx, csv, splashes, data, or "
                        "all (default: ask, or all when not asked)")
    p.add_argument("--clean", action="store_true",
                   help="delete the cached artwork once the export is written")
    p.add_argument("--output", metavar="DIR", help="where to write the results")
    p.add_argument("--lockfile", metavar="PATH",
                   help="path to the client's lockfile (only for odd installs)")
    p.add_argument("--no-pause", action="store_true",
                   help="close at once when finished, without the countdown")
    p.add_argument("--keep-open", action="store_true",
                   help="wait for Enter when finished instead of closing")
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


def pause(enabled, code=0, keep_open=False, seconds=6):
    """Closes by itself when the export worked, waits when it did not.

    An error nobody gets to read is no better than a silent failure, so a
    failed run always holds the window open.
    """
    if not enabled:
        sys.exit(code)
    if code == 0 and not keep_open:
        try:
            for left in range(seconds, 0, -1):
                print(f"\r  This window closes in {left}    ", end="", flush=True)
                time.sleep(1)
            print()
        except Exception:
            pass
    else:
        try:
            input("\nPress Enter to close…")
        except Exception:
            pass
    sys.exit(code)


def open_document(path):
    """Show the finished PDF in whatever the platform uses."""
    try:
        if sys.platform == "darwin":
            subprocess.run(["open", path], check=False)
        elif os.name == "nt":
            os.startfile(path)  # noqa: S606
        else:
            subprocess.run(["xdg-open", path], check=False)
    except Exception:
        pass


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
    collectibles = {}
    try:
        skins, profile = client.fetch_inventory(args.lockfile)
        if "pdf" in formats:
            collectibles = client.fetch_collectibles(args.lockfile)
    except client.ClientNotFound as e:
        print("\n" + str(e))
        pause(wait, 1)
    except Exception as e:
        print(f"\nCould not read data from the client: {e}")
        print("Make sure the League client is running and you are logged in.")
        pause(wait, 1)

    if "data" in formats:
        client.save(skins, profile, out)

    # ------------------------------------------------------------ step 2 --
    needs_art = bool(formats & {"pdf", "xlsx", "splashes"})
    print("\n[2/2] " + ("Downloading splash art and building the export…"
                        if needs_art else "Building the export…"))
    if needs_art:
        print("      (the first run takes a few minutes, then images are cached)")
    print()
    try:
        written = build_catalog(skins, profile, out, formats, collectibles)
    except Exception as e:
        print(f"\nExport failed: {e}")
        traceback.print_exc()
        pause(wait, 1)

    print("\n" + RULE)
    print("  DONE")
    print(RULE + "\n")
    print("Created:")
    width = max((len(os.path.basename(p)) for p in written), default=12) + 3
    for path in written:
        if os.path.isdir(path):
            count = len([f for f in os.listdir(path) if f.endswith(".jpg")])
            print(f"  {os.path.basename(path) + '/':<{width}} {count} images")
        elif os.path.exists(path):
            name = os.path.basename(path)
            print(f"  {name:<{width}} {os.path.getsize(path) / 1048576:.1f} MB")

    if args.clean:
        cache = paths.thumb_dir(out)
        if os.path.isdir(cache):
            files = sum(len(f) for _, _, f in os.walk(cache))
            shutil.rmtree(cache, ignore_errors=True)
            print(f"\nCleaned the artwork cache ({files} files). The next run "
                  "downloads it again.")

    catalog = next((p for p in written if p.lower().endswith(".pdf")), None)
    if not args.no_open and catalog and os.path.exists(catalog):
        open_document(catalog)
    pause(wait, 0, args.keep_open)


def build_catalog(all_skins, profile, out, formats=None, collectibles=None):
    """Writes the requested outputs. Returns the paths that were created."""
    formats = set(formats or FORMATS)
    collectibles = collectibles or {}
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

    assets.ensure_cache_version(out)

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

    names = paths.output_names(profile)
    written = []
    if "csv" in formats:
        print("Writing CSV…")
        path = os.path.join(out, names["csv"])
        sheet.write_csv(skins, path)
        written.append(path)
    if "xlsx" in formats:
        print("Writing XLSX…")
        path = os.path.join(out, names["xlsx"])
        sheet.write_xlsx(skins, profile, tier_counts, path)
        written.append(path)
    if "pdf" in formats:
        icons = wards = []
        if collectibles.get("icons") or collectibles.get("wards"):
            print("Downloading icons and ward skins…")
            icons = assets.download_collectibles(collectibles.get("icons", []),
                                                 "icons", out)
            wards = assets.download_collectibles(collectibles.get("wards", []),
                                                 "wards", out)
        gems = assets.fetch_gem_icons(out)
        print("Writing PDF…")
        path = os.path.join(out, names["pdf"])
        pdf.build(skins, profile, tier_counts, icon, path,
                  icons=icons, wards=wards, gems=gems)
        written.append(path)
    if keep_full:
        written.append(paths.splash_dir(out))
    if "data" in formats:
        written += [os.path.join(out, n) for n in ("skins.json", "profile.json")]
    return written


if __name__ == "__main__":
    main()
