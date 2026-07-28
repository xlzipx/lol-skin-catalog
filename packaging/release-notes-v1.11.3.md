# LoL Skin Catalog 1.11.3

Turns your League of Legends collection into a printable PDF catalog — skins
with their art and rarity gems, plus your summoner icons and ward skins — and
exports an Excel sheet and a CSV list alongside it.

## What changed since 1.11.2

- **The macOS launcher is gone.** 1.11.2 shipped a `Start on macOS.command` on
  the assumption that macOS treats downloaded scripts more leniently than
  compiled binaries. Testing on a Mac showed it does not — the script was
  refused exactly like the program. The package is back to just the program.
- **The macOS instructions say what actually works**, in the README and in the
  note inside the package, and name the dead ends so nobody retries them.

## Running it on macOS

The first time, macOS refuses to open the program and says Apple could not
verify it. Nothing is wrong with the download: it is not notarised, which needs
a paid Apple developer account, and macOS blocks anything unnotarised that came
from the internet. Allow it once, either way:

- Try to open the program, dismiss the warning, then open **System Settings →
  Privacy & Security**, scroll down, and press **Open Anyway** next to the
  blocked program.
- Or in Terminal, from the unzipped folder:
  `xattr -dr com.apple.quarantine ./LoL-Skin-Catalog`

After that it starts normally and never asks again.

Two things do **not** work: right-clicking and choosing Open, which Apple
removed, and a launcher script, which macOS blocks the same way. Signing does
not help either — PyInstaller already ad-hoc signs the binary; the block is
about notarisation, not a missing signature.

## Download

| File | For |
|---|---|
| `LoL-Skin-Catalog.zip (Windows)` | Windows — double-click the `.exe`, then *More info* → *Run anyway* |
| `LoL-Skin-Catalog.zip (macOS)` | macOS — see above |

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
SHA256  6BFF027580CFC3AD9985A0D31326C417CEE5E9A3C9B5AA948D3468710E6ED7B5  LoL-Skin-Catalog.zip (Windows)
```

The macOS package is built by the release workflow, so its checksum appears in
the run log rather than here.
