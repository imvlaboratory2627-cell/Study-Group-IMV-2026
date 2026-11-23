# Hand Tracking dengan MediaPipe: Landmark, Virtual Painter, Volume Control & Study Case
 
Materi hands-on **IMV Laboratory**. Repositori ini menggabungkan dua notebook (*Hands-on Landmark MediaPipe* dan *Modul 3 Hand Tracking*) menjadi satu alur belajar, dalam dua versi:
 
| File | Dipakai untuk | Kamera |
|---|---|---|
| `hand_tracking_mediapipe_lokal.ipynb` | Jupyter / VS Code di komputer sendiri | Webcam real-time (`cv2.imshow`) |
| `hand_tracking_mediapipe_colab.ipynb` | Google Colab | Foto (upload / kamera browser), video upload, atau simulasi gesture |
 
---
 
## Daftar Isi
 
1. [Yang Akan Dipelajari](#1-yang-akan-dipelajari)
2. [Prasyarat](#2-prasyarat)
3. [Instalasi Versi Lokal](#3-instalasi-versi-lokal)
4. [Menjalankan Versi Lokal](#4-menjalankan-versi-lokal)
5. [Menjalankan Versi Colab](#5-menjalankan-versi-colab)
6. [Isi Notebook Langkah demi Langkah](#6-isi-notebook-langkah-demi-langkah)
7. [Referensi Gesture & Kontrol](#7-referensi-gesture--kontrol)
8. [Parameter yang Bisa Diubah](#8-parameter-yang-bisa-diubah)
9. [Study Case: Penghapus dengan Gesture](#9-study-case-penghapus-dengan-gesture)
10. [Troubleshooting](#10-troubleshooting)
---
 
## 1. Yang Akan Dipelajari
 
- Konsep **landmark** MediaPipe: tangan (21 titik) dan tubuh (33 titik).
- Sistem **koordinat ternormalisasi** `(x, y, z)` dan konversinya ke **piksel** `(cx, cy)`.
- Mendeteksi dan **menghitung jari terangkat**.
- Membuat interaksi berbasis gesture:
  1. **Virtual Painter**: menggambar di udara dengan telunjuk.
  2. **Volume Control**: jarak jempol-telunjuk menjadi volume 0-100%.
  3. **Study Case**: menambahkan **penghapus berbasis gesture** ke painter, dikodekan sendiri dari nol.
**Target:** peserta dapat melacak tangan dan membuat minimal satu interaksi yang dipicu gesture.
 
---
 
## 2. Prasyarat
 
| Kebutuhan | Keterangan |
|---|---|
| Python | **3.9 - 3.12** untuk `mediapipe==0.10.21` (disarankan untuk versi lokal) |
| Webcam | Wajib hanya untuk mode live di versi lokal |
| Sistem operasi | Windows / macOS / Linux. Fitur volume sistem nyata hanya di **Windows** |
| Akun Google | Hanya untuk versi Colab |
 
**Library:**
 
| Library | Fungsi |
|---|---|
| `opencv-python` | Baca kamera, gambar, tampilkan jendela |
| `mediapipe==0.10.21` | Deteksi 21 landmark tangan |
| `numpy` | Operasi array, `np.interp` |
| `matplotlib` | Visualisasi di notebook |
| `jupyter` / `ipykernel` | Menjalankan notebook |
| `pycaw`, `comtypes` | *Opsional*, kontrol volume Windows sungguhan |
 
> **Soal versi `mediapipe`.** Versi lama (<= 0.10.21) memiliki API `mp.solutions.hands`. Versi baru (>= 0.10.30) tidak lagi memilikinya. Notebook sudah menangani keduanya lewat fungsi `make_hands()`: jika `mp.solutions` ada, dipakai langsung; jika tidak, otomatis memakai **Tasks API** (`HandLandmarker`) dan mengunduh model `hand_landmarker.task` sekali (butuh internet). Untuk versi lokal tetap disarankan mengunci ke `0.10.21` agar tidak perlu mengunduh model.
 
---
 
## 3. Instalasi Versi Lokal
 
### 3.1 Siapkan folder proyek
 
```bash
mkdir hand-tracking && cd hand-tracking
# salin kedua file .ipynb dan README.md ke folder ini
```
 
### 3.2 Buat virtual environment
 
**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
Jika muncul error *execution policy*, jalankan dulu: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
 
**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
 
Cek versi Python (disarankan 3.9 - 3.12):
```bash
python --version
```
 
### 3.3 Pasang dependensi
 
```bash
python -m pip install --upgrade pip
pip install opencv-python mediapipe==0.10.21 numpy matplotlib jupyter ipykernel
```
 
Opsional, hanya jika ingin mengubah **volume Windows sungguhan**:
```bash
pip install pycaw comtypes
```
 
### 3.4 Daftarkan kernel (agar muncul di Jupyter / VS Code)
 
```bash
python -m ipykernel install --user --name hand-tracking --display-name "Python (hand-tracking)"
```
 
### 3.5 Verifikasi instalasi
 
```bash
python -c "import cv2, mediapipe as mp, numpy, matplotlib; print('cv2', cv2.__version__); print('solutions OK:', hasattr(mp, 'solutions'))"
```
 
Dengan `mediapipe==0.10.21` hasil yang benar menampilkan versi OpenCV dan `solutions OK: True`. Jika `False` (MediaPipe versi baru), notebook tetap jalan lewat Tasks API, tetapi mengunduh model saat pertama kali dijalankan.
 
### 3.6 Izin kamera
 
- **Windows:** Settings > Privacy & security > Camera > izinkan aplikasi desktop.
- **macOS:** System Settings > Privacy & Security > Camera > izinkan Terminal / VS Code / Jupyter.
- **Linux:** pastikan user termasuk grup `video` dan perangkat ada (`ls /dev/video*`).
---
 
## 4. Menjalankan Versi Lokal
 
1. Aktifkan virtual environment (lihat 3.2), lalu buka notebook:
```bash
jupyter notebook hand_tracking_mediapipe_lokal.ipynb
```
   atau buka file tersebut di **VS Code** dan pilih kernel **Python (hand-tracking)**.
2. Jalankan sel **dari atas ke bawah** secara berurutan (`Shift + Enter`).
3. Sel-sel konsep (Bagian A) menampilkan gambar statis. Urutan sumber citra otomatis:
   1. file `hand.jpg` atau `image.jpg` di folder yang sama,
   2. webcam (1 frame),
   3. kanvas tangan sintetis (fallback).
4. Sel live (`run_live(...)`) membuka **jendela video OpenCV**. Klik jendelanya, lalu tekan **`q`** untuk menutup dan lanjut ke sel berikutnya.
> **Jangan "Run All" tanpa siap.** Ada tiga sel live (hand tracking, Virtual Painter, Volume Control). Tiap sel menahan eksekusi sampai Anda menekan `q`.
 
> Gunakan video sebagai pengganti webcam: ubah `SOURCE = 0` menjadi `SOURCE = "demo.mp4"` pada sel setup, lalu jalankan ulang sel itu.
 
### Mengaktifkan volume sistem Windows (opsional)
 
Pada sel setup, ubah menjadi:
```python
SYSTEM_VOLUME = True
```
Jalankan ulang sel tersebut, lalu jalankan sel Volume Control. Jika `pycaw` gagal, notebook memberi peringatan dan otomatis kembali ke mode simulasi (bar di layar).
 
---
 
## 5. Menjalankan Versi Colab
 
1. Unggah `hand_tracking_mediapipe_colab.ipynb` ke [colab.research.google.com](https://colab.research.google.com) (*File > Upload notebook*), atau simpan di Google Drive lalu buka dengan Colab.
2. Jalankan sel **Setup** pertama (`!pip install -q mediapipe`).
   - Jika muncul error numpy / mediapipe: **Runtime > Restart session**, lalu jalankan ulang dari sel import.
3. Pilih sumber foto pada sel setup lewat variabel `INPUT_MODE`:
   | Nilai | Perilaku |
   |---|---|
   | `"synthetic"` (default) | Tangan sintetis, tanpa input apa pun |
   | `"upload"` | Dialog upload foto tangan dari komputer |
   | `"webcam"` | Tombol **Ambil foto** lewat kamera browser (izinkan akses kamera) |
4. (Opsional) Untuk Painter dan Volume dengan video sendiri, unggah video lalu isi `VIDEO_PATH`:
```python
from google.colab import files
up = files.upload()
VIDEO_PATH = next(iter(up))
```
5. Jalankan sel sampai akhir. Di Colab:
   - Bagian konsep, piksel, dan hitung jari berjalan pada **foto** (jika memilih `upload`/`webcam`) dengan MediaPipe sungguhan.
   - **Painter dan Volume** berjalan pada **video upload** (`VIDEO_PATH`) atau, jika kosong, pada **urutan gesture sintetis**. Hasilnya berupa cuplikan beberapa frame. Logikanya identik dengan versi lokal.
> Colab tidak bisa memakai `cv2.VideoCapture` maupun `cv2.imshow`, sehingga interaksi real-time hanya tersedia di versi lokal.
 
---
 
## 6. Isi Notebook Langkah demi Langkah
 
| # | Bagian | Yang dilakukan |
|---|---|---|
| 0 | **Setup** | Impor library, fungsi bantu (`show`, `make_hands`, `detect`, `to_pixels`, `fingers_up`, `draw_skeleton`), kelas `Painter` dan `VolumeControl`, pemuatan sumber citra |
| 1 | **Akuisisi & deteksi** | Muat citra, konversi BGR ke RGB, deteksi 21 landmark, gambar rangka tangan |
| 2 | **Koordinat ternormalisasi** | Cetak `x, y, z` untuk ID 0/4/8/12/16/20, plot peta landmark (sumbu y dibalik) |
| 3 | **Konversi piksel** | `cx = int(lm.x * w)`, `cy = int(lm.y * h)`, simpan sebagai `lm_list = [[id, cx, cy], ...]` |
| 4 | **Isolasi landmark** | ID 8 sebagai kursor kuas, jarak ID 4 ke ID 8 untuk volume |
| 5 | **Hand tracking dasar** | Mengenali jari terangkat dan label tangan Left/Right (lokal: live multi-tangan + FPS; Colab: satu foto) |
| 6 | **Virtual Painter** | Gambar di udara (lokal: live; Colab: video / simulasi) |
| 7 | **Volume Control** | Jarak jempol-telunjuk menjadi 0-100% + smoothing EMA |
| 8 | **Study case** | Penghapus dengan gesture, dikodekan sendiri dari nol |
 
Bagian A mencakup bagian 1-4 (konsep landmark), Bagian B mencakup bagian 5-8 (hands-on).
 
### Konsep kunci
 
**Dua model landmark**
- Hand: **21 titik** (ID 0-20): 1 pergelangan + 4 titik x 5 jari.
- Pose: **33 titik** (ID 0-32): kerangka tubuh penuh.
**ID tangan yang wajib dihafal**
 
| ID | Bagian | Dipakai untuk |
|---|---|---|
| 0 | Wrist (pergelangan) | Acuan kedalaman `z`, ukuran telapak |
| 4 | Ujung jempol | Volume Control |
| 8 | Ujung telunjuk | Kursor Virtual Painter |
| 12 / 16 / 20 | Ujung tengah / manis / kelingking | Hitung jari |
 
**Koordinat ternormalisasi**
- `x`: 0.0 (kiri) sampai 1.0 (kanan).
- `y`: 0.0 (atas) sampai 1.0 (bawah). Makin ke bawah, nilai `y` makin **besar**.
- `z`: kedalaman relatif terhadap pergelangan. Makin **negatif** berarti makin dekat ke kamera.
- Semuanya rasio terhadap ukuran frame, **bukan** piksel.
**BGR vs RGB:** OpenCV membaca **BGR**, MediaPipe dan Matplotlib memakai **RGB**. Konversi `cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)` **wajib** sebelum `hands.process()`. Jika terlewat, deteksi gagal dan warna tertukar.
 
**Urutan dimensi OpenCV:** `h, w, c = frame.shape` (tinggi dulu, bukan lebar).
 
**Logika hitung jari**
- Jari selain jempol terangkat jika `y` ujung < `y` sendi PIP (ID `tip - 2`). Ingat: posisi lebih tinggi di layar berarti `y` lebih kecil.
- Jempol dibandingkan di sumbu `x` (ID 4 terhadap ID 3), tergantung tangan kiri/kanan. Frame diasumsikan sudah di-**mirror** dan telapak menghadap kamera.
**Format `info`:** setelah bagian 5, semua logika aplikasi menerima `info = [(pts, up, label), ...]`, yaitu 21 titik piksel, status 5 jari `[jempol, telunjuk, tengah, manis, kelingking]`, dan label tangan. List kosong berarti tidak ada tangan.
 
**Normalisasi jarak (Volume):** jarak jempol-telunjuk dibagi ukuran telapak (ID 0 ke ID 5), sehingga hasilnya konsisten walau tangan dekat atau jauh dari kamera. Nilai dihaluskan dengan *exponential moving average* (EMA) agar bar tidak bergetar.
 
**Fallback:** jika MediaPipe tidak mendeteksi tangan, notebook memakai 21 landmark sintetis (telapak terbuka). Variabel `hand_lms` selalu terisi, sehingga tidak muncul error `NoneType`.
 
---
 
## 7. Referensi Gesture & Kontrol
 
### Virtual Painter
 
| Gesture | Aksi |
|---|---|
| Telunjuk saja terangkat | **Menggambar** |
| Telunjuk + tengah terangkat | Pindah posisi (pen diangkat) |
| Telapak terbuka (5 jari) ditahan ~25 frame (~1 detik) | **Hapus semua** |
 
Keyboard (fokus di jendela video, **hanya versi lokal**):
 
| Tombol | Fungsi |
|---|---|
| `1` / `2` / `3` / `4` | Biru / Hijau / Merah / Kuning |
| `e` | Toggle penghapus |
| `c` | Hapus kanvas |
| `q` | Keluar |
 
### Volume Control
 
| Gesture | Aksi |
|---|---|
| Jempol dan telunjuk menempel | Volume ~0% |
| Jempol dan telunjuk terbuka lebar | Volume ~100% |
 
---
 
## 8. Parameter yang Bisa Diubah
 
| Parameter | Default | Efek |
|---|---|---|
| `SOURCE` (lokal) | `0` | `0/1/2` = nomor webcam, atau path video (`"demo.mp4"`) |
| `INPUT_MODE` (Colab) | `"synthetic"` | `"synthetic"` / `"webcam"` / `"upload"` |
| `VIDEO_PATH` (Colab) | `None` | Nama file video untuk Painter dan Volume. `None` = simulasi sintetis |
| `make_hands(detection_conf=...)` | `0.7` | Ambang deteksi awal tangan |
| `make_hands(tracking_conf=...)` | `0.6` | Ambang pelacakan antar-frame |
| `Painter.CLEAR_HOLD_FRAMES` | `25` | Lama menahan telapak sebelum kanvas dihapus |
| `RATIO_MIN` | `0.25` | Rasio cubitan yang dianggap 0% |
| `RATIO_MAX` | `1.40` | Rasio cubitan yang dianggap 100% |
| `SMOOTH` | `0.2` | Smoothing volume. Makin kecil makin halus tapi makin lambat (Colab memakai 0.5 agar cepat mengejar pada urutan pendek) |
| `SYSTEM_VOLUME` (lokal) | `False` | `True` = ubah volume Windows sungguhan |
 
---
 
## 9. Study Case: Penghapus dengan Gesture
 
**Masalah:** di Virtual Painter, menghapus harus menekan tombol `e` di keyboard, padahal tangan sedang "di udara". Rancang sendiri painter mini yang bisa menghapus hanya dengan gesture.
 
**Syarat minimal:**
 
| Gesture | Aksi |
|---|---|
| Telunjuk saja terangkat | Menggambar garis |
| Telunjuk + tengah terangkat, ujung **merenggang** | Pen diangkat (tidak menggambar, tidak menghapus) |
| Telunjuk + tengah terangkat, ujung **merapat** | Menghapus coretan di bawah ujung jari |
 
Coretan harus tetap ada antar-frame (butuh kanvas yang bertahan).
 
**Kontrak fungsi:** peserta menulis `my_step(frame, info)` yang dipanggil tiap frame dengan `frame` (gambar BGR) dan `info` (format di bagian 6). Study case ini **tidak menyediakan kode**, solusi dikerjakan dari nol di sel baru.
 
**Menjalankan:**
- Lokal: `run_live(my_step, "Studi Kasus")` untuk webcam, atau `run_offline(synthetic_eraser_sequence(), my_step, every=15, max_snap=3, cols=4)` tanpa webcam.
- Colab: `run_offline(synthetic_eraser_sequence(), my_step, every=15, max_snap=3, cols=4)`. Untuk video sendiri, isi `VIDEO_PATH` lalu pakai `get_sequence("painter")` sebagai pengganti `synthetic_eraser_sequence()`.
**Hasil yang benar pada simulasi:** garis lurus yang bagian tengahnya hilang.
 
**Bahan diskusi:**
1. Mengapa `fingers_up()` saja tidak cukup untuk membedakan merapat vs merenggang?
2. Apa efek ambang jarak yang terlalu besar atau terlalu kecil?
3. Bagaimana menormalisasi jarak agar tidak bergantung pada jauh-dekatnya tangan dari kamera? (petunjuk: normalisasi pada Volume Control)
---
 
## 10. Troubleshooting
 
| Masalah | Solusi |
|---|---|
| `module 'mediapipe' has no attribute 'solutions'` | Notebook ini sudah menanganinya otomatis (Tasks API, perlu internet sekali untuk mengunduh model). Alternatif: `pip install mediapipe==0.10.21` dengan Python 3.9 - 3.12 |
| Gagal mengunduh `hand_landmarker.task` | Cek koneksi internet / proxy, atau pakai `mediapipe==0.10.21` |
| `RuntimeError: Tidak bisa membuka sumber video` | Ganti `SOURCE` (0/1/2), tutup aplikasi lain yang memakai kamera, atau pakai file video. Cek izin kamera (3.6) |
| Jendela video tidak muncul | Di Colab jendela live tidak didukung, gunakan versi lokal. Di lokal, pastikan memakai `opencv-python` (bukan `-headless`) |
| Sel macet, jendela tidak bisa ditutup | Klik jendela video lalu tekan `q`. Jika masih macet: **Restart Kernel** |
| Jempol terbaca terbalik | Pastikan telapak menghadap kamera. Hitungan jempol mengasumsikan frame di-mirror (foto dan video sudah di-mirror otomatis oleh notebook) |
| Tangan tidak terdeteksi pada foto | Pakai foto dengan tangan jelas, cahaya cukup, latar sederhana. Sementara itu notebook memakai landmark sintetis |
| Kamera tidak menyala di Colab (`INPUT_MODE = "webcam"`) | Izinkan akses kamera di browser (ikon gembok di address bar), lalu jalankan ulang sel |
| Garis Painter patah-patah | Naikkan cahaya ruangan, gerakkan tangan lebih pelan |
| Volume tidak berubah | `SYSTEM_VOLUME = True` hanya bekerja di Windows dengan `pycaw` terpasang. Selain itu hanya bar simulasi |
| Error numpy di Colab setelah `pip install` | **Runtime > Restart session**, jalankan ulang dari sel import |
| Warna gambar tertukar (merah tampak biru) | Konversi BGR ke RGB terlewat sebelum `plt.imshow` atau `hands.process` |
| Titik landmark menumpuk di pojok kiri atas | Koordinat belum dikali `w` / `h` (konversi piksel terlewat) |
 
---
 
*Study Group IMV Laboratory 2026.*