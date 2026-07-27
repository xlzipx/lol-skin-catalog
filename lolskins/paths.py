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
