"""
Downloads splash art and rarity data from Community Dragon - a public,
community-run mirror of the game's own asset files. No login involved.
"""

import io
import os
import shutil

import requests
from PIL import Image

from .paths import safe_filename, splash_dir, thumb_dir
from .theme import RARITY_ENUM, TIERS

CDRAGON = (
    "https://raw.communitydragon.org/latest/plugins"
    "/rcp-be-lol-game-data/global/default"
)

SPLASH_WIDTH = 720   # what is kept in splashes/, full uncropped art
# Catalog cards use Riot's own square tile, which ships at exactly 380 px.
# Across a 31 mm card that is about 310 DPI, so it is taken at native size -
# no resampling at all.
THUMB_WIDTH = 380


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


# Raise this whenever cached artwork would come out different than before.
# The width check alone cannot notice a change in how an image is processed,
# so without a stamp an old cache would quietly hide the improvement.
CACHE_VERSION = 2


def ensure_cache_version(base=None, log=print):
    """Drops the cache when the way artwork is produced has changed."""
    folder = thumb_dir(base)
    stamp = os.path.join(folder, "cache-version.txt")
    current = None
    if os.path.exists(stamp):
        try:
            with open(stamp, encoding="utf-8") as f:
                current = int(f.read().strip())
        except Exception:
            current = None

    if current != CACHE_VERSION:
        if current is not None:
            log("Artwork handling changed since the last run; fetching it again.")
        for name in os.listdir(folder):
            path = os.path.join(folder, name)
            try:
                shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
            except Exception:
                pass
        with open(stamp, "w", encoding="utf-8") as f:
            f.write(str(CACHE_VERSION))


def _on_panel(img):
    """Flattens artwork onto the card colour, transparent or not.

    Some ward art ships as plain RGB with the black backdrop baked in. Those
    get the backdrop keyed out by flooding inwards from the corners, which
    leaves dark areas inside the ward alone - a plain brightness threshold
    would punch holes in them.
    """
    from PIL import ImageDraw, ImageFilter

    if img.mode in ("RGBA", "LA", "P"):
        rgba = img.convert("RGBA")
        alpha = rgba.getchannel("A")
        if alpha.getextrema()[0] < 250:      # genuinely transparent somewhere
            flat = Image.new("RGB", rgba.size, PANEL_RGB)
            flat.paste(rgba, mask=alpha)
            return flat
        img = rgba

    rgb = img.convert("RGB")
    corners = [(0, 0), (rgb.width - 1, 0), (0, rgb.height - 1),
               (rgb.width - 1, rgb.height - 1)]
    if not any(sum(rgb.getpixel(p)) < 60 for p in corners):
        return rgb                            # nothing dark to key out

    SENTINEL = (255, 0, 255)
    work = rgb.copy()
    for corner in corners:
        if sum(work.getpixel(corner)) < 60:
            ImageDraw.floodfill(work, corner, SENTINEL, thresh=45)

    mask = Image.new("L", rgb.size, 255)
    source, target = work.load(), mask.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            if source[x, y] == SENTINEL:
                target[x, y] = 0
    mask = mask.filter(ImageFilter.GaussianBlur(0.6))

    flat = Image.new("RGB", rgb.size, PANEL_RGB)
    flat.paste(rgb, mask=mask)
    return flat


def fetch_gem_icons(base=None, log=print):
    """Riot's own rarity gems. Returns {tier: path}.

    Only the six tiers the client actually shows have artwork; the legacy
    "Rare" tier is in the data but has no gem, so it simply gets none here.
    """
    folder = os.path.join(thumb_dir(base), "gems")
    os.makedirs(folder, exist_ok=True)
    session = requests.Session()
    found = {}

    for tier in TIERS:
        target = os.path.join(folder, f"{tier.lower()}.png")
        if os.path.exists(target):
            found[tier] = target
            continue
        try:
            r = session.get(f"{CDRAGON}/v1/rarity-gem-icons/{tier.lower()}.png",
                            timeout=30)
            if r.status_code != 200:
                continue
            Image.open(io.BytesIO(r.content)).convert("RGBA").save(target)
            found[tier] = target
        except Exception as e:
            log(f"Could not download the {tier} gem: {e}")

    return found


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
            img = _on_panel(Image.open(io.BytesIO(r.content)))
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

        # Two different sources: the wide splash for splashes/, and Riot's own
        # square tile for the catalog card. The tile is hand-framed on the
        # champion, so it beats guessing a crop out of the splash.
        jobs = []
        if skin["file"] and not _is_current(skin["file"], SPLASH_WIDTH):
            jobs.append(("file", skin.get("splashPath") or skin.get("tilePath"),
                         SPLASH_WIDTH, False))
        if skin["thumb"] and not _is_current(skin["thumb"], THUMB_WIDTH):
            jobs.append(("thumb", skin.get("tilePath") or skin.get("splashPath"),
                         THUMB_WIDTH, True))
        if not jobs:
            continue

        for key, path, width, square in jobs:
            if not path:
                skin[key] = None
                continue
            url = CDRAGON + path.lower().replace("/lol-game-data/assets", "")
            try:
                r = session.get(url, timeout=60)
                if r.status_code != 200:
                    log(f"[{i}] HTTP {r.status_code}: {name}")
                    skin[key] = None
                    continue
                img = Image.open(io.BytesIO(r.content)).convert("RGB")
                if square:
                    if img.width != img.height:
                        # only reached when a skin has no tile and we fall back
                        side = min(img.width, img.height)
                        left = (img.width - side) // 2
                        top = (img.height - side) // 2
                        img = img.crop((left, top, left + side, top + side))
                    if img.size != (width, width):
                        img = img.resize((width, width), Image.LANCZOS)
                else:
                    height = max(1, round(img.height * width / img.width))
                    img = img.resize((width, height), Image.LANCZOS)
                # 86 costs about 3/255 against Riot's original and saves a
                # quarter of the bytes - invisible on a 31 mm card
                img.save(skin[key], "JPEG", quality=86, optimize=True)
            except Exception as e:
                log(f"[{i}] {name}: {e}")
                skin[key] = None

        if i % 25 == 0 or i == len(skins):
            log(f"  downloaded {i}/{len(skins)}")
