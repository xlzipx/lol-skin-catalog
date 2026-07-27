# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows
[Semantic Versioning](https://semver.org/).

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

[1.4.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.4.0
[1.3.1]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.3.1
[1.3.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.3.0
[1.2.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.2.0
[1.1.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.1.0
[1.0.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.0.0
