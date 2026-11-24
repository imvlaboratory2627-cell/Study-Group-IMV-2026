# Modul 2 — Study Group IMV
---

## Daftar Isi

1. [Tujuan & Pemahaman Dasar](#1-tujuan--pemahaman-dasar)
2. [Gambar adalah Angka, Video adalah Deretan Frame](#2-gambar-adalah-angka-video-adalah-deretan-frame)
3. [Face Detection vs Face Recognition](#3-face-detection-vs-face-recognition)
4. [Cara Kerja Haar Cascade](#4-cara-kerja-haar-cascade)
5. [Haar Cascade di OpenCV](#5-haar-cascade-di-opencv)
6. [Detection vs Landmark](#6-detection-vs-landmark)
7. [dlib: 68 Titik Landmark Wajah](#7-dlib-68-titik-landmark-wajah)
8. [Alur Program `facelandmark.py`](#8-alur-program-facelandmarkpy)
9. [Koordinat Titik Wajah](#9-koordinat-titik-wajah)
10. [Dari Titik ke Informasi: MAR (Mulut Terbuka)](#10-dari-titik-ke-informasi-mar-mulut-terbuka)
11. [Posisi & Ukuran Filter dari Mata](#11-posisi--ukuran-filter-dari-mata)
12. [Alpha Blending: Tempel yang Transparan](#12-alpha-blending-tempel-yang-transparan)
13. [Dua Filter Digambar Berlapis](#13-dua-filter-digambar-berlapis)
14. [Melatih Model Sendiri](#14-melatih-model-sendiri)
15. [Model Resmi vs Model Sendiri](#15-model-resmi-vs-model-sendiri)
16. [Format Dataset Latihan (XML)](#16-format-dataset-latihan-xml)
17. [Pengaturan Training](#17-pengaturan-training)
18. [Sesi Hands-on](#18-sesi-hands-on)

---

## 1. Tujuan & Pemahaman Dasar

Tujuan modul: peserta mampu membedakan **face detection** dan **face recognition**, memakai **Haar Cascade** untuk mendeteksi wajah di gambar/video, mengambil **landmark 68 titik** memakai **dlib**, lalu memanfaatkan koordinat landmark untuk aplikasi praktis (filter mata, deteksi mulut terbuka, dsb).

Pemahaman dasar yang harus sudah terbentuk sebelum modul ini:
- Gambar di OpenCV disimpan sebagai `numpy.ndarray` berformat **BGR** (lihat Modul 1).
- Operasi matriks di NumPy sama dengan operasi atas intensitas piksel.

---

## 2. Gambar adalah Angka, Video adalah Deretan Frame

- **Gambar** = matriks 2D (grayscale) atau 3D (berwarna) berisi **intensitas piksel**.
- **Video** = **deretan frame**. Setiap frame adalah satu gambar statis. Pemrosesan video pada dasarnya adalah pemrosesan gambar yang di-loop per frame.

Konsekuensi: semua teknik pengolahan citra (filtering, deteksi, landmarking) dapat langsung diterapkan ke video dengan membaca frame satu per satu dari `cv2.VideoCapture`.

---

## 3. Face Detection vs Face Recognition

| | **Face Detection** | **Face Recognition** |
|---|---|---|
| Pertanyaan | Ada wajah di mana? | Wajah ini milik siapa? |
| Hasil | **Kotak** `(x, y, lebar, tinggi)` | **Identitas** |
| Contoh | Fokus otomatis kamera, menghitung jumlah orang | Buka kunci ponsel, absensi |
| Algoritma di modul | **Haar Cascade** dan **YOLOv8** | (di luar lingkup modul ini) |

Face detection adalah **prasyarat** untuk recognition: tidak bisa mengenali identitas kalau belum tahu di mana wajahnya.

---

## 4. Cara Kerja Haar Cascade

Haar Cascade mendeteksi wajah dengan tiga komponen inti:

### 4.1 Fitur Haar — pola terang dan gelap

Fitur Haar adalah **pola terang-gelap sederhana** berupa persegi yang mengukur selisih intensitas rata-rata antar area.

Contoh pola khas wajah: **area mata lebih gelap daripada pipi** → fitur Haar berupa dua persegi horizontal (atas gelap, bawah terang) akan menangkapnya.

### 4.2 Sliding Window — mencari wajah di gambar

**Jendela kecil digeser ke seluruh gambar** pada **berbagai ukuran (skala)**. Setiap posisi jendela dievaluasi: wajah atau bukan.

### 4.3 Cascade — seleksi berlapis

- **Tahap awal** melakukan evaluasi cepat; area yang jelas bukan wajah **langsung ditolak**.
- Hanya area yang **lolos semua tahap** yang dinyatakan wajah.

Haar Cascade **bekerja pada gambar grayscale**. Cepat karena **hampir semua area gugur di tahap awal** — dianalogikan seperti **seleksi berkas sebelum wawancara**: yang tidak lolos berkas tidak perlu diproses lebih jauh.

---

## 5. Haar Cascade di OpenCV

OpenCV menyertakan berkas Haar Cascade terlatih (`haarcascade_frontalface_default.xml` dll). Pola pemakaian:

```python
import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

img  = cv2.imread("foto.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
```

Keluaran `faces` adalah list kotak `(x, y, w, h)` — satu per wajah.

---

## 6. Detection vs Landmark

| Parameter | **Detection** | **Landmark** |
|---|---|---|
| Hasil | **1 kotak per wajah** | **Banyak titik** di wajah |
| Menjawab | Wajah ada di mana? | Di mana mata, hidung, mulut? |
| Kegunaan | Hitung orang, crop wajah | Filter mata, MAR, EAR, head pose, dsb. |

Landmark **lebih kaya informasi** — kotak hanya area, titik membawa geometri wajah.

---

## 7. dlib: 68 Titik Landmark Wajah

**dlib** menyediakan model landmark wajah dengan **68 titik** terstandar:

| Indeks | Bagian |
|---|---|
| `0–16` | Garis rahang (chin / jawline) |
| `17–21` | Alis kanan |
| `22–26` | Alis kiri |
| `27–30` | Batang hidung |
| `31–35` | Dasar hidung |
| `36–41` | Mata kanan (6 titik) |
| `42–47` | Mata kiri (6 titik) |
| `48–59` | Bibir luar (12 titik) |
| `60–67` | Bibir dalam (8 titik) |

Model yang dipakai: `shape_predictor_68_face_landmarks.dat`.

Cara titik ditemukan (singkat): model regresi bertingkat (**ensemble of regression trees** / ERT) memprediksi pergeseran tiap titik dari posisi awal, iteratif sampai konvergen.

---

## 8. Alur Program `facelandmark.py`

Alur umum skrip landmark wajah:

```python
import cv2, dlib

detector  = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret: break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for face in detector(gray):
        shape = predictor(gray, face)
        pts = [(shape.part(i).x, shape.part(i).y) for i in range(68)]
        for (x, y) in pts:
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

    cv2.imshow("landmark", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
```

Langkah:
1. Konversi frame ke grayscale.
2. `detector` → dapatkan bounding box tiap wajah.
3. `predictor` → dapatkan 68 titik landmark untuk tiap kotak wajah.
4. Gambar titik-titik ke frame asli.

---

## 9. Koordinat Titik Wajah

Setiap titik landmark adalah pasangan `(x, y)` dalam **koordinat piksel gambar** (origin di sudut kiri-atas, `x` ke kanan, `y` ke bawah).

Operasi geometri umum yang dipakai dari koordinat:
- **Jarak Euclidean** antara dua titik:
  `d = sqrt((x2-x1)**2 + (y2-y1)**2)`
- **Titik tengah**:
  `cx, cy = (x1+x2)/2, (y1+y2)/2`
- **Rasio** antara dua jarak (untuk MAR, EAR).

---

## 10. Dari Titik ke Informasi: MAR (Mulut Terbuka)

**MAR = Mouth Aspect Ratio.** Rasio bukaan mulut terhadap lebarnya.

Rumus umum (memakai 8 titik bibir dalam `60–67`):

```
MAR = (|p62 - p68| + |p63 - p67| + |p64 - p66|) / (3 * |p61 - p65|)
```

(Gunakan indeks bibir dalam dari skema dlib 68 titik; nama di atas mengikuti konvensi 1-indexed yang umum di literatur.)

Interpretasi:
- **MAR kecil** → mulut tertutup.
- **MAR melewati threshold** (mis. `0.6`) selama beberapa frame → **mulut terbuka / menguap**.

Pola ini juga dipakai untuk **EAR (Eye Aspect Ratio)** mendeteksi kedipan mata memakai titik `36–41` / `42–47`.

---

## 11. Posisi & Ukuran Filter dari Mata

Untuk menempel filter (mis. kacamata) ke wajah, posisi dan ukuran filter diturunkan dari **titik mata**:

- **Posisi x, y** filter: dari titik pojok luar mata kanan (`36`) dan pojok luar mata kiri (`45`), atau titik tengahnya.
- **Lebar filter** proporsional dengan **jarak antar-mata** (`|p36 - p45|`).
- **Tinggi** mengikuti rasio asli PNG filter (`height = width * h0 / w0`).
- **Rotasi** (opsional): sudut dari garis mata — `angle = atan2(y45-y36, x45-x36)`.

Ini membuat filter **menyesuaikan skala** ketika wajah mendekat/menjauh dari kamera.

---

## 12. Alpha Blending: Tempel yang Transparan

PNG filter punya **kanal alpha** (`A`) selain BGR. Alpha menentukan **transparansi per piksel** (`0` = transparan penuh, `255` = opaque).

Rumus alpha blending per piksel:

```
out = alpha * filter + (1 - alpha) * background
```

Implementasi NumPy:

```python
bgr   = filter_rgba[..., :3]
alpha = filter_rgba[..., 3:] / 255.0    # shape (h, w, 1)

roi = frame[y:y+h, x:x+w]
frame[y:y+h, x:x+w] = (alpha * bgr + (1 - alpha) * roi).astype(np.uint8)
```

Catatan:
- Pastikan filter sudah di-**resize** ke ukuran target sebelum blending.
- Pastikan ROI tidak keluar dari frame — clip koordinat kalau perlu.

---

## 13. Dua Filter Digambar Berlapis

Kalau ingin menempel **dua filter** sekaligus (mis. kacamata + topi):

1. Mulai dari frame asli sebagai background.
2. Blend filter **paling bawah** (kacamata) dulu, hasilnya jadi background baru.
3. Blend filter **paling atas** (topi) di atas background baru.

Urutan penting: filter yang di-blend **belakangan** akan **menutupi** yang sebelumnya di area tumpang-tindih (persis seperti layer di Photoshop, ditumpuk dari bawah ke atas).

---

## 14. Melatih Model Sendiri

Alternatif dari memakai model resmi: **latih Haar Cascade sendiri** untuk objek spesifik (bukan hanya wajah frontal). Dipakai bila objek target tidak ada modelnya atau performa model umum tidak cukup.

Alur global:
1. **Kumpulkan dataset positif** (gambar berisi objek) dan **negatif** (gambar tanpa objek).
2. **Anotasi** kotak objek di tiap gambar positif.
3. **Konversi** anotasi ke format XML (dlib) atau `.vec` (OpenCV `opencv_createsamples`).
4. **Jalankan training** dengan parameter yang sesuai.
5. **Evaluasi** di set validasi.

---

## 15. Model Resmi vs Model Sendiri

| | **Model Resmi** (bawaan OpenCV / dlib) | **Model Sendiri** |
|---|---|---|
| Objek target | Umum (wajah frontal, mata, dll.) | Spesifik kasus pakai |
| Waktu | Siap pakai | Butuh waktu kumpulkan data + training |
| Data | Sudah dilatih dari dataset besar | Harus siapkan sendiri (puluhan–ribuan gambar) |
| Akurasi domain | Baik di domain umum | Bisa lebih tinggi di domain spesifik |

**Aturan praktis**: mulai dari model resmi dulu. Hanya pindah ke model sendiri jika performa tidak cukup atau objek target tidak standar.

---

## 16. Format Dataset Latihan (XML)

dlib memakai format XML dengan struktur umum:

```xml
<?xml version='1.0' encoding='ISO-8859-1'?>
<dataset>
  <name>Training data</name>
  <images>
    <image file='positives/img001.jpg'>
      <box top='34' left='56' width='120' height='120'/>
    </image>
    <image file='positives/img002.jpg'>
      <box top='40' left='80' width='96'  height='96'/>
    </image>
    <!-- ... -->
  </images>
</dataset>
```

Yang harus dipastikan:
- Path `file=` **relatif terhadap lokasi training**.
- Nilai `top`, `left`, `width`, `height` dalam **piksel**.
- Setiap `<image>` boleh berisi **lebih dari satu** `<box>` kalau ada banyak objek di gambar yang sama.

---

## 17. Pengaturan Training

Parameter utama untuk dlib `train_simple_object_detector`:

| Parameter | Arti | Praktik umum |
|---|---|---|
| `C` | Regularization SVM (trade-off margin vs error) | `5` |
| `epsilon` | Toleransi konvergensi | `0.01` |
| `num_threads` | Jumlah thread paralel | sesuai core |
| `be_verbose` | Log progres | `True` |
| `add_left_right_image_flips` | Augmentasi flip horizontal | `True` kalau objek simetris |
| `detection_window_size` | Ukuran jendela deteksi | `80*80` atau sesuai objek |

Contoh pemakaian ringkas:

```python
import dlib

options = dlib.simple_object_detector_training_options()
options.C = 5
options.epsilon = 0.01
options.num_threads = 4
options.be_verbose = True
options.add_left_right_image_flips = True

dlib.train_simple_object_detector("train.xml", "detector.svm", options)
```

Lakukan tuning `C` berdasarkan performa di set validasi — terlalu besar bisa **overfit**, terlalu kecil **underfit**.

---

## 18. Sesi Hands-on

Persiapan:
- Python + `opencv-python` + `dlib` + `numpy`.
- Berkas `haarcascade_frontalface_default.xml` dan `shape_predictor_68_face_landmarks.dat`.
- Webcam / video sampel.
- PNG filter dengan **kanal alpha** untuk alpha blending.

Panduan ringkas:
1. **Latihan 1**: deteksi wajah dengan Haar Cascade → gambar kotak.
2. **Latihan 2**: tambahkan landmark 68 titik dari dlib → gambar titik.
3. **Latihan 3**: hitung MAR dari titik bibir → cetak status "mulut terbuka" bila `MAR > 0.6` selama N frame.
4. **Latihan 4**: pasang filter kacamata memakai titik mata → alpha blending.
5. **Latihan 5**: tambahkan filter kedua, urutkan layer dari bawah ke atas.
6. **Opsional**: kumpulkan 50–100 gambar objek, buat XML, latih detektor sendiri.

---

## Rangkuman

- Gambar = angka; video = deretan frame.
- **Detection** memberi kotak; **recognition** memberi identitas; **landmark** memberi titik-titik.
- **Haar Cascade** = fitur Haar + sliding window + cascade bertingkat pada grayscale.
- **dlib 68 titik** memetakan rahang, alis, hidung, mata, bibir.
- Dari koordinat titik → informasi geometri (MAR, EAR, posisi filter).
- **Alpha blending** memakai kanal alpha untuk menempel objek transparan.
- Model resmi dulu; model sendiri hanya kalau perlu, dengan dataset XML + `train_simple_object_detector`.

---

## Tugas (dari slide)

Lihat halaman "tugas" pada slide — rincian tugas diisi oleh asisten study group.
