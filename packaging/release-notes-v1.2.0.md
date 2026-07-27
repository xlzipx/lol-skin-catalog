# LoL Skin Catalog 1.2.0

Turns the skins you own in League of Legends into a printable PDF catalog —
with splash art, rarity gems and chroma counts — plus an Excel sheet and a CSV
list.

## What changed since 1.1.0

- **Sharper splash art.** The pictures embedded in the catalog went from 220 to
  460 px wide, which is roughly 210 DPI on a card — crisp on screen and in
  print. The `splashes/` folder now holds 720 px art instead of 480 px. The PDF
  grows from about 2.4 MB to 6.6 MB as a result.
- **You choose what gets created.** The program asks whether you want
  everything, only the PDF, only Excel or only CSV — and produces nothing else.
  A PDF-only export no longer leaves a `splashes/` folder behind, and a
  CSV-only export downloads no artwork at all and finishes in about two
  seconds. From a command line the same choice is `--formats pdf,csv`.
- **Upgrades refresh the cache.** Previously downloaded art is checked against
  the current resolution, so coming from an older version replaces the smaller
  images automatically.

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
5. The first run downloads a few hundred images and takes a couple of minutes. The PDF opens by itself when it finishes.

Results land next to the executable. The PDF and the spreadsheet are
self-contained, so you can forward either one to a friend.

## What's in it

- Cover page with your profile icon, level, name and a rarity breakdown
- Champion roster: every champion and how many skins you own for them
- One card per skin — splash art framed in its rarity colour, name, champion and chroma count
- Excel sheet with embedded thumbnails, colour-coded rarities and an autofilter

## Before you click

Windows SmartScreen will warn you on first launch, because the executable is not
signed with a paid certificate. Choose **More info → Run anyway**. Some antivirus
products also flag one-file PyInstaller builds as a false positive; if yours
removes it, the `no-exe` folder in the ZIP holds the same program as Python
scripts.

## Is it safe?

It reads data from the League client running on your own machine and sends
nothing anywhere. Two `GET` requests go to `127.0.0.1`, the artwork comes from
the public Community Dragon mirror, and nothing is ever written back to the
game. It never sees your Riot password. The full walkthrough is in the
[README](https://github.com/xlzipx/lol-skin-catalog#how-it-works).

Riot does not officially document the LCU API this relies on. Read-only tools
like this are widely used and long tolerated, but that is tolerance, not a
guarantee.

## Checksums

```
SHA256  A14F9A4F059166CF2B1D04B22403C05B8217E20749C07213F272C1DE1B191736  LoL-Skin-Catalog.zip
```
