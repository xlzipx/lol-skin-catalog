# LoL Skin Catalog 1.3.0

Turns your League of Legends collection into a printable PDF catalog — skins
with splash art and rarity gems, plus your summoner icons and ward skins — and
exports an Excel sheet and a CSV list alongside it.

## What changed since 1.2.0

- **Summoner icons and ward skins are catalogued too.** They follow the skins as
  their own sections, grouped by the year you acquired them, newest first, the
  way the client's collection screen shows them. Icons without a purchase date
  land in a final group so the totals still match the client exactly.
- **The cover now has a table of contents.** Four plaques styled after the
  client's collection tabs name each section and the page it starts on. They are
  clickable, and the PDF carries a proper outline for your reader's sidebar.

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
- Champion roster: every champion and how many skins you own for them
- One card per skin — splash art framed in its rarity colour, name, champion and chroma count
- Summoner icons and ward skins, grouped by the year you got them
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
SHA256  646AB03A77C465A98AE036BF109B97366D3AF6B54CF32250731856DC75C09471  LoL-Skin-Catalog.zip
```
