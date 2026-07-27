# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows
[Semantic Versioning](https://semver.org/).

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
- **Bilingual output** in English and Czech, chosen from the system locale and
  overridable with `--lang`. Czech gets correct plural forms for chromas.
- **Standalone Windows executable** built by `build.py`, packaged into a ZIP
  with bilingual instructions and a plain-Python fallback.

### Notes

- Default champion skins are excluded from the count; only real skins are
  listed.
- Rarity tiers come from Community Dragon because the client's inventory
  endpoint returns an empty rarity field.
- Chromas are counted only on real skins, matching the client's own tally.

[1.0.0]: https://github.com/xlzipx/lol-skin-catalog/releases/tag/v1.0.0
