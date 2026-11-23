"""Cek apakah library untuk study group IMV sudah terpasang.

Jalankan dari root repo:
    python setup/check_environment.py
"""
import importlib
import sys

REQUIRED = ["numpy", "cv2", "matplotlib", "skimage", "mediapipe"]
OPTIONAL = ["numba"]


def check(name):
    try:
        mod = importlib.import_module(name)
    except ImportError:
        return None
    return getattr(mod, "__version__", "terpasang")


def main():
    print(f"Python {sys.version.split()[0]}")
    if not (3, 9) <= sys.version_info[:2] <= (3, 12):
        print("[PERINGATAN] mediapipe==0.10.21 butuh Python 3.9 - 3.12")

    missing = []
    for name in REQUIRED + OPTIONAL:
        version = check(name)
        tag = "opsional" if name in OPTIONAL else "wajib"
        if version is None:
            print(f"[KURANG] {name} ({tag})")
            if name in REQUIRED:
                missing.append(name)
        else:
            print(f"[OK]     {name} {version}")

    if missing:
        print("\nPasang dulu: pip install -r requirements.txt")
        sys.exit(1)
    print("\nEnvironment siap.")


if __name__ == "__main__":
    main()
