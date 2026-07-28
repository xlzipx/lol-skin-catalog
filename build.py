"""
Builds the standalone executable for whichever platform it runs on, plus a
ready-to-send ZIP. PyInstaller cannot cross-compile, so a macOS build has to
be made on a Mac - the release workflow does that.

    pip install pyinstaller
    python build.py
"""

import os
import shutil
import stat
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")
WORK = os.path.join(HERE, "build")
NAME = "LoL-Skin-Catalog"

WINDOWS = os.name == "nt"
PLATFORM = "Windows" if WINDOWS else ("macOS" if sys.platform == "darwin" else "Linux")
BINARY = NAME + (".exe" if WINDOWS else "")
ARCHIVE = NAME + ("" if WINDOWS else f"-{PLATFORM}") + ".zip"

# what goes into the "no-exe" fallback folder inside the ZIP
SOURCE_FILES = ["main.py", "requirements.txt", "README.md", "README.cs.md", "LICENSE"]


def make_icon():
    """icon.png -> icon.ico. Only Windows needs it; macOS wants .icns."""
    if not WINDOWS:
        return None
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

    exe = os.path.join(DIST, BINARY)
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

    archive = os.path.join(DIST, ARCHIVE)
    if os.path.exists(archive):
        os.remove(archive)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(staging):
            for name in files:
                path = os.path.join(root, name)
                arcname = os.path.relpath(path, staging)
                if name == BINARY and not WINDOWS:
                    # zipfile drops the mode, and a binary without the execute
                    # bit is useless once unzipped
                    info = zipfile.ZipInfo.from_file(path, arcname)
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = (stat.S_IFREG | 0o755) << 16
                    with open(path, "rb") as f:
                        z.writestr(info, f.read())
                else:
                    z.write(path, arcname)

    print(f"Packaged {archive} ({os.path.getsize(archive) / 1048576:.1f} MB)")
    return archive


if __name__ == "__main__":
    make_zip(build_exe(make_icon()))
