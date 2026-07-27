# LoL Skin Catalog 1.6.0

Turns your League of Legends collection into a printable PDF catalog — skins
with splash art and rarity gems, plus your summoner icons and ward skins — and
exports an Excel sheet and a CSV list alongside it.

## What changed since 1.5.1

- **Skin cards are dressed in their rarity.** A thin coloured outline was doing
  all the work; now each card carries a wash rising out of its caption, an
  accent bar along the foot, corner brackets around the art, a soft scrim
  blending the art into the caption and a bright rule beneath the gem — all in
  that tier's colour. Cards with no tier get the same treatment in a muted
  steel, so they still look designed without pretending to be rare.
- **Page numbers sit between short gold rules**, the way a printed book sets
  them.
- **The back link opens with an arrow** rather than a diamond, so it reads as a
  control instead of an ornament. It is drawn as vector, so no font has to
  carry the glyph.

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
SHA256  87C0883CFDF6300ED590B9F086C3768AB80EFA86F590C3637365BFF45E147B93  LoL-Skin-Catalog.zip
```
