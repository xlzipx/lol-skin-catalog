# LoL Skin Catalog 1.5.0

Turns your League of Legends collection into a printable PDF catalog — skins
with splash art and rarity gems, plus your summoner icons and ward skins — and
exports an Excel sheet and a CSV list alongside it.

## Important fix

**Releases 1.4.0 and 1.4.1 drew half of every skin page off the paper.** A loop
added in 1.4.0 reused the variable that held the skin grid's column count, so
the grid laid its cards out in six columns instead of three, and three of them
fell past the right edge. Each page still carried all fifteen skins, but only
nine were visible.

If you generated a catalog with either of those versions, run this one again to
get a correct PDF. A new regression test now reads back where every image was
placed and fails if any of it lands outside the page.

## What else changed since 1.4.1

- **A new backdrop.** Pages fade vertically from `#031f2c` down to `#03101a`
  and carry soft teal light streaks, echoing the client's own background. Card
  panels and the roster stripes were retuned to match.

## Download

| File | Size | What it is |
|---|---|---|
| `LoL-Skin-Catalog.zip` | 38.7 MB | Everything you need: the executable, instructions and a plain-Python fallback |

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
- A link back to the roster at the foot of every page but the last
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
SHA256  9F1DCC436FF8834B93C51D73925F10B23237017BA3236C7A1FEDB9875A0A1ECA  LoL-Skin-Catalog.zip
```
