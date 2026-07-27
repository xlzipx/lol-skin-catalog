"""
Builds the standalone Windows executable and a ready-to-send ZIP.

    pip install pyinstaller
    python build.py
"""

import os
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")
WORK = os.path.join(HERE, "build")
NAME = "LoL-Skin-Catalog"

# what goes into the "no-exe" fallback folder inside the ZIP
SOURCE_FILES = ["main.py", "requirements.txt", "README.md", "README.cs.md", "LICENSE"]


def make_icon():
    """icon.png -> icon.ico (PyInstaller needs .ico on Windows)."""
    png = os.path.join(HERE, "icon.png")
    ico = os.path.join(HERE, "icon.ico")
    if not os.path.exists(png):
        return None
    if os.path.exists(ico) and os.path.getmtime(ico) >= os.path.getmtime(png):
        return ico
    from PIL import Image

    img = Image.open(png).convert("RGBA")
    side = max(img.size)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(img, ((side - img.width) // 2, (side - img.height) // 2))
    canvas.save(ico, sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print("icon.ico written")
    return ico


def build_exe(icon):
    command = [
        sys.executable, "-m", "PyInstaller",
        "--onefile", "--console", "--noconfirm",
        "--name", NAME,
        "--distpath", DIST,
        "--workpath", WORK,
        "--specpath", WORK,
        "--paths", HERE,
    ]
    if icon:
        command += ["--icon", icon]
    command.append(os.path.join(HERE, "main.py"))

    print("Running PyInstaller…")
    result = subprocess.run(command)
    if result.returncode != 0:
        sys.exit("PyInstaller failed.")

    exe = os.path.join(DIST, NAME + ".exe")
    print(f"Built {exe} ({os.path.getsize(exe) / 1048576:.1f} MB)")
    return exe


def make_zip(exe):
    staging = os.path.join(DIST, NAME)
    shutil.rmtree(staging, ignore_errors=True)
    os.makedirs(os.path.join(staging, "no-exe", "lolskins"), exist_ok=True)

    shutil.copy(exe, staging)
    shutil.copy(os.path.join(HERE, "packaging", "README-FIRST.txt"), staging)
    for name in SOURCE_FILES:
        source = os.path.join(HERE, name)
        if os.path.exists(source):
            shutil.copy(source, os.path.join(staging, "no-exe"))
    for name in os.listdir(os.path.join(HERE, "lolskins")):
        if name.endswith(".py"):
            shutil.copy(os.path.join(HERE, "lolskins", name),
                        os.path.join(staging, "no-exe", "lolskins"))

    archive = os.path.join(DIST, NAME + ".zip")
    if os.path.exists(archive):
        os.remove(archive)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(staging):
            for name in files:
                path = os.path.join(root, name)
                z.write(path, os.path.relpath(path, staging))

    print(f"Packaged {archive} ({os.path.getsize(archive) / 1048576:.1f} MB)")
    return archive


if __name__ == "__main__":
    make_zip(build_exe(make_icon()))
