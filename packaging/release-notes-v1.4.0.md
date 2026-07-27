# LoL Skin Catalog 1.4.0

Turns your League of Legends collection into a printable PDF catalog — skins
with splash art and rarity gems, plus your summoner icons and ward skins — and
exports an Excel sheet and a CSV list alongside it.

## What changed since 1.3.1

- **Icons and wards are one continuous grid now.** They still run newest first
  by acquisition date, but without a separate heading for every year, which
  packs them far more densely. On a test account the catalog went from 30 pages
  to 26. Each section opens with its own title and count instead.
- **A way back from anywhere.** Every page but the last carries a small link at
  the foot back to the champion roster, so twenty pages deep is one click from
  the index.
- **The cover plaques say "PAGE 3" rather than just "3".** Every other figure on
  the cover is a count — 272 skins, 121 champions, 18 legendary — so a bare
  number read as one too.

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
SHA256  36237FEDA815D477410D8EBA3AF4D4A5655131C041991A7E8E25F6ACF97EB257  LoL-Skin-Catalog.zip
```
