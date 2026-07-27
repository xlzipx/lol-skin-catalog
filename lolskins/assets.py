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

SPLASH_WIDTH = 720   # what is kept in splashes/
# What gets embedded into the PDF and XLSX. A catalog card is about 55 mm
# wide, so 460 px lands at roughly 210 DPI - crisp in print and on screen.
THUMB_WIDTH = 460


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


ICON_WIDTH = 180    # summoner icons are square
WARD_WIDTH = 220    # ward art is transparent PNG, flattened onto the panel colour
PANEL_RGB = (16, 28, 50)

CATALOGS = {
    "icons": ("/v1/summoner-icons.json", "title", "imagePath"),
    "wards": ("/v1/ward-skins.json", "name", "wardImagePath"),
}


def fetch_catalog(kind, log=print):
    """{item id: {'name', 'path'}} for summoner icons or ward skins."""
    endpoint, name_key, path_key = CATALOGS[kind]
    try:
        data = requests.get(CDRAGON + endpoint, timeout=60).json()
    except Exception as e:
        log(f"Could not download the {kind} catalog: {e}")
        return {}
    return {
        entry["id"]: {
            "name": entry.get(name_key) or f"#{entry['id']}",
            "path": entry.get(path_key) or "",
        }
        for entry in data
        if isinstance(entry, dict) and "id" in entry
    }


def download_collectibles(items, kind, base=None, log=print):
    """Fills each item with 'name' and 'thumb'. Unknown ids are dropped."""
    catalog = fetch_catalog(kind, log=log)
    if not catalog:
        return []

    folder = os.path.join(thumb_dir(base), kind)
    os.makedirs(folder, exist_ok=True)
    width = ICON_WIDTH if kind == "icons" else WARD_WIDTH
    session = requests.Session()
    kept = []

    for i, item in enumerate(items, 1):
        entry = catalog.get(item["itemId"])
        if not entry or not entry["path"]:
            continue
        item["name"] = entry["name"]
        item["thumb"] = os.path.join(folder, f"{item['itemId']}.jpg")
        kept.append(item)
        if _is_current(item["thumb"], width):
            continue

        url = CDRAGON + entry["path"].lower().replace("/lol-game-data/assets", "")
        try:
            r = session.get(url, timeout=60)
            if r.status_code != 200:
                item["thumb"] = None
                continue
            img = Image.open(io.BytesIO(r.content))
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGBA")
                flat = Image.new("RGB", img.size, PANEL_RGB)
                flat.paste(img, mask=img.split()[-1])
                img = flat
            else:
                img = img.convert("RGB")
            height = max(1, round(img.height * width / img.width))
            img.resize((width, height), Image.LANCZOS).save(
                item["thumb"], "JPEG", quality=88
            )
            if i % 50 == 0 or i == len(items):
                log(f"  downloaded {i}/{len(items)}")
        except Exception as e:
            log(f"[{i}] {kind} {item['itemId']}: {e}")
            item["thumb"] = None

    return kept


def _is_current(path, width):
    """True when the cached file already has the width we want.

    Checking the size means an upgrade that raises the resolution refreshes
    old, smaller art instead of silently reusing it.
    """
    if not os.path.exists(path):
        return False
    try:
        with Image.open(path) as im:
            return im.width == width
    except Exception:
        return False


def download_splashes(skins, base=None, log=print, keep_full=True, need_thumbs=True):
    """Fills each skin with 'file' and 'thumb'. Already downloaded art is reused.

    keep_full   also write the full-size art into splashes/
    need_thumbs write the smaller copies the PDF and XLSX embed

    With both switched off nothing is downloaded at all, which is what a
    CSV-only export wants.
    """
    if not keep_full and not need_thumbs:
        for skin in skins:
            skin["file"] = skin["thumb"] = None
        return

    splashes = splash_dir(base) if keep_full else None
    thumbs = thumb_dir(base) if need_thumbs else None
    session = requests.Session()

    for i, skin in enumerate(skins, 1):
        name = safe_filename(f"{skin['champion']} - {skin['skin']}") + ".jpg"
        skin["file"] = os.path.join(splashes, name) if splashes else None
        skin["thumb"] = os.path.join(thumbs, name) if thumbs else None

        wanted = [(skin[key], width) for key, width in
                  (("file", SPLASH_WIDTH), ("thumb", THUMB_WIDTH)) if skin[key]]
        if all(_is_current(target, width) for target, width in wanted):
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
            for target, width in wanted:
                if _is_current(target, width):
                    continue
                height = max(1, round(img.height * width / img.width))
                img.resize((width, height), Image.LANCZOS).save(
                    target, "JPEG", quality=88
                )
            if i % 25 == 0 or i == len(skins):
                log(f"  downloaded {i}/{len(skins)}")
        except Exception as e:
            log(f"[{i}] {name}: {e}")
            skin["file"] = skin["thumb"] = None
