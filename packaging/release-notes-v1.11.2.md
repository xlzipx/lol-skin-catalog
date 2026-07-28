# LoL Skin Catalog 1.11.2

Turns your League of Legends collection into a printable PDF catalog — skins
with their art and rarity gems, plus your summoner icons and ward skins — and
exports an Excel sheet and a CSV list alongside it.

## What changed since 1.11.1

macOS refuses to open the program the first time, saying Apple could not verify
it. Nothing is wrong with the download: the binary is not notarised, which needs
a paid Apple developer account. This release makes that easier to get past.

- **A launcher for macOS.** The package now carries
  `Start on macOS.command`. Double-click it and Terminal runs the program.
  Finder does not hold scripts to notarisation the way it holds a compiled
  binary, so the launcher gets through; it clears the quarantine flag macOS
  puts on downloaded files and starts the program. It does by itself what you
  would otherwise type into Terminal.
- **Corrected instructions.** The old advice was to right-click and choose
  Open, which recent macOS versions no longer accept. The manual route is now
  System Settings → Privacy & Security → **Open Anyway**.

Signing the binary would not help, incidentally: PyInstaller already ad-hoc
signs it. The block is about notarisation, not a missing signature.

## Download

| File | For |
|---|---|
| `LoL-Skin-Catalog.zip (Windows)` | Windows — double-click the `.exe` |
| `LoL-Skin-Catalog.zip (macOS)` | macOS — double-click `Start on macOS.command` |

Both hold the same program plus a `no-exe` folder with the Python source, if
you would rather run it that way. Linux has no native League client, so the
client cannot be discovered automatically there; pass `--lockfile` and the rest
works.

## How to run it

1. Start League of Legends and log in. The lobby is enough — you do not have to play. Leave the client open.
2. Unzip the archive somewhere on your disk and run it **unzipped**, not from inside the ZIP.
3. Start the program.
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

Neither build is signed with a paid certificate, so both systems question it
once. On Windows, SmartScreen shows a blue panel: choose **More info → Run
anyway**. On macOS, use the launcher described above.

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
SHA256  8ADC582E8CAE7E75D57A1A7995738C25E2225E652D7328DE9450E0AA36F5A165  LoL-Skin-Catalog.zip (Windows)
```

The macOS package is built by the release workflow, so its checksum appears in
the run log rather than here.
