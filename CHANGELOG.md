# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows
[Semantic Versioning](https://semver.org/).

## [1.11.1] — 2026-07-28

### Fixed

- The macOS package never got built. `build.py` staged the ZIP in a folder
  named after the program, and off Windows the binary has no extension, so the
  folder collided with the executable beside it. Windows never hit it because
  of the `.exe`. The staging folder has its own name now.
- The macOS workflow can be re-run by hand against a given tag, so a packaging
  failure no longer needs a fresh version to retry.

## [1.11.0] — 2026-07-28

### Added

- **A macOS package.** PyInstaller cannot cross-compile, so pushing a version
  tag now builds the Mac binary on a macOS runner, checks that it starts, and
  attaches it to that release. Windows keeps its own package as before.
- `build.py` names its output after the platform it ran on and keeps the
  execute bit on the binary inside the ZIP, which plain zipping drops.

### Changed

- macOS is documented as tested rather than assumed. Client discovery through
  the running process, the serif headings and opening the finished PDF were all
  confirmed on a Mac.

## [1.10.1] — 2026-07-28

### Fixed

- The roster page printed a page number that the last row of the champion
  table sat on top of, leaving half a digit peeking out. Front matter is
  unnumbered now, so numbering starts at 3 with the first page of skins.

## [1.10.0] — 2026-07-28

### Changed

- The window now closes by itself a few seconds after a successful export.
  A failed run still waits for Enter, because an error nobody gets to read is
  no better than a silent failure. `--keep-open` restores the old behaviour.

### Added

- macOS: the running client is found through `ps`, the same way it is found on
  Windows, instead of relying on the lockfile alone.
- Fonts are looked for on macOS and Linux too, not only in the Windows font
  folder, so headings keep their serif face off Windows.
- The finished PDF opens with `open` on macOS and `xdg-open` on Linux.

## [1.9.0] — 2026-07-28

Found while auditing what each export leaves on disk.

### Fixed

- `skins.json` and `profile.json` were written on every run regardless of the
  format chosen, even though nothing reads them back — leftovers from when the
  tool was two scripts. A CSV-only export now really does leave one CSV and
  nothing else.
- Excel rows were 162 points tall after skins went square, nearly twice their
  old depth. The thumbnail is now sized by height, so a row is the same depth
  whatever shape the art is.

### Added

- `data` is a format of its own: ask for it, or take `all`, and you get the raw
  client dump. Otherwise it is not written.
- `--clean` deletes the cached artwork once the export is finished, for anyone
  who wants only the document and no working files left behind.

## [1.8.0] — 2026-07-27

### Changed

- **Skin cards now show a square crop**, the way the client's own collection
  cards do. It comes from Riot's square tile art rather than a crop guessed out
  of the splash: the tile is framed on the champion by hand, ships at exactly
  the 380 px the card wants, and downloads at a third of the weight. Skins
  without a tile fall back to a centred crop of the splash.
- **Cards are smaller and pack five across and five down**, 25 skins to a page
  instead of 15. The skin section drops from 19 pages to 11, and the catalog
  as a whole from 26 to 18.
- **The rarity gem straddles the bottom edge of the art**, as it does in game,
  which frees the full card width for the skin name. Name and champion are
  centred under it.
- Embedded art is 380 px square, roughly 310 DPI at the new card size, stored
  at a quality that costs about 3/255 against Riot's original and a quarter of
  the bytes.
- A PDF-only export now fetches the small tile instead of the full splash, so
  it finishes considerably faster.

## [1.7.0] — 2026-07-27

### Changed

- Exports carry the summoner's name: `ZIPEEK - LoL Collection.pdf`,
  `ZIPEEK - LoL Skins.xlsx`, `ZIPEEK - LoL Skins.csv`. Two accounts exported
  into the same folder no longer overwrite one another.
- A name styled as spaced-out letters ("Z I P E E K") is collapsed for both the
  file name and the page headers, while a genuine two-word name keeps its
  space. Characters a file system rejects are stripped, and a missing name
  falls back to "Summoner".

## [1.6.0] — 2026-07-27

### Added

- **Skin cards are dressed in their rarity.** Instead of a thin coloured
  outline, each card now carries a wash rising out of its caption, an accent
  bar along the foot, corner brackets around the art, a scrim blending the art
  into the caption and a bright rule beneath the gem — all in the tier's
  colour. Cards with no tier get the same treatment in a muted steel.

### Changed

- Page numbers are flanked by short gold rules, the way a printed book sets
  them.
- The back link opens with a drawn upward arrow instead of a diamond, so it
  reads as a control rather than an ornament. The arrow is vector, not a
  glyph, so no font has to carry it.

## [1.5.1] — 2026-07-27

### Changed

- Page numbers moved from the top right corner to the foot of the page, plain
  and centred.
- The link back to the roster now sits in the bottom right corner and simply
  reads "back to roster".
- Page headers and section titles are centred.
- The backdrop is a plain vertical fade again; the light streaks are gone. It
  is drawn as vector bands rather than an embedded image, which also trims the
  executable back down.

## [1.5.0] — 2026-07-27

### Fixed

- **Half of every skin page was drawn off the paper.** A loop added in 1.4.0
  reused the variable holding the skin grid's column count, so the grid laid
  cards out in six columns instead of three and three of them fell past the
  right edge. Pages carried all fifteen cards but only nine were visible.
  Releases 1.4.0 and 1.4.1 are affected; regenerate your catalog with this
  version.

### Added

- A regression test that reads back where every image was placed and fails if
  any of it lands outside the page.

### Changed

- New page backdrop: a vertical fade from `#031f2c` down to `#03101a` with
  soft teal light streaks, echoing the client's own background. Card panels
  and roster stripes were retuned to match.

## [1.4.1] — 2026-07-27

### Changed

- The running page header names the section it belongs to — champion roster,
  skins collection, icons collection, wards collection — rather than reading
  "collection" on every page.

## [1.4.0] — 2026-07-27

### Added

- Every content page except the last carries a small link at the foot back to
  the champion roster, so a reader twenty pages deep can get back in one click.

### Changed

- Summoner icons and ward skins now run as one continuous grid ordered by
  acquisition date, newest first, instead of being split under a heading for
  every year. Each section opens with its own title and count. On a test
  account this took the catalog from 30 pages to 26.

### Fixed

- The contents plaques on the cover showed a bare figure, which read as a
  count next to the collection totals surrounding it. Each one now says
  "PAGE 3" so it cannot be mistaken for "3 skins".

## [1.3.1] — 2026-07-27

### Added

- Every champion in the roster links to the page where their skins begin.

### Fixed

- The contents plaques on the cover were wide enough to touch the ornamental
  frame. They are now a fixed width and centred, clear of the border.

## [1.3.0] — 2026-07-27

### Added

- **Summoner icons and ward skins** are now catalogued too, as their own
  sections after the skins. Both are grouped by the year you acquired them,
  newest first, the way the client's collection screen does it. Items with no
  purchase date land in a final group.
- **A table of contents on the cover.** Four plaques, styled after the client's
  collection tabs, name each section and the page it starts on. They are live
  links, and the PDF also gets a proper outline for the reader's sidebar.

### Changed

- The running page header reads "COLLECTION" rather than "OWNED SKINS", since
  the document now covers more than skins.
- Cover layout tightened to make room for the contents block.

## [1.2.0] — 2026-07-27

### Added

- `--formats` picks what to produce: any of `pdf`, `xlsx`, `csv`, `splashes`,
  or `all`. Run without it in a terminal and the program asks. Nothing you did
  not ask for is written, so a PDF-only export skips the `splashes/` folder and
  a CSV-only export downloads no artwork at all.

### Changed

- Splash art resolution raised: embedded art from 220 to 460 px (about 210 DPI
  on a catalog card), the `splashes/` folder from 480 to 720 px. The PDF grows
  from roughly 2.4 MB to 6.6 MB.
- Cached art is now checked against the current resolution, so upgrading
  refreshes older, smaller images instead of silently reusing them.

## [1.1.0] — 2026-07-27

### Changed

- Page two of the catalog is now a champion roster. The rarity gems were
  repeated there directly below the cover; they stay on the cover only, and the
  freed space went into a larger, more readable champion list.
- Cover statistics renamed so they cannot be confused: "Champions with skins"
  counts the champions present in the catalog, "Champions owned" counts every
  unlocked champion.
- Rarity gems follow the in-game side counts: Legendary four, Mythic five,
  Ultimate six. The Legendary gem is now as wide as it is tall.
- The last catalog page credits the project and links to the repository.

### Removed

- Czech translation and the `--lang` switch. The tool is English only, which
  removes the translation layer entirely.

### Added

- GitHub Actions workflow running an offline smoke test on Ubuntu and Windows
  against Python 3.9 and 3.12.
- `tests/smoke_test.py`, which builds every output from synthetic data and
  needs neither the game client nor network access.

## [1.0.0] — 2026-07-27

First public release.

### Added

- **PDF catalog** — cover page with your summoner profile, level badge and
  profile icon, a collection summary, then every skin in an alphabetical grid
  with splash art, rarity gem and chroma count.
- **Rarity gems** drawn as original faceted vectors, one silhouette per tier
  (Exalted, Transcendent, Ultimate, Mythic, Legendary, Epic, Rare), matching
  the colours the client uses.
- **Excel export** with embedded thumbnails, colour-coded rarity cells, an
  autofilter and a separate summary sheet.
- **CSV export** for anyone who just wants the list.
- **Splash art download** at 480 px, cached between runs.
- **Client auto-discovery** — reads the port and auth token from the running
  `LeagueClientUx.exe` process, so the install location does not matter.
  Falls back to the `lockfile`, an explicit `--lockfile` path, the
  `LOL_LOCKFILE` variable, or a scan of every drive.
- **Standalone Windows executable** built by `build.py`, packaged into a ZIP
  with instructions and a plain-Python fallback.

### Notes

- Default champion skins are excluded from the count; only real skins are
  listed.
- Rarity tiers come from Community Dragon because the client's inventory
  endpoint returns an empty rarity field.
- Chromas are counted only on real skins, matching the client's own tally.

[1.11.1]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.11.1
[1.11.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.11.0
[1.10.1]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.10.1
[1.10.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.10.0
[1.9.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.9.0
[1.8.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.8.0
[1.7.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.7.0
[1.6.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.6.0
[1.5.1]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.5.1
[1.5.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.5.0
[1.4.1]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.4.1
[1.4.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.4.0
[1.3.1]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.3.1
[1.3.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.3.0
[1.2.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.2.0
[1.1.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.1.0
[1.0.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.0.0
