# IMV-StudyGroup
```
Study-Group-IMV-2026/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── docs/
│   ├── curriculum.md
│   ├── installation-guide.md
│   └── troubleshooting.md
│
├── setup/
│   ├── check_environment.py
│   └── setup_guide.md
│
├── modules/
│   ├── module-01-opencv-fundamentals/
│   │   ├── README.md
│   │   ├── materials/
│   │   ├── notebooks/
│   │   ├── src/
│   │   ├── exercises/
│   │   └── assets/
│   │
│   ├── module-02-face-detection/
│   │   ├── README.md
│   │   ├── materials/
│   │   ├── notebooks/
│   │   ├── src/
│   │   ├── exercises/
│   │   └── assets/
│   │
│   ├── module-03-hand-tracking/
│   │   ├── README.md
│   │   ├── materials/
│   │   ├── notebooks/
│   │   ├── src/
│   │   ├── exercises/
│   │   └── assets/
│   │
│   └── module-04-deep-learning/
│       ├── README.md
│       ├── materials/
│       ├── notebooks/
│       ├── src/
│       ├── exercises/
│       └── assets/
│
├── opening-demo/
│   ├── README.md
│   ├── src/
│   ├── effects/
│   └── assets/
│
└── tutorials/
    ├── 01-installation/
    ├── 02-python-venv/
    └── 03-library-setup/
```
| Folder | Fungsi |
|---|---|
| `docs/` | Dokumentasi keseluruhan pelatihan |
| `setup/` | Pengecekan instalasi dan environment |
| `modules/` | Seluruh materi dan kode per modul |
| `materials/` | PDF, slide, dan materi pembelajaran |
| `notebooks/` | Notebook per topik (bahan sebelum digabung) |
| `src/` | Notebook gabungan per modul, versi lokal dan Colab |
| `exercises/` | Tugas dan starter code peserta |
| `assets/` | Gambar, video pendek, dan aset pendukung |
| `opening-demo/` | Program demo gabungan |
| `tutorials/` | Video dan panduan persiapan |

## Status Modul

| Modul | Status |
|---|---|
| `module-01-opencv-fundamentals` | Tersedia |
| `module-02-face-detection` | Belum diisi |
| `module-03-hand-tracking` | Tersedia |
| `module-04-deep-learning` | Belum diisi |

Folder yang belum diisi sudah dibuat sebagai kerangka (berisi `README.md` atau `.gitkeep`).

## Mulai Cepat

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python setup/check_environment.py
```

Python yang didukung: 3.9 - 3.12 (batas dari `mediapipe==0.10.21`).

## Aturan Penamaan File

- Huruf kecil, kata dipisah `_`. Tanpa spasi dan tanpa `&`.
- Notebook versi Colab diberi akhiran `_colab`.
- Notebook gabungan di `src/` diberi akhiran `_lokal` atau `_colab`.
