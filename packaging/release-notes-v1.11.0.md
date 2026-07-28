# LoL Skin Catalog 1.11.0

Turns your League of Legends collection into a printable PDF catalog — skins
with their art and rarity gems, plus your summoner icons and ward skins — and
exports an Excel sheet and a CSV list alongside it.

## What changed since 1.10.1

- **There is a macOS package now.** PyInstaller cannot cross-compile, so the
  Mac binary is built on a macOS runner when a version tag is pushed, checked
  that it starts, and attached here alongside the Windows one.
- **macOS is tested, not assumed.** Finding the running client, the serif
  headings and opening the finished PDF were all confirmed on a Mac.

## Download

| File | For |
|---|---|
| `LoL-Skin-Catalog.zip (Windows)` | Windows — double-click the `.exe` |
| `LoL-Skin-Catalog.zip (macOS)` | macOS — the binary has no extension |

Both hold the same program plus a `no-exe` folder with the Python source, if
you would rather run it that way. Linux has no native League client, so the
client cannot be discovered automatically there; pass `--lockfile` and the rest
works.

## How to run it

1. Start League of Legends and log in. The lobby is enough — you do not have to play. Leave the client open.
2. Unzip the archive somewhere on your disk and run it **unzipped**, not from inside the ZIP.
3. Double-click the program.
4. Choose what you want, or press Enter for everything.
5. The first run downloads several hundred images and takes a few minutes. The PDF opens by itself when it finishes, and the window closes shortly after.

Results are named after your summoner and land next to the program. The PDF and
the spreadsheet are self-contained, so you can forward either one to a friend.

## What's in it

- Cover page with your profile icon, level, name, a rarity breakdown and a linked table of contents
- Champion roster: every champion, how many skins you own, and a link to their skins
- One card per skin, styled in the colours of its rarity gem
- Summoner icons and ward skins, newest acquisition first
- Excel sheet with embedded thumbnails, colour-coded rarities and an autofilter

## Before you click

Neither build is signed with a paid certificate, so both operating systems will
question it once.

- **Windows:** SmartScreen shows a blue panel. Choose **More info → Run anyway**.
- **macOS:** Gatekeeper refuses it. Right-click the program, choose **Open**, and confirm. Once only.

Some antivirus products also flag one-file PyInstaller builds as a false
positive; if yours removes it, the `no-exe` folder holds the same program as
Python scripts.

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
SHA256  3EF0D9139A1BD8AA2E1393684FE5FD50D53D7E569BF5BF51A38B3580C8C6688A  LoL-Skin-Catalog.zip (Windows)
```

The macOS package is built by the release workflow, so its checksum appears in
the run log rather than here.
