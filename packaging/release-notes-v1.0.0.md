# LoL Skin Catalog 1.0.0

Turns the skins you own in League of Legends into a printable PDF catalog —
with splash art, rarity gems and chroma counts — plus an Excel sheet and a CSV
list. First public release.

## Download

| File | Size | What it is |
|---|---|---|
| `LoL-Skin-Catalog.zip` | 37.7 MB | Everything you need: the executable, bilingual instructions and a plain-Python fallback |

Source code is below if you would rather run it with Python.

## How to run it

1. Start League of Legends and log in. The lobby is enough — you do not have to play. Leave the client open.
2. Unzip the archive somewhere on your disk and run it **unzipped**, not from inside the ZIP.
3. Double-click `LoL-Skin-Catalog.exe`.
4. The first run downloads a few hundred images and takes a couple of minutes. The PDF opens by itself when it finishes.

Results land next to the executable: `Skins.pdf`, `Skins.xlsx`, `skins.csv` and
a `splashes/` folder. The PDF and the spreadsheet are self-contained, so you can
forward either one to a friend.

## What's in it

- Cover page with your profile icon, level, name and a rarity breakdown
- Collection summary: counts per rarity tier and per champion, in striped tables
- One card per skin — splash art framed in its rarity colour, name, champion and chroma count
- Excel sheet with embedded thumbnails, colour-coded rarities and an autofilter
- English and Czech output, picked from your system language (`--lang en` or `--lang cs` to force one)

## Before you click

Windows SmartScreen will warn you on first launch, because the executable is not
signed with a paid certificate. Choose **More info → Run anyway**. Some antivirus
products also flag one-file PyInstaller builds as a false positive; if yours
removes it, the `no-exe` folder in the ZIP holds the same program as Python
scripts.

## Is it safe?

It reads data from the League client running on your own machine and sends
nothing anywhere. Two `GET` requests go to `127.0.0.1`, the artwork comes from
the public Community Dragon mirror, and nothing is ever written back to the
game. It never sees your Riot password. The full walkthrough is in the
[README](https://github.com/xlzipx/lol-skin-catalog#how-it-works).

Riot does not officially document the LCU API this relies on. Read-only tools
like this are widely used and long tolerated, but that is tolerance, not a
guarantee.

## Checksums

```
SHA256  08F2C8821CEAD87E5D52240D7CA0B64889F2C4D96C604C36F1FB54F4043F141E  LoL-Skin-Catalog.zip
SHA256  A38EEC3E2ED1E6FD1E4A643F6D6614B0F629855AC3D5BE16FC8A422693EC3470  LoL-Skin-Catalog.exe
```

---

# LoL Skin Catalog 1.0.0 (česky)

Udělá z tvých skinů v League of Legends PDF katalog k vytištění — se splash
arty, raritními drahokamy a počty chromat — a k tomu Excel a CSV. První veřejné
vydání.

## Jak to spustit

1. Spusť League of Legends a přihlas se. Stačí lobby, hrát nemusíš. Klienta nech otevřeného.
2. Rozbal archiv na disk a spouštěj ho **rozbalený**, ne přímo ze ZIPu.
3. Dvojklikni na `LoL-Skin-Catalog.exe`.
4. První běh stáhne několik set obrázků a trvá pár minut. Až doběhne, PDF se samo otevře.

Výstupy se uloží vedle spustitelného souboru: `Skins.pdf`, `Skins.xlsx`,
`skins.csv` a složka `splashes/`. PDF i tabulka jsou soběstačné, takže je můžeš
komukoli přeposlat.

## Co v tom je

- Titulní strana s profilovou ikonkou, úrovní, jménem a rozpadem podle rarity
- Souhrn sbírky: počty podle rarity a podle šampiona, v proužkovaných tabulkách
- Karta pro každý skin — splash art v barvě rarity, název, šampion a počet chromat
- Excel s vloženými náhledy, barevnými raritami a filtrem
- Výstup česky nebo anglicky podle jazyka systému (`--lang cs`, `--lang en`)

## Než klikneš

Windows SmartScreen při prvním spuštění zaprotestuje, protože program není
podepsaný placeným certifikátem. Klikni na **Další informace → Přesto spustit**.
Některé antiviry navíc hlásí jednosouborové PyInstaller buildy jako falešný
poplach; kdyby ti to smazal, ve složce `no-exe` je stejný program jako Python
skripty.

## Je to bezpečné?

Čte data z League klienta běžícího u tebe v počítači a nikam nic neodesílá.
Odejdou dva dotazy `GET` na `127.0.0.1`, grafika se stahuje z veřejného
Community Dragonu a do hry se nikdy nic nezapisuje. Tvoje heslo k Riot účtu
program nikdy nevidí. Celý postup je popsaný
v [READMEčku](https://github.com/xlzipx/lol-skin-catalog/blob/main/README.cs.md#jak-to-funguje).

Riot LCU API, na kterém to stojí, oficiálně nedokumentuje. Nástroje jen pro
čtení jsou hojně rozšířené a dlouhodobě tolerované, ale je to tolerance, ne
záruka.
