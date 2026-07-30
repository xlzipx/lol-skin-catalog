# LoL Skin Catalog 1.13.0

Turns your League of Legends collection into a printable PDF catalog — skins
with their art and rarity gems, plus your summoner icons and ward skins — and
exports an Excel sheet and a CSV list alongside it.

## What changed since 1.12.2

- **Most skins were listed and counted twice.** Today's League of Legends
  Classic release ships the old models as a second set of champion entries, and
  the client hands both sets over as owned — so a Bloodstone Taric you own once
  turned up on two cards. Skins are now collapsed on champion and skin name, and
  champions are counted by name for the same reason.
- **The skins that exist only in Classic are kept.** `Classic Ahri`,
  `Classic 2012 Kayle` and the rest have names of their own, so nothing you own
  disappears. Summoner icons and ward skins were never affected.

Everyone running this while League of Legends Classic is installed wants this
release; nothing else changed.

## Download

| File | For |
|---|---|
| `LoL-Skin-Catalog.zip (Windows)` | Windows — double-click the `.exe`, then *More info* → *Run anyway* |
| `LoL-Skin-Catalog.zip (macOS)` | macOS — see below |

Both hold the same program plus a `no-exe` folder with the Python source, if
you would rather run it that way. Linux has no native League client, so the
client cannot be discovered automatically there; pass `--lockfile` and the rest
works.

## Running it on macOS

The first time, macOS refuses to open the program and says Apple could not
verify it. Nothing is wrong with the download: it is not notarised, which needs
a paid Apple developer account. Allow it once, either way:

- Try to open the program, dismiss the warning, then open **System Settings →
  Privacy & Security**, scroll down, and press **Open Anyway**.
- Or in Terminal, from the unzipped folder:
  `xattr -dr com.apple.quarantine ./LoL-Skin-Catalog`

Right-clicking and choosing Open does not work — Apple removed that shortcut —
and neither does a launcher script, because macOS blocks downloaded scripts the
same way.

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
SHA256  5F263E341EF75B62C9A5DB83468411DA4C140102626FD98889A95A82B5271E2C  LoL-Skin-Catalog.zip (Windows)
```

The macOS package is built by the release workflow, so its checksum appears in
the run log rather than here.
