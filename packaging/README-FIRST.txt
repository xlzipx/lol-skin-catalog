===========================================================
  LoL SKIN CATALOG
===========================================================

Builds a PDF catalog of every League of Legends skin you own,
including splash art, rarity tiers and chroma counts.
Plus an Excel sheet and a CSV list.


HOW TO RUN
-----------------------------------------------------------

  1. Start League of Legends and log in.
     The lobby is enough - you do not have to play.
     Leave the client open.

  2. Unzip this archive somewhere on your disk.
     Run it unzipped, not from inside the ZIP.

  3. Double-click LoL-Skin-Catalog.exe

  4. It asks what you want. Press Enter for everything, or
     pick just the PDF, just Excel, or just CSV.

  5. Wait. The first run takes a few minutes while the
     artwork downloads. The PDF opens by itself when done.


WHAT YOU GET (next to the .exe)
-----------------------------------------------------------

  Files are named after your summoner, for example:

  NAME - LoL Collection.pdf   the catalog with pictures
  NAME - LoL Skins.xlsx       filterable table with thumbnails
  NAME - LoL Skins.csv        plain list, no images
  splashes\                   splash art as individual images

  The PDF and the spreadsheet are self-contained - pictures are
  inside the file, so you can forward either one.

  You only get what you asked for. Picking "PDF only" skips
  the splashes folder, and "CSV only" downloads no pictures
  at all and finishes in seconds.

  Pictures are kept in a ".thumbs" folder so a second run is
  quick. If you would rather not leave it behind, run the
  program from a command line with --clean.


WINDOWS MAY WARN YOU
-----------------------------------------------------------

  On first launch you may see a blue window saying
  "Windows protected your PC".

  That is because the program is not signed with a paid
  certificate, not because it is harmful. Click "More info"
  and then "Run anyway".

  If your antivirus deletes it outright, the "no-exe" folder
  holds the same program as Python scripts - see
  no-exe\README.md.


GOOD TO KNOW
-----------------------------------------------------------

  - It only reads data from the League client running on your
    own computer. It sends nothing anywhere, writes nothing to
    the game, and never asks for your password. Artwork is
    downloaded from the public Community Dragon mirror.

  - It finds the client by itself, wherever the game is
    installed. If it says it cannot connect, the client is
    almost certainly not running yet - wait until you are in
    the lobby and start it again.
    Last resort: find the file "lockfile" in your League of
    Legends folder and drag it onto the .exe.

  - Default champion skins are not counted, only real skins.

  - Source code and updates:
    https://github.com/xlzipx/lol-skin-catalog

===========================================================
  Not affiliated with Riot Games. League of Legends and all
  related artwork are property of Riot Games, Inc.
===========================================================
