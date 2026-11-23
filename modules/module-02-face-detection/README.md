# Hands-on IMV Laboratory: Chroma Key, Filtering, dan Edge Detection

Modul praktikum study group **IMV Laboratory** untuk pemrosesan citra digital dengan Python dan OpenCV. Dua materi digabung dalam satu alur: **ruang warna dan chroma keying**, lalu **konvolusi, filtering, dan edge detection**, ditutup dengan bonus hapus background dan satu studi kasus.

## Daftar Isi

1. [Tujuan Pembelajaran](#tujuan-pembelajaran)
2. [Struktur Materi](#struktur-materi)
3. [Prasyarat](#prasyarat)
4. [Setup Versi Lokal (VSCode)](#setup-versi-lokal-vscode)
5. [Setup Versi Google Colab](#setup-versi-google-colab)
6. [File Pendukung (Opsional)](#file-pendukung-opsional)
7. [Cara Menjalankan Notebook](#cara-menjalankan-notebook)
8. [Mekanisme Fallback](#mekanisme-fallback)
9. [Output yang Dihasilkan](#output-yang-dihasilkan)
10. [Troubleshooting](#troubleshooting)
11. [Studi Kasus (Bagian 4)](#studi-kasus-bagian-4)
12. [Referensi Fungsi Utama](#referensi-fungsi-utama)

---

## Tujuan Pembelajaran

Setelah menyelesaikan modul ini, kamu dapat:

- Menjelaskan urutan channel **BGR** pada OpenCV dan kenapa citra perlu dikonversi ke RGB sebelum ditampilkan dengan Matplotlib.
- Menjelaskan kelemahan RGB untuk segmentasi warna dan keunggulan **HSV**.
- Membedakan `cv2.threshold` (grayscale) dengan `cv2.inRange` (rentang warna HSV).
- Membuat **mask biner**, memakai `cv2.bitwise_not` dan `cv2.bitwise_and`, lalu menggabungkan subjek dengan background baru memakai `cv2.add`.
- Menulis **konvolusi 2D** dengan loop, memverifikasinya terhadap OpenCV, dan memahami efek padding.
- Menerapkan filter mean, Gaussian, median, dan sharpening, serta memilih filter yang tepat untuk jenis noise tertentu.
- Mendeteksi tepi dengan Sobel, Prewitt, Laplacian/LoG, dan Canny.
- Menghapus background dengan Otsu, edge + contour, dan GrabCut.

## Struktur Materi

### Bagian 1: Color Space, Thresholding, dan Background Replacement

| Sub | Topik | Fungsi kunci |
|---|---|---|
| 1.0 | Akuisisi frame dan gambar background | `cv2.VideoCapture`, `cv2.imread`, `cv2.cvtColor` |
| 1.1 | Ruang warna HSV dan channel H, S, V | `cv2.cvtColor(..., COLOR_BGR2HSV)`, `cv2.split` |
| 1.2 | Binary threshold vs HSV range | `cv2.threshold`, `cv2.inRange` |
| 1.3 | Masking dan operasi bitwise | `cv2.bitwise_not`, `cv2.bitwise_and` |
| 1.4 | Penggabungan akhir | `cv2.add` |
| 1.5 | Live chroma key (lokal) atau fungsi per-frame (Colab) | `run_live_chroma_key()` / `chroma_key_frame()` |

### Bagian 2: Filtering dan Edge Detection

| Sub | Topik | Fungsi kunci |
|---|---|---|
| 2.0 | Persiapan gambar grayscale | `load_image`, `resize_max` |
| 2.1 | Konvolusi 2D manual, verifikasi, border handling | `convolve2d`, `cv2.filter2D` |
| 2.2 | Filtering: mean, Gaussian, median, sharpening | `gaussian_kernel`, `median_filter`, `cv2.GaussianBlur`, `cv2.medianBlur` |
| 2.3 | Edge detection: Sobel/Prewitt, pengaruh noise, Laplacian/LoG, Canny | `gradient`, `zero_crossing`, `cv2.Sobel`, `cv2.Canny` |
| 2.4 | Perbandingan akhir pada gambar ber-noise | `show` |

### Bagian 3: Bonus Hapus Background

| Metode | Ide |
|---|---|
| A. Otsu + morfologi | Pisahkan berdasarkan terang/gelap |
| B. Canny + contour | Tutup celah tepi, isi kontur terbesar |
| C. GrabCut | Model warna foreground vs background dengan kotak (`rect`) |

Ditutup dengan ekspor **PNG transparan** dan penggantian background lewat alpha blending.

### Bagian 4: Studi Kasus

Perbaikan hasil chroma key yang kasar (bintik noise dan tepi bergerigi) memakai konsep dari Bagian 1 sampai 3.

## Prasyarat

| Kebutuhan | Keterangan |
|---|---|
| Python | 3.9 atau lebih baru (disarankan 3.10+) |
| Library wajib | `numpy`, `opencv-python`, `matplotlib`, `scikit-image` |
| Library opsional | `numba` (mempercepat loop manual puluhan sampai ratusan kali) |
| Webcam | Opsional; hanya untuk mengambil foto sendiri atau live chroma key |
| Kain hijau / biru | Opsional; tanpa itu dipakai citra sintetis |

> Tanpa `numba` semua sel tetap berjalan dengan Python murni, hanya lebih lambat pada sel konvolusi dan median.

## Setup Versi Lokal (VSCode)

### 1. Siapkan folder dan virtual environment

```bash
mkdir imv-handson && cd imv-handson
# salin kedua file .ipynb dan README.md ke folder ini

python -m venv .venv
```

Aktifkan environment:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat

# macOS / Linux
source .venv/bin/activate
```

### 2. Install library

```bash
pip install --upgrade pip
pip install numpy opencv-python matplotlib scikit-image numba
pip install ipykernel jupyter
```

Atau simpan sebagai `requirements.txt`:

```text
numpy
opencv-python
matplotlib
scikit-image
numba
ipykernel
jupyter
```

lalu jalankan `pip install -r requirements.txt`.

> Jangan menginstal `opencv-python` dan `opencv-python-headless` bersamaan. Versi headless tidak punya GUI sehingga `cv2.imshow` (live chroma key) tidak akan bekerja.

### 3. Buka di VSCode

1. Install ekstensi **Python** dan **Jupyter** dari Marketplace VSCode.
2. Buka folder `imv-handson` (`File > Open Folder`).
3. Buka `IMV_HandsOn_Gabungan_Lokal.ipynb`.
4. Klik **Select Kernel** di pojok kanan atas, pilih interpreter `.venv` yang tadi dibuat.
5. Jalankan sel pertama untuk memeriksa. Keluaran yang benar:

```
OpenCV  : 4.x.x
numba tersedia: True
```

### 4. Izin kamera (hanya bila memakai webcam)

- **Windows:** `Settings > Privacy & security > Camera`, izinkan aplikasi desktop.
- **macOS:** `System Settings > Privacy & Security > Camera`, izinkan VSCode / Terminal. Restart VSCode setelah memberi izin.
- **Linux:** pastikan user masuk grup `video` dan perangkat ada di `/dev/video0`.

## Setup Versi Google Colab

1. Buka [colab.research.google.com](https://colab.research.google.com), pilih **File > Upload notebook**, unggah `IMV_HandsOn_Gabungan_Colab.ipynb`. (Atau unggah ke Google Drive lalu buka dengan Colab.)
2. Pilih runtime Python biasa (CPU sudah cukup; GPU tidak diperlukan).
3. Jalankan sel dari atas ke bawah (`Runtime > Run all`, atau `Shift+Enter` per sel).

Colab sudah memiliki semua library yang dibutuhkan. Bila ada yang kurang, hapus tanda `#` pada sel instalasi di awal:

```python
!pip install -q numpy opencv-python matplotlib scikit-image numba
```

### Memilih sumber frame di Colab

Colab berjalan di server jarak jauh, sehingga `cv2.VideoCapture(0)` dan `cv2.imshow` **tidak bisa dipakai**. Sebagai gantinya, ubah variabel `SUMBER_FRAME` pada Bagian 1.0:

| Nilai | Perilaku |
|---|---|
| `'sintetis'` (default) | Citra buatan, tanpa izin apa pun |
| `'webcam'` | Muncul tombol **Ambil foto**; browser meminta izin kamera |
| `'upload'` | Dialog upload; pilih foto dari komputer |

Untuk background pengganti sendiri, set `UPLOAD_BACKGROUND = True`. Untuk gambar Bagian 2 dan 3, hapus tanda `#` pada baris `IMAGE_PATH = upload_file() or IMAGE_PATH`.

> File yang diunggah ke Colab hanya bertahan selama runtime aktif. Setelah runtime terputus, unggah ulang.

## File Pendukung (Opsional)

| File | Dipakai di | Fungsi | Bila tidak ada |
|---|---|---|---|
| `foto_subjek.jpg` | Bagian 1.0 (lokal, `SUMBER_FRAME = 'file'`) | Foto subjek di depan green screen | Citra sintetis |
| `background.jpg` | Bagian 1.0 dan live chroma key | Background pengganti | Pemandangan sintetis |
| `h2hjuun.jpg` | Bagian 2 dan 3 | Gambar sendiri untuk filtering dan hapus background | `skimage.data.camera()` dan `data.astronaut()` |

Letakkan file di folder yang sama dengan notebook. Untuk memakai nama file lain, ubah `bg_path`, `FRAME_PATH`, atau `IMAGE_PATH` pada sel terkait.

**Tips foto green screen yang baik:**
- Kain hijau rata, minim kerutan.
- Pencahayaan merata; hindari bayangan tajam pada kain.
- Jangan memakai pakaian berwarna hijau.
- Jarak subjek dari kain sekitar 1 meter agar tidak ada pantulan hijau di tepi badan.

## Cara Menjalankan Notebook

Jalankan sel **berurutan dari atas ke bawah**. Sel-sel di bawah bergantung pada variabel dari sel sebelumnya (`frame`, `mask`, `img`, dan seterusnya).

### Langkah singkat

1. **Setup dan fungsi bantu:** jalankan sel import dan sel `show()`.
2. **Bagian 1:** ambil frame, lihat channel HSV, bandingkan threshold, buat mask, gabungkan background.
3. **Bagian 2:** muat gambar grayscale, bangun konvolusi, uji filter dan edge detector.
4. **Bagian 3:** coba tiga metode hapus background, simpan PNG transparan.
5. **Bagian 4:** kerjakan studi kasus.

### Mode live webcam (hanya versi lokal)

Di versi lokal, sel terakhir Bagian 1.5 berisi fungsi `run_live_chroma_key()`. Hapus tanda komentar pada baris pemanggilan untuk menjalankannya:

```python
run_live_chroma_key('background.jpg')
```

Jendela video akan terbuka. Tekan **`q`** pada jendela video untuk berhenti. Bila jendela tidak terlihat, cek apakah tersembunyi di belakang jendela VSCode.

### Waktu eksekusi

Dengan `numba` terpasang, seluruh notebook selesai dalam hitungan detik sampai satu menit (sel pertama yang memanggil fungsi `njit` ikut mengompilasi, jadi sedikit lebih lama). Tanpa `numba`, sel konvolusi dan median pada gambar 256 piksel bisa memakan beberapa detik hingga puluhan detik per sel.

## Mekanisme Fallback

Notebook dirancang agar **selalu bisa dijalankan sampai selesai**:

| Kondisi | Yang terjadi |
|---|---|
| Webcam tidak ada / gagal dibuka | Frame diganti citra sintetis 480 x 640 (subjek simulasi di depan latar hijau) |
| `background.jpg` tidak ditemukan | Dibuat background pemandangan sintetis |
| File gambar Bagian 2 dan 3 tidak ditemukan | Dipakai `skimage.data.camera()` (grayscale) dan `data.astronaut()` (warna) |
| `numba` tidak terpasang | Loop manual berjalan dengan Python murni |

Pesan `[INFO]` pada keluaran sel menunjukkan fallback mana yang sedang aktif.

> Dengan gambar contoh `astronaut`, kotak `rect` GrabCut belum disesuaikan sehingga hasil potongannya kemungkinan kurang rapi. Atur `rect` pada sel 3.C bila perlu (lihat Troubleshooting).

## Output yang Dihasilkan

| Output | Lokasi | Keterangan |
|---|---|---|
| Visualisasi perbandingan | Di dalam notebook | Dibuat dengan `show()` |
| `hasil_tanpa_background.png` | Folder kerja notebook | PNG transparan hasil GrabCut (RGBA) |
| `webcam_frame.jpg` | Folder kerja Colab | Hanya bila memakai `take_photo()` |

Di Colab, untuk mengunduh PNG ke komputer, hapus tanda `#` pada baris `files.download('hasil_tanpa_background.png')`.

## Troubleshooting

| Gejala | Penyebab | Solusi |
|---|---|---|
| `ModuleNotFoundError: cv2` | OpenCV belum terpasang di kernel yang dipilih | `pip install opencv-python`, lalu pastikan kernel VSCode menunjuk ke `.venv` yang sama |
| Warna gambar terbalik (kulit kebiruan) | Citra BGR ditampilkan langsung | Konversi dulu dengan `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` |
| `[INFO] Frame tidak tersedia...` padahal punya webcam | Kamera dipakai aplikasi lain, atau izin ditolak | Tutup Zoom/Teams/browser yang memakai kamera, cek izin kamera OS. Coba indeks lain: `cv2.VideoCapture(1)` |
| `cv2.imshow` error / jendela tidak muncul | Memakai `opencv-python-headless`, atau di server tanpa display | `pip uninstall opencv-python-headless`, lalu `pip install opencv-python`. Di Colab gunakan versi Colab |
| Live chroma key mengunci jendela | Loop menunggu tombol `q` | Fokuskan jendela video, tekan `q`. Bila macet, interrupt kernel |
| Mask bocor / ada lubang di subjek | Rentang HSV tidak cocok dengan warna kainmu | Periksa nilai `frame_hsv[y, x]` pada kain, lalu sesuaikan `lower_green` dan `upper_green` |
| Subjek ikut terhapus | Pakaian atau kulit masuk dalam rentang hue latar | Persempit rentang Hue, naikkan batas bawah Saturation |
| Bintik hitam kecil di background | Noise pada mask | `cv2.medianBlur(mask, 5)` atau blur frame sebelum threshold |
| Sel konvolusi sangat lambat | `numba` tidak ada, atau gambar terlalu besar | Install `numba`; pastikan gambar lewat `resize_max` (maks 256 piksel) |
| GrabCut memotong salah | `rect` tidak melingkupi objek | Ubah pecahan pada `rect = (int(0.15*w), int(0.02*h), int(0.70*w), int(0.96*h))` |
| `cv2.error` pada `findContours` / `max()` of empty | Canny tidak menemukan tepi | Turunkan threshold Canny, atau kurangi blur |
| `files.upload()` / `take_photo()` tidak jalan | Memakai notebook versi lokal di Colab | Gunakan `IMV_HandsOn_Gabungan_Colab.ipynb` |
| Webcam browser Colab tidak muncul | Izin kamera browser ditolak | Izinkan kamera untuk `colab.research.google.com` pada pengaturan situs browser |

## Studi Kasus (Bagian 4)

**Situasi:** mengganti background video call dengan foto kampus. Hasil chroma key awal kasar: ada bintik noise dan tepi bergerigi.

**Tugas:**

1. Buat chroma key dasar dengan `cv2.inRange` dan `cv2.add`.
2. Bersihkan bintik pada mask dengan `cv2.medianBlur(mask, 5)`.
3. Haluskan tepi: blur mask dengan `cv2.GaussianBlur`, lalu alpha blending (`alpha * subjek + (1 - alpha) * background`).
4. Bandingkan tiga hasil dengan `show()`: dasar, setelah median, setelah feathering.

**Bonus:** jalankan `cv2.Canny` pada mask untuk memeriksa kemulusan tepi.

## Referensi Fungsi Utama

**Ruang warna dan masking**

| Fungsi | Kegunaan |
|---|---|
| `cv2.cvtColor(img, code)` | Konversi ruang warna (BGR, RGB, HSV, GRAY) |
| `cv2.inRange(hsv, lower, upper)` | Mask biner untuk rentang warna |
| `cv2.bitwise_not(mask)` | Membalik mask |
| `cv2.bitwise_and(a, a, mask=m)` | Meloloskan piksel sesuai mask |
| `cv2.add(a, b)` | Penjumlahan citra dengan saturasi 255 |

Rentang HSV pada OpenCV (`uint8`): H `0-179`, S `0-255`, V `0-255`.

| Warna latar | `lower` | `upper` |
|---|---|---|
| Hijau | `[35, 50, 50]` | `[85, 255, 255]` |
| Biru | `[90, 50, 50]` | `[130, 255, 255]` |
| Merah (sisi bawah) | `[0, 70, 50]` | `[10, 255, 255]` |

Merah melingkar di roda hue, jadi untuk cakupan penuh gabungkan dua mask: `0-10` dan `170-179`.

**Filtering dan edge detection**

| Fungsi | Kegunaan |
|---|---|
| `convolve2d` (buatan sendiri) | Konvolusi 2D manual dengan padding zero / replicate / reflect |
| `cv2.filter2D` | Korelasi dengan kernel (flip kernel agar setara konvolusi) |
| `cv2.GaussianBlur` | Low-pass Gaussian; cocok untuk Gaussian noise |
| `cv2.medianBlur` | Filter median; cocok untuk salt-and-pepper |
| `cv2.Sobel` | Turunan orde pertama |
| `cv2.Canny` | Edge detector multi-tahap (blur, gradien, NMS, double threshold, hysteresis) |
| `cv2.grabCut` | Segmentasi foreground/background dengan kotak awal |

**Panduan memilih filter**

| Jenis noise | Filter yang cocok |
|---|---|
| Gaussian noise | Gaussian atau mean |
| Salt-and-pepper | Median |
| Sebelum edge detection | Gaussian blur dulu (turunan memperbesar noise) |

---

*Study group IMV Laboratory 2026.*