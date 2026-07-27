"""
Downloads splash art and rarity data from Community Dragon - a public,
community-run mirror of the game's own asset files. No login involved.
"""

import io
import os

import requests
from PIL import Image

from .paths import safe_filename, splash_dir, thumb_dir
from .theme import RARITY_ENUM

CDRAGON = (
    "https://raw.communitydragon.org/latest/plugins"
    "/rcp-be-lol-game-data/global/default"
)

SPLASH_WIDTH = 480   # what is kept in splashes/
THUMB_WIDTH = 220    # what gets embedded into the PDF and XLSX


def fetch_rarities(log=print):
    """Skin tier per skin id. The LCU inventory does not expose it."""
    try:
        data = requests.get(CDRAGON + "/v1/skins.json", timeout=60).json()
    except Exception as e:
        log(f"Could not download rarity data: {e}")
        return {}
    return {
        int(sid): RARITY_ENUM.get(v.get("rarity", ""), "")
        for sid, v in data.items()
    }


def fetch_profile_icon(icon_id, base=None, log=print):
    if not icon_id:
        return None
    target = os.path.join(thumb_dir(base), f"profile_{icon_id}.jpg")
    if os.path.exists(target):
        return target
    try:
        r = requests.get(f"{CDRAGON}/v1/profile-icons/{icon_id}.jpg", timeout=60)
        if r.status_code != 200:
            return None
        Image.open(io.BytesIO(r.content)).convert("RGB").save(target, "JPEG", quality=92)
        return target
    except Exception as e:
        log(f"Could not download the profile icon: {e}")
        return None


def download_splashes(skins, base=None, log=print):
    """Fills each skin with 'file' and 'thumb'. Already downloaded art is reused."""
    splashes = splash_dir(base)
    thumbs = thumb_dir(base)
    session = requests.Session()

    for i, skin in enumerate(skins, 1):
        name = safe_filename(f"{skin['champion']} - {skin['skin']}") + ".jpg"
        skin["file"] = os.path.join(splashes, name)
        skin["thumb"] = os.path.join(thumbs, name)
        if os.path.exists(skin["file"]) and os.path.exists(skin["thumb"]):
            continue

        path = skin.get("splashPath") or skin.get("tilePath")
        if not path:
            skin["file"] = skin["thumb"] = None
            continue

        url = CDRAGON + path.lower().replace("/lol-game-data/assets", "")
        try:
            r = session.get(url, timeout=60)
            if r.status_code != 200:
                log(f"[{i}] HTTP {r.status_code}: {name}")
                skin["file"] = skin["thumb"] = None
                continue
            img = Image.open(io.BytesIO(r.content)).convert("RGB")
            for target, width in ((skin["file"], SPLASH_WIDTH), (skin["thumb"], THUMB_WIDTH)):
                height = max(1, round(img.height * width / img.width))
                img.resize((width, height), Image.LANCZOS).save(
                    target, "JPEG", quality=88
                )
            if i % 25 == 0 or i == len(skins):
                log(f"  downloaded {i}/{len(skins)}")
        except Exception as e:
            log(f"[{i}] {name}: {e}")
            skin["file"] = skin["thumb"] = None
