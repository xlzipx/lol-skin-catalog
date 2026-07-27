# LoL Skin Catalog 1.1.0

Turns the skins you own in League of Legends into a printable PDF catalog —
with splash art, rarity gems and chroma counts — plus an Excel sheet and a CSV
list.

## What changed since 1.0.0

- **Page two is now a champion roster.** The rarity gems used to be repeated
  there directly below the cover; they live on the cover alone now, and the
  freed space went into a much more readable list of every champion and the
  number of skins you own for them.
- **The cover labels say what they mean.** "Champions with skins" counts the
  champions in the catalog, "Champions owned" counts every champion you have
  unlocked — the two are no longer easy to confuse.
- **Rarity gems match the in-game side counts:** Legendary four, Mythic five,
  Ultimate six.
- **Bigger type** on the cover statistics and the rarity strip.
- **The last page credits the project** and links back to the repository.
- **English only.** The Czech translation and the `--lang` switch are gone; one
  language means one thing to keep correct.
- **Continuous integration**, running an offline build of every output on
  Ubuntu and Windows against Python 3.9 and 3.12.

## Download

| File | Size | What it is |
|---|---|---|
| `LoL-Skin-Catalog.zip` | 37.7 MB | Everything you need: the executable, instructions and a plain-Python fallback |

Source code is below if you would rather run it with Python.

## How to run it

1. Start League of Legends and log in. The lobby is enough — you do not have to play. Leave the client open.
2. Unzip the archive somewhere on your disk and run it **unzipped**, not from inside the ZIP.
3. Double-click `LoL-Skin-Catalog.exe`.
4. The first run downloads a few hundred images and takes a couple of minutes. The PDF opens by itself when it finishes.

Results land next to the executable: `Skins.pdf`, `Skins.xlsx`, `skins.csv` and
a `splashes/` folder. The PDF and the spreadsheet are self-contained, so you can
forward either one to a friend.

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
SHA256  59710C199784923DADB1F39C148FF34904610D9BB05CA0D562929262FFE9BF61  LoL-Skin-Catalog.zip
SHA256  548B11DA108AC711FD2869EF6D55E6D6797253F5809292C8B9FC947416AE54FB  LoL-Skin-Catalog.exe
```
