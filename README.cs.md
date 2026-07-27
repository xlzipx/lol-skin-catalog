# LoL Skin Catalog

Vyexportuje všechny skiny v League of Legends, které **vlastníš**, do PDF
katalogu k vytištění, Excelu s náhledy a prostého CSV — seřazené podle abecedy,
se splash arty, raritami a počty chromat.

🇬🇧 [English version of this file](README.md)

---

## Co dostaneš

| Soubor | Obsah |
|---|---|
| `Skins.pdf` | Titulní strana s profilem, souhrn sbírky a mřížka všech skinů |
| `Skins.xlsx` | Filtrovatelná tabulka s vloženými náhledy a barevnými raritami |
| `skins.csv` | Prostý seznam bez obrázků |
| `splashes/` | Splash arty jako jednotlivé JPEG, šířka 480 px |
| `skins.json`, `profile.json` | Surová data načtená z klienta |

`Skins.pdf` a `Skins.xlsx` jsou soběstačné — obrázky i fonty jsou uvnitř
souboru, takže je můžeš komukoli přeposlat a otevřou se kdekoli.

## Co je potřeba

- Windows nebo macOS s nainstalovaným League of Legends
- **Spuštěný a přihlášený** League klient (stačí lobby, hrát nemusíš)
- Python 3.9+ při spouštění ze zdrojáků; předpřipravené `.exe` nepotřebuje nic

## Použití

### Hotové .exe

Stáhni release, rozbal, spusť League klienta a dvojklikni na
`LoL-Skin-Catalog.exe`. Výstupy se uloží vedle spustitelného souboru.

### Ze zdrojáků

```bash
pip install -r requirements.txt
python main.py
```

Přepínače:

| Přepínač | Význam |
|---|---|
| `--lang en\|cs` | Jazyk výstupu. Výchozí je jazyk systému, jinak angličtina |
| `--output SLOŽKA` | Zapsat výsledky jinam |
| `--lockfile CESTA` | Ručně ukázat na klienta (jen u netypických instalací) |
| `--no-pause` | Nečekat na Enter po dokončení |
| `--no-open` | Neotevírat PDF po dokončení |

První běh stáhne několik set obrázků a trvá pár minut. Grafika se ukládá do
`splashes/` a `.thumbs/`, takže další běhy jsou otázkou vteřin.

---

## Jak to funguje

Tohle je ta část, kterou má smysl si přečíst, pokud tě zajímá, jestli program
nedělá něco nekalého. Nedělá. Tady je celý postup.

### 1. Nalezení klienta

Když se League klient spustí, nastartuje si lokální webový server pro vlastní
uživatelské rozhraní a vygeneruje **náhodný port a náhodné heslo pro danou
relaci**. Obojí zapíše do souboru `lockfile` ve složce s hrou a obojí zároveň
předá jako argumenty procesu `LeagueClientUx.exe`.

Program si je přečte z běžícího procesu (a když to nevyjde, sáhne po
`lockfile`). To je celé „přihlašování" — je to lokální handshake, který si
klient vydává sám sobě, mění se při každém restartu a komukoli mimo tvůj počítač
je k ničemu.

### 2. Přečtení inventáře

Odejdou dva dotazy typu `GET` na `https://127.0.0.1:<port>` — tedy na tvůj
vlastní počítač, nikam jinam:

| Endpoint | K čemu slouží |
|---|---|
| `/lol-summoner/v1/current-summoner` | Jméno, tag, úroveň, ID profilové ikonky |
| `/lol-champions/v1/inventories/{id}/champions` | Šampioni a jejich skiny s příznakem `owned` |

Tomuhle rozhraní se říká LCU API — je to totéž, na kterém stojí obrazovky
samotného klienta, a totéž, které používají aplikace jako OP.GG nebo Blitz.
Riot ho oficiálně nedokumentuje, ale je to běžné lokální API, ne hack.

### 3. Stažení grafiky

Splash arty a rarity pocházejí z [Community Dragonu](https://communitydragon.org),
veřejného komunitního zrcadla herních assetů. Jsou to obyčejná HTTPS stažení
veřejných obrázků — žádný účet, žádné přihlášení, žádné tokeny.

Rarita musí přijít odtud, protože inventářový endpoint klienta vrací pole
s raritou prázdné.

### 4. Sestavení dokumentů

Obrázky se zmenšují přes Pillow, tabulka vzniká v openpyxl a PDF se kreslí
v ReportLabu. Všechno se odehrává na tvém disku.

### Co program nikdy nedělá

- ❌ Nechce, neukládá ani neodesílá tvoje heslo k Riot účtu — nikdy ho nevidí
- ❌ Neupravuje hru, nepatchuje ji, nic do ní neinjektuje ani nečte její paměť
- ❌ Nesahá na herní soubory, konfiguraci ani na nic ve složce s instalací
- ❌ Neodesílá tvoje data nikam ven; jediný odchozí provoz je stahování
  veřejných obrázků z Community Dragonu
- ❌ Neovlivňuje hraní a nemůže změnit, co vlastníš
- ✅ Každý dotaz na klienta je `GET`. Nikdy se nic nezapisuje zpět.

Klientské API je tak, jak se tu používá, jen pro čtení — nástroj tohoto typu
se může dívat pouze na to, co ti klient stejně ukazuje na obrazovce.

**Jedno upozornění:** Riot LCU API oficiálně nedokumentuje ani nepodporuje.
Nástroje jen pro čtení, jako je tenhle, jsou hojně rozšířené a dlouhodobě
tolerované, ale je to tolerance, ne záruka. Používej to pro pohodlí, ne proto,
že by to někdo posvětil.

---

## Poznámky k číslům

- **Základní vzhledy se nepočítají.** Klient hlásí výchozí vzhled každého
  šampiona jako „vlastněný skin", proto je jeho hrubý počet mnohem vyšší než
  počet skinů, které sis skutečně pořídil.
- **Rarity** odpovídají drahokamům v klientovi: Exalted, Transcendent, Ultimate,
  Mythic, Legendary, Epic. `Rare` je starý tier za 975 RP, který už souhrn
  v klientovi nezobrazuje — tenhle katalog ho uvádí.
- **Chromy** se počítají jen u skutečných skinů, stejně jako je počítá klient.

## Struktura projektu

```
main.py             vstupní bod a CLI
build.py            sestavení samostatného .exe přes PyInstaller
lolskins/
  client.py         nalezení klienta a čtení inventáře
  assets.py         stahování z Community Dragonu
  pdf.py            PDF katalog
  sheet.py          XLSX a CSV
  theme.py          barvy, raritní drahokamy, fonty
  i18n.py           anglické a české texty
  paths.py          kam se zapisují soubory
```

## Sestavení spustitelného souboru

```bash
pip install pyinstaller
python build.py
```

Vyrobí `dist/LoL-Skin-Catalog.exe` a k tomu ZIP s dvojjazyčným návodem,
připravený k odeslání.

Protože binárka není podepsaná, Windows SmartScreen při prvním spuštění
zaprotestuje („Další informace" → „Přesto spustit") a některé antiviry hlásí
jednosouborové PyInstaller buildy jako falešný poplach. Spuštění ze zdrojáků
se tomu vyhne.

## Licence

MIT — viz [LICENSE](LICENSE).

Není nijak spojeno s Riot Games ani jimi schváleno. League of Legends a veškerá
související grafika jsou majetkem Riot Games, Inc.
