"""Where the program reads and writes files."""

import os
import re
import sys

SPLASH_SUBDIR = "splashes"
THUMB_SUBDIR = ".thumbs"


def output_dir():
    """Next to the .exe when frozen, next to the project when run from source."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.getcwd()


def splash_dir(base=None):
    path = os.path.join(base or output_dir(), SPLASH_SUBDIR)
    os.makedirs(path, exist_ok=True)
    return path


def thumb_dir(base=None):
    path = os.path.join(base or output_dir(), THUMB_SUBDIR)
    os.makedirs(path, exist_ok=True)
    return path


def safe_filename(text):
    return re.sub(r'[\\/:*?"<>|]', "_", text).strip()


def display_name(profile):
    """Readable summoner name.

    Players often style their name as spaced-out letters ("Z I P E E K"); that
    is collapsed, while a genuine two-word name keeps its space.
    """
    parts = ((profile or {}).get("gameName") or "").split()
    if parts and all(len(p) == 1 for p in parts):
        return "".join(parts)
    return " ".join(parts)


def output_names(profile):
    """File names for one account, so exports from two accounts can coexist."""
    stem = safe_filename(display_name(profile)) or "Summoner"
    return {
        "pdf": f"{stem} - LoL Collection.pdf",
        "xlsx": f"{stem} - LoL Skins.xlsx",
        "csv": f"{stem} - LoL Skins.csv",
    }
