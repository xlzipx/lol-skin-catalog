# LoL Skin Catalog 1.9.0

Turns your League of Legends collection into a printable PDF catalog — skins
with their art and rarity gems, plus your summoner icons and ward skins — and
exports an Excel sheet and a CSV list alongside it.

This release came out of an audit of what each export actually leaves on disk.

## Fixed

- **A CSV-only export now really does leave one CSV and nothing else.**
  `skins.json` and `profile.json` were written on every run whatever format you
  picked, even though nothing ever reads them back — leftovers from when this
  was two separate scripts.
- **Excel rows are back to a sensible depth.** When skin art went square in
  1.8.0, rows grew to 162 points, nearly twice their previous height. The
  thumbnail is now sized by height, so a row is the same depth whatever shape
  the art happens to be.

## Added

- **`data` is a format of its own.** Ask for it, or take `all`, and you get the
  raw client dump. Otherwise it is not written.
- **`--clean`** deletes the cached artwork once the export is finished, for
  anyone who wants the document and no working files left behind.

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
SHA256  D19AA1494C1132703B6A6EB969B3FFCA21CED74F09C955A0F0A4BAB128E0A1CA  LoL-Skin-Catalog.zip
```
