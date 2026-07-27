# LoL Skin Catalog 1.5.1

Turns your League of Legends collection into a printable PDF catalog — skins
with splash art and rarity gems, plus your summoner icons and ward skins — and
exports an Excel sheet and a CSV list alongside it.

## What changed since 1.5.0

- **Page numbers moved to the foot of the page**, plain and centred, and left
  the top right corner.
- **The link back to the roster sits in the bottom right corner** and simply
  reads "back to roster".
- **Page headers and section titles are centred.**
- **The backdrop is a plain vertical fade again** — the light streaks are gone.
  It is now drawn as vector bands instead of an embedded image, which trims a
  megabyte off the executable and prints without resampling.

If you are coming from 1.4.0 or 1.4.1, note that those releases drew half of
every skin page off the paper. That was fixed in 1.5.0; regenerate your catalog
with this version.

## Download

| File | Size | What it is |
|---|---|---|
| `LoL-Skin-Catalog.zip` | 37.7 MB | Everything you need: the executable, instructions and a plain-Python fallback |

Source code is below if you would rather run it with Python.

## How to run it

1. Start League of Legends and log in. The lobby is enough — you do not have to play. Leave the client open.
2. Unzip the archive somewhere on your disk and run it **unzipped**, not from inside the ZIP.
3. Double-click `LoL-Skin-Catalog.exe`.
4. Choose what you want, or press Enter for everything.
5. The first run downloads several hundred images and takes a few minutes. The PDF opens by itself when it finishes.

Results land next to the executable. The PDF and the spreadsheet are
self-contained, so you can forward either one to a friend.

## What's in it

- Cover page with your profile icon, level, name, a rarity breakdown and a linked table of contents
- Champion roster: every champion, how many skins you own, and a link to their skins
- One card per skin — splash art framed in its rarity colour, name, champion and chroma count
- Summoner icons and ward skins, newest acquisition first
- Excel sheet with embedded thumbnails, colour-coded rarities and an autofilter

## Before you click

Windows SmartScreen will warn you on first launch, because the executable is not
signed with a paid certificate. Choose **More info → Run anyway**. Some antivirus
products also flag one-file PyInstaller builds as a false positive; if yours
removes it, the `no-exe` folder in the ZIP holds the same program as Python
scripts.

## Is it safe?

It reads data from the League client running on your own machine and sends
nothing anywhere. A handful of `GET` requests go to `127.0.0.1`, the artwork
comes from the public Community Dragon mirror, and nothing is ever written back
to the game. It never sees your Riot password. The full walkthrough is in the
[README](https://github.com/xlzipx/lol-skin-catalog#how-it-works).

Riot does not officially document the LCU API this relies on. Read-only tools
like this are widely used and long tolerated, but that is tolerance, not a
guarantee.

## Checksums

```
SHA256  E072FFEFA983A3A094468464726CFE28F7BE453CEAD23A045FA31C0FEB9DC3BC  LoL-Skin-Catalog.zip
```
