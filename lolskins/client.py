"""
Talks to the League Client Update (LCU) API - the local HTTP API the client
itself uses. Read-only: nothing is written back to the game.
"""

import base64
import json
import os
import re
import string
import subprocess
import sys

import requests
import urllib3

from .paths import output_dir

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Folders League is usually installed in, relative to a drive root.
SUBFOLDERS = [
    r"Riot Games\League of Legends",
    r"Program Files\Riot Games\League of Legends",
    r"Program Files (x86)\Riot Games\League of Legends",
    r"Games\Riot Games\League of Legends",
    r"Riot Games\League of Legends (TENCENT)",
]

MAC_PATHS = [
    "/Applications/League of Legends.app/Contents/LoL/lockfile",
    os.path.expanduser("~/Applications/League of Legends.app/Contents/LoL/lockfile"),
]

NOT_FOUND_EXE = """\
Could not connect to the League client.

  1) Start League of Legends and log in (the lobby is enough, you do not
     have to play), then run this program again.

  2) If the client is running and it still fails, find the file 'lockfile'
     in your League of Legends folder and drag it onto this .exe."""

NOT_FOUND_SCRIPT = """\
Could not connect to the League client.

  1) The League client must be running (logged in is enough).
  2) For a non-standard install, pass the path manually:
     python main.py --lockfile "path/to/League of Legends/lockfile\""""


class ClientNotFound(RuntimeError):
    pass


def _client_command_line():
    """Command line of the running LeagueClientUx.exe (Windows), else ''."""
    if os.name != "nt":
        return ""
    commands = [
        # PowerShell/CIM works on Win11 too, where wmic is gone
        [
            "powershell", "-NoProfile", "-NonInteractive", "-Command",
            "Get-CimInstance Win32_Process -Filter \"Name='LeagueClientUx.exe'\""
            " | Select-Object -ExpandProperty CommandLine",
        ],
        ["wmic", "process", "where", "name='LeagueClientUx.exe'", "get", "commandline"],
    ]
    for command in commands:
        try:
            out = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=25,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            ).stdout
        except Exception:
            continue
        if out and "--app-port" in out:
            return out
    return ""


def _credentials_from_process():
    """Port and auth token straight from the running client's arguments."""
    line = _client_command_line()
    if not line:
        return None
    port = re.search(r"--app-port=(\d+)", line)
    token = re.search(r"--remoting-auth-token=([\w.\-_]+)", line)
    if port and token:
        return port.group(1), token.group(1)
    return None


def _lockfile_from_process():
    """Locate the lockfile via the folder the client actually runs from."""
    line = _client_command_line()
    if not line:
        return None
    # the client quotes the whole argument ("--install-directory=C:\Riot Games\..."),
    # so the value ends at a quote; older builds end it at the next " --"
    paths = []
    for m in re.finditer(r"--install-directory=([^\"\r\n]+)", line):
        paths.append(re.split(r"\s+--", m.group(1))[0].strip())
    # fallback: path of the executable itself, may use forward slashes
    paths += re.findall(r"([A-Za-z]:[\\/][^\"\r\n]*?)[\\/]LeagueClientUx\.exe", line)
    for path in paths:
        candidate = os.path.join(path.strip(), "lockfile")
        if os.path.exists(candidate):
            return candidate
    return None


def find_lockfile(explicit=None):
    """Explicit path > env var > client process > scan of every drive."""
    if explicit and os.path.exists(explicit):
        return explicit
    from_env = os.environ.get("LOL_LOCKFILE")
    if from_env and os.path.exists(from_env):
        return from_env

    from_process = _lockfile_from_process()
    if from_process:
        return from_process

    candidates = []
    if os.name == "nt":
        for letter in string.ascii_uppercase:
            root = f"{letter}:\\"
            if not os.path.exists(root):
                continue
            for sub in SUBFOLDERS:
                candidates.append(os.path.join(root, sub, "lockfile"))
    else:
        candidates = MAC_PATHS

    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def _session(port, password, protocol="https"):
    token = base64.b64encode(f"riot:{password}".encode()).decode()
    s = requests.Session()
    s.verify = False  # the client uses a self-signed certificate on localhost
    s.headers.update({"Authorization": f"Basic {token}"})
    return s, f"{protocol}://127.0.0.1:{port}"


def connect(lockfile=None, log=print):
    """Returns (session, base_url) for the running client."""
    credentials = _credentials_from_process()
    if credentials:
        port, password = credentials
        log(f"Client found via its running process (port {port})")
        return _session(port, password)

    path = find_lockfile(lockfile)
    if not path:
        raise ClientNotFound(
            NOT_FOUND_EXE if getattr(sys, "frozen", False) else NOT_FOUND_SCRIPT
        )
    log(f"Lockfile: {path}")
    with open(path, "r", encoding="utf-8") as f:
        parts = f.read().strip().split(":")
    return _session(parts[2], parts[3], parts[4])


def fetch_inventory(lockfile=None, log=print):
    """Reads owned skins and profile info. Returns (skins, profile)."""
    s, base = connect(lockfile, log=log)

    me = s.get(f"{base}/lol-summoner/v1/current-summoner").json()
    log(f"Logged in as: {me.get('gameName') or me.get('displayName')}")

    champions = s.get(
        f"{base}/lol-champions/v1/inventories/{me['summonerId']}/champions"
    ).json()

    skins = []
    chromas_total = 0
    chromas_on_skins = 0

    for champion in champions:
        for skin in champion.get("skins", []):
            if not (skin.get("ownership") or {}).get("owned"):
                continue
            is_base = bool(skin.get("isBase"))
            skins.append({
                "champion": champion["name"],
                "skin": skin["name"],
                "skinId": skin["id"],
                "splashPath": skin.get("splashPath") or "",
                "tilePath": skin.get("tilePath") or "",
                "chromas": len(skin.get("chromas") or []),
                "isBase": is_base,
            })
            if is_base:
                continue
            owned = sum(
                1 for ch in (skin.get("chromas") or [])
                if (ch.get("ownership") or {}).get("owned")
            )
            chromas_total += owned
            if owned:
                chromas_on_skins += 1

    skins.sort(key=lambda x: (x["champion"].lower(), x["skin"].lower()))
    log(f"Owned skins (including base): {len(skins)}")
    log(f"Real skins (base excluded): {sum(1 for s_ in skins if not s_['isBase'])}")

    profile = {
        "gameName": me.get("gameName") or me.get("displayName") or "",
        "tagLine": me.get("tagLine") or "",
        "level": me.get("summonerLevel") or 0,
        "profileIconId": me.get("profileIconId") or 0,
        "championsOwned": sum(
            1 for c in champions if (c.get("ownership") or {}).get("owned")
        ),
        "chromasOwned": chromas_total,
        "skinsWithChroma": chromas_on_skins,
    }
    return skins, profile


COLLECTIBLES = (("icons", "SUMMONER_ICON"), ("wards", "WARD_SKIN"))


def fetch_collectibles(lockfile=None, log=print, session=None):
    """Summoner icons and ward skins, newest acquisition first.

    Every item the endpoint returns is counted, which is what the client's own
    totals do: some starter icons carry no purchase date and the default ward
    is free, yet the collection screen still lists them.
    """
    if session:
        s, base = session
    else:
        s, base = connect(lockfile, log=log)

    out = {}
    for key, inventory_type in COLLECTIBLES:
        try:
            items = s.get(
                f"{base}/lol-inventory/v2/inventory/{inventory_type}", timeout=30
            ).json()
        except Exception as e:
            log(f"Could not read {inventory_type}: {e}")
            out[key] = []
            continue
        if not isinstance(items, list):
            out[key] = []
            continue

        collected = []
        for item in items:
            # "20181125T081240.000Z" -> "2018"
            stamp = (item.get("purchaseDate") or "")[:4]
            collected.append({
                "itemId": item.get("itemId"),
                "purchaseDate": item.get("purchaseDate") or "",
                "year": stamp if stamp.isdigit() else "UNDATED",
                "free": item.get("ownershipType") == "F2P",
            })
        collected.sort(key=lambda x: x["purchaseDate"], reverse=True)
        out[key] = collected
        log(f"{key.capitalize()} owned: {len(collected)}")

    return out


def save(skins, profile, folder=None, log=print):
    folder = folder or output_dir()
    for name, data in (("skins.json", skins), ("profile.json", profile)):
        with open(os.path.join(folder, name), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        log(f"Saved to {name}")
