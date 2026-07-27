# LoL Skin Catalog 1.8.0

Turns your League of Legends collection into a printable PDF catalog — skins
with their art and rarity gems, plus your summoner icons and ward skins — and
exports an Excel sheet and a CSV list alongside it.

## What changed since 1.7.0

- **Skin cards are square now**, the way the client's own collection cards are.
  The picture comes from Riot's square tile art, which is framed on the
  champion by hand, so the skin reads clearly even on a small card. Skins
  without a tile fall back to a centred crop of the splash.
- **Cards are smaller and denser**: five across and five down, 25 skins to a
  page instead of 15. The skin section drops from 19 pages to 11 and the whole
  catalog from 26 to 18.
- **The rarity gem straddles the bottom edge of the art**, as it does in game.
  That frees the full card width for the skin name, which is now centred under
  the gem with the champion beneath it.
- **A PDF-only export is much quicker**, because it fetches the small tile
  rather than the full splash. The wide splash art is downloaded only when you
  ask for the `splashes/` folder.

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

Results are named after your summoner and land next to the executable. The PDF
and the spreadsheet are self-contained, so you can forward either one to a
friend.

## What's in it

- Cover page with your profile icon, level, name, a rarity breakdown and a linked table of contents
- Champion roster: every champion, how many skins you own, and a link to their skins
- One card per skin, styled in the colours of its rarity gem
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
SHA256  32FE1E31F4B8F18CAB3DE4FEEBB4FEB886C773DF8789CECDF60E51C38014DCAE  LoL-Skin-Catalog.zip
```
