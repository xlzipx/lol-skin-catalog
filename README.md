# LoL Skin Catalog

Exports the League of Legends collection **you own** into a printable PDF
catalog: every skin with its splash art, rarity tier and chroma count, followed
by your summoner icons and ward skins ordered by when you acquired them. Skins
also go out as an Excel sheet with thumbnails and a plain CSV list.

---

## What you get

Files carry your summoner name, so exports from two accounts sit side by side
without overwriting each other.

| File | Contents |
|---|---|
| `<name> - LoL Collection.pdf` | Cover with your profile and a linked table of contents, a champion roster, every skin, then your summoner icons and ward skins |
| `<name> - LoL Skins.xlsx` | Filterable table with embedded thumbnails and colour-coded rarities |
| `<name> - LoL Skins.csv` | Plain list, no images |
| `splashes/` | Splash art as individual JPEGs, 720 px wide |
| `skins.json`, `profile.json` | Raw data pulled from the client |

The PDF and the spreadsheet are self-contained — images and fonts live inside
the file, so you can send either one to a friend and it opens anywhere.

## Requirements

- Windows or macOS with League of Legends installed
- The League client **running and logged in** (the lobby is enough — you do not
  have to play)
- Python 3.9+ if you run from source; the prebuilt `.exe` needs nothing else

## Usage

### Prebuilt executable

Download the release, unzip it, start the League client, then double-click
`LoL-Skin-Catalog.exe`. Results are written next to the executable.

### From source

```bash
pip install -r requirements.txt
python main.py
```

Options:

| Flag | Meaning |
|---|---|
| `--formats LIST` | What to produce: any of `pdf`, `xlsx`, `csv`, `splashes`, or `all` |
| `--output DIR` | Write results somewhere else |
| `--lockfile PATH` | Point at the client manually (only needed for odd installs) |
| `--no-pause` | Do not wait for Enter when finished |
| `--no-open` | Do not open the PDF when finished |

Run without `--formats` in a terminal and it asks what you want: everything,
PDF only, Excel only, or CSV only. Anything not asked for is not produced —
choosing PDF only skips the `splashes/` folder entirely, and CSV only downloads
no artwork at all, finishing in seconds.

The first run downloads a few hundred images and takes a couple of minutes.
Art is cached in `splashes/` and `.thumbs/`, so later runs finish quickly. The
cache is checked against the current resolution, so upgrading the tool
refreshes older, smaller art by itself.

---

## How it works

This is the part worth reading if you are wondering whether the program does
anything shady. It does not. Here is the whole pipeline.

### 1. Finding the client

When the League client starts, it launches a local web server for its own user
interface and generates **a random port and a random password for that
session**. Both are written into a file called `lockfile` in the game folder,
and both are also passed as command-line arguments to the `LeagueClientUx.exe`
process.

This program reads them from the running process (and falls back to the
`lockfile`). That is the whole "authentication" — it is a local handshake that
the client hands out to itself, it changes every time the client restarts, and
it is worthless to anyone outside your machine.

### 2. Reading the inventory

Two read-only `GET` requests go to `https://127.0.0.1:<port>` — your own
computer, nowhere else:

| Endpoint | Used for |
|---|---|
| `/lol-summoner/v1/current-summoner` | Display name, tag, level, profile icon id |
| `/lol-champions/v1/inventories/{id}/champions` | Champions and their skins, with an `owned` flag |
| `/lol-inventory/v2/inventory/SUMMONER_ICON` | Owned summoner icons and when you got them |
| `/lol-inventory/v2/inventory/WARD_SKIN` | Owned ward skins and when you got them |

This interface is the LCU API — the same one the client's own screens are built
on, and the same one third-party apps such as OP.GG or Blitz use. It is not
officially documented by Riot, but it is a normal local API, not a hack.

Icons and wards are counted exactly the way the client counts them: every item
the inventory returns, including a handful of starter icons that carry no
purchase date and the free default ward.

### 3. Fetching the artwork

Splash art, icon and ward images, their names and the rarity tiers all come
from [Community Dragon](https://communitydragon.org), a public community mirror
of the game's asset files. These are ordinary HTTPS downloads of public images
— no account, no login, no tokens.

The inventory endpoints hand back nothing but item ids, so the names and
pictures for icons and wards are matched up from there, and rarity has to come
from there too because the client's own field for it comes back empty.

### 4. Building the documents

Images are resized with Pillow, the spreadsheet is written with openpyxl and
the PDF is drawn with ReportLab. All of it happens on your disk.

### What the program never does

- ❌ It does not ask for, store or transmit your Riot password — it never sees one
- ❌ It does not modify, patch, inject into or read the memory of the game
- ❌ It does not touch game files, configs or anything inside the install folder
- ❌ It does not send your data anywhere; the only outbound traffic is fetching
  public images from Community Dragon
- ❌ It does not affect gameplay, and it cannot change what you own
- ✅ Every request to the client is a `GET`. Nothing is ever written back.

The client API is read-only *as used here* — a tool like this can only look at
what the client already shows you on screen.

**A word of caution:** Riot does not officially document or support the LCU
API. Read-only tools like this one are widely used and have long been
tolerated, but that is tolerance, not a guarantee. Use it because it is
convenient, not because anyone promised it is blessed.

---

## Notes on the numbers

- **Base skins are excluded.** The client reports every champion's default look
  as an "owned skin", which is why its raw count is much higher than the number
  of skins you actually bought.
- **Rarity tiers** map to the client's gems: Exalted, Transcendent, Ultimate,
  Mythic, Legendary, Epic. `Rare` is the old 975 RP tier, which the client's own
  summary no longer displays — this catalog still lists it.
- **Chromas** are counted only on real skins, matching the client's own tally.
- **Icons and wards** are counted the way the client counts them, which includes
  a few starter icons carrying no purchase date and the free default ward. They
  are ordered newest acquisition first; anything undated sorts to the end.

## Project layout

```
main.py             entry point and CLI
build.py            builds the standalone .exe with PyInstaller
lolskins/
  client.py         LCU discovery and inventory reading
  assets.py         Community Dragon downloads
  pdf.py            the PDF catalog
  sheet.py          XLSX and CSV
  theme.py          colours, rarity gems, fonts
  paths.py          where files are written
tests/
  smoke_test.py     offline build of every output, run by CI
.github/workflows/
  ci.yml            Ubuntu and Windows, Python 3.9 and 3.12
```

## Building the executable

```bash
pip install pyinstaller
python build.py
```

Produces `dist/LoL-Skin-Catalog.exe` plus a ready-to-send ZIP with instructions
and a plain-Python fallback.

Because the binary is unsigned, Windows SmartScreen will warn about it on first
launch ("More info" → "Run anyway"), and some antivirus products flag one-file
PyInstaller builds as a false positive. Running from source avoids both.

## License

MIT — see [LICENSE](LICENSE).

Not affiliated with or endorsed by Riot Games. League of Legends and all
related artwork are property of Riot Games, Inc.
