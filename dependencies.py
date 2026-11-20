import subprocess
import sys
import shutil

def linux_deps():
    if shutil.which("apt"):    # Debian, Ubuntu, Mint, Pop!_OS
        cmd=["sudo","apt","install","-y","gir1.2-geoclue-2.0","python3-gi","python3-tk","python3-pil.imagetk"]
    elif shutil.which("dnf"):   # Fedora, RHEL, Nobara
        cmd=["sudo","dnf","install","-y","geoclue2","geoclue2-libs", "python3-gobject", "python3-tkinter","python3-pillow-tk"]
    elif shutil.which("pacman"):    # Arch, Manjaro, EndeavourOS
        cmd=["sudo","pacman","-S","--noconfirm", "geoclue", "python-gobject", "tk"]
    else:
        print("invalid package manager. Plese manually install: GeoClue2,PyGObject, Tkinter")
        return

    subprocess.run(cmd,check=True)

subprocess.run([sys.executable,"-m","pip","install","customtkinter","pillow","skyfield","timezonefinder","pandas","tkcalendar","ursina"],check=True)

if sys.platform == "win32":
    subprocess.run([sys.executable,"-m","pip","install","winrt-Windows.Devices.Geolocation"],check=True)

elif sys.platform.startswith("linux"):
    linux_deps()