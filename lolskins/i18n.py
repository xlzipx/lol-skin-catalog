"""Bilingual strings (English primary, Czech secondary)."""

import locale
import os
import warnings

LANGUAGES = ("en", "cs")
DEFAULT = "en"

_current = DEFAULT

STRINGS = {
    # ---------------------------------------------------------- console ----
    "app_title": {
        "en": "LEAGUE OF LEGENDS SKIN CATALOG",
        "cs": "KATALOG SKINŮ V LEAGUE OF LEGENDS",
    },
    "output_folder": {
        "en": "Output will be saved to:",
        "cs": "Výstupy se uloží do složky:",
    },
    "step_read": {
        "en": "[1/2] Reading data from the running client…",
        "cs": "[1/2] Načítám data z běžícího klienta…",
    },
    "step_build": {
        "en": "[2/2] Downloading splash art and building the catalog…",
        "cs": "[2/2] Stahuji splash arty a skládám katalog…",
    },
    "step_build_note": {
        "en": "      (the first run takes a few minutes, then images are cached)",
        "cs": "      (poprvé to trvá pár minut, potom už jsou obrázky uložené)",
    },
    "done": {"en": "DONE", "cs": "HOTOVO"},
    "created": {"en": "Created:", "cs": "Vytvořeno:"},
    "splash_folder_note": {
        "en": "  splashes/      folder with splash art",
        "cs": "  splashes/      složka se splash arty",
    },
    "press_enter": {
        "en": "\nPress Enter to close…",
        "cs": "\nStiskni Enter pro zavření…",
    },
    "client_found_port": {
        "en": "Client found via its running process (port {port})",
        "cs": "Klient nalezen podle běžícího procesu (port {port})",
    },
    "lockfile_used": {"en": "Lockfile: {path}", "cs": "Lockfile: {path}"},
    "logged_in_as": {"en": "Logged in as: {name}", "cs": "Přihlášen jako: {name}"},
    "owned_incl_base": {
        "en": "Owned skins (including base): {count}",
        "cs": "Vlastněných skinů (včetně základních): {count}",
    },
    "owned_real": {
        "en": "Real skins (base excluded): {count}",
        "cs": "Skutečných skinů (bez základních): {count}",
    },
    "saved_to": {"en": "Saved to {name}", "cs": "Uloženo do {name}"},
    "skins_to_export": {
        "en": "Skins to export: {count}",
        "cs": "Skinů k exportu: {count}",
    },
    "rarity_line": {"en": "Rarities: {data}", "cs": "Rarity: {data}"},
    "downloading_splashes": {
        "en": "Downloading splash art…",
        "cs": "Stahuji splash arty…",
    },
    "download_progress": {
        "en": "  downloaded {done}/{total}",
        "cs": "  staženo {done}/{total}",
    },
    "writing_csv": {"en": "Writing CSV…", "cs": "Píšu CSV…"},
    "writing_xlsx": {"en": "Writing XLSX…", "cs": "Píšu XLSX…"},
    "writing_pdf": {"en": "Writing PDF…", "cs": "Píšu PDF…"},
    "rarity_fetch_failed": {
        "en": "Could not download rarity data: {error}",
        "cs": "Rarity se nepodařilo stáhnout: {error}",
    },
    "profile_icon_failed": {
        "en": "Could not download the profile icon: {error}",
        "cs": "Profilovku se nepodařilo stáhnout: {error}",
    },
    "read_failed": {
        "en": "Could not read data from the client: {error}",
        "cs": "Nepodařilo se přečíst data z klienta: {error}",
    },
    "check_client": {
        "en": "Make sure the League client is running and you are logged in.",
        "cs": "Zkontroluj, že League klient běží a jsi přihlášený.",
    },
    "export_failed": {"en": "Export failed: {error}", "cs": "Export selhal: {error}"},
    "no_client_exe": {
        "en": (
            "Could not connect to the League client.\n\n"
            "  1) Start League of Legends and log in (the lobby is enough,\n"
            "     you do not have to play), then run this program again.\n\n"
            "  2) If the client is running and it still fails, find the file\n"
            "     'lockfile' in your League of Legends folder and drag it\n"
            "     onto this .exe."
        ),
        "cs": (
            "Nepodařilo se spojit s League klientem.\n\n"
            "  1) Spusť League of Legends a přihlas se (stačí lobby, hrát\n"
            "     nemusíš) a pak tenhle program spusť znovu.\n\n"
            "  2) Když už klient běží a přesto to nejde, najdi ve složce\n"
            "     s hrou soubor 'lockfile' a přetáhni ho myší na tohle .exe."
        ),
    },
    "no_client_script": {
        "en": (
            "Could not connect to the League client.\n\n"
            "  1) The League client must be running (logged in is enough).\n"
            "  2) For a non-standard install, pass the path manually:\n"
            '     python main.py --lockfile "path/to/League of Legends/lockfile"'
        ),
        "cs": (
            "Nepodařilo se spojit s League klientem.\n\n"
            "  1) Musí běžet League klient (stačí přihlášený, hrát nemusíš).\n"
            "  2) Při netypické instalaci předej cestu ručně:\n"
            '     python main.py --lockfile "cesta/k/League of Legends/lockfile"'
        ),
    },
    # -------------------------------------------------------------- PDF ----
    "pdf_game": {"en": "LEAGUE OF LEGENDS", "cs": "LEAGUE OF LEGENDS"},
    "pdf_subtitle": {
        "en": "OWNED SKINS COLLECTION",
        "cs": "SBÍRKA VLASTNĚNÝCH SKINŮ",
    },
    "pdf_total_1": {"en": "TOTAL SKINS", "cs": "SKINŮ"},
    "pdf_total_2": {"en": "OWNED", "cs": "CELKEM"},
    "pdf_champions": {"en": "CHAMPIONS", "cs": "ŠAMPIONŮ"},
    "pdf_chromas": {"en": "CHROMAS", "cs": "CHROMAS"},
    "pdf_champs_owned": {"en": "CHAMPS OWNED", "cs": "ŠAMPIONŮ VLASTNĚNO"},
    "pdf_generated": {"en": "Generated {date}", "cs": "Vygenerováno {date}"},
    "pdf_header": {
        "en": "{name}'S OWNED SKINS",
        "cs": "SKINY HRÁČE {name}",
    },
    "pdf_summary": {"en": "COLLECTION SUMMARY", "cs": "SOUHRN SBÍRKY"},
    "pdf_by_rarity": {"en": "BY RARITY", "cs": "PODLE RARITY"},
    "pdf_by_champion": {
        "en": "BY CHAMPION ({count})",
        "cs": "PODLE ŠAMPIONA ({count})",
    },
    "pdf_no_tier": {"en": "No tier", "cs": "Bez tieru"},
    "pdf_footer": {
        "en": "Generated with LoL Skin Catalog — a free, open-source tool "
              "for exporting the skins you own.",
        "cs": "Vygenerováno nástrojem LoL Skin Catalog — volně dostupným "
              "open-source programem pro export vlastněných skinů.",
    },
    # ------------------------------------------------------ spreadsheet ----
    "col_index": {"en": "#", "cs": "#"},
    "col_champion": {"en": "Champion", "cs": "Šampion"},
    "col_skin": {"en": "Skin", "cs": "Skin"},
    "col_rarity": {"en": "Rarity", "cs": "Rarita"},
    "col_chromas": {"en": "Chromas", "cs": "Chromas"},
    "col_skin_id": {"en": "Skin ID", "cs": "ID skinu"},
    "col_splash": {"en": "Splash art", "cs": "Splash art"},
    "col_splash_file": {"en": "Splash file", "cs": "Soubor splashe"},
    "col_count": {"en": "Count", "cs": "Počet"},
    "sheet_skins": {"en": "Skins", "cs": "Skiny"},
    "sheet_summary": {"en": "Summary", "cs": "Souhrn"},
    "xls_overview": {"en": "Overview", "cs": "Přehled"},
    "xls_player": {"en": "Player", "cs": "Hráč"},
    "xls_level": {"en": "Level", "cs": "Úroveň"},
    "xls_skins_total": {"en": "Skins total", "cs": "Skinů celkem"},
    "xls_champs_with_skin": {
        "en": "Champions with a skin",
        "cs": "Šampionů se skinem",
    },
    "xls_champs_owned": {"en": "Champions owned", "cs": "Vlastněných šampionů"},
    "xls_chromas_owned": {"en": "Chromas owned", "cs": "Chromas celkem"},
    "xls_export_date": {"en": "Export date", "cs": "Datum exportu"},
    "xls_no_tier": {"en": "No tier", "cs": "Bez tieru"},
}


def _locale_candidates():
    """Every hint about the user's language, best source first."""
    found = []

    # 1) the language Windows itself is displayed in
    if os.name == "nt":
        try:
            import ctypes

            lcid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            found.append(locale.windows_locale.get(lcid, ""))
        except Exception:
            pass

    # 2) POSIX-style environment (Linux, macOS, and anyone overriding it)
    for var in ("LC_ALL", "LC_MESSAGES", "LANG", "LANGUAGE"):
        found.append(os.environ.get(var, ""))

    # 3) whatever locale this process is set to
    try:
        found.append(locale.getlocale()[0] or "")
    except Exception:
        pass

    # 4) removed in Python 3.15, kept as a last resort for older runtimes
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            found.append(locale.getdefaultlocale()[0] or "")
    except Exception:
        pass

    return [x for x in found if x]


def detect_language():
    """--lang > LOLSKINS_LANG > OS language > English.

    Windows reports the locale in several shapes ('cs_CZ', 'cs-CZ',
    'Czech_Czechia'), so all of them are recognised.
    """
    from_env = (os.environ.get("LOLSKINS_LANG") or "").strip().lower()
    if from_env in LANGUAGES:
        return from_env

    for candidate in _locale_candidates():
        code = candidate.lower()
        if code.startswith(("cs", "cz")) or "czech" in code:
            return "cs"
        return DEFAULT  # the best available hint says something else
    return DEFAULT


def set_language(lang):
    global _current
    _current = lang if lang in LANGUAGES else DEFAULT
    return _current


def get_language():
    return _current


def t(key, **kwargs):
    zaznam = STRINGS.get(key)
    if not zaznam:
        return key
    text = zaznam.get(_current) or zaznam.get(DEFAULT) or key
    return text.format(**kwargs) if kwargs else text


def chromas(count):
    """'1 chroma' / '6 chromas'.

    Czech keeps the same wording on purpose: players say "chroma" and
    "chromas", and the declined Czech plural ("chromat") reads badly.
    """
    return f"{count} chroma" if count == 1 else f"{count} chromas"
