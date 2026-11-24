# Modul 4 — Study Group IMV
## Deep Learning & Object Detection (CNN + YOLO)
---
## Daftar Isi

1. [Deep Learning & Object Detection: Pengantar](#1-deep-learning--object-detection-pengantar)
2. [CV Konvensional vs Deep Learning](#2-cv-konvensional-vs-deep-learning)
3. [Alur Kerja CV Konvensional](#3-alur-kerja-cv-konvensional)
4. [Perbandingan Teknis: Konvensional vs DL](#4-perbandingan-teknis-konvensional-vs-dl)
5. [Kapan Memakai Mana?](#5-kapan-memakai-mana)
6. [Struktur Lapisan Neural Network](#6-struktur-lapisan-neural-network)
7. [Arsitektur CNN](#7-arsitektur-cnn)
8. [Mekanisme Operasi Konvolusi (Kernel & Filter)](#8-mekanisme-operasi-konvolusi-kernel--filter)
9. [Max Pooling & Hierarki Fitur](#9-max-pooling--hierarki-fitur)
10. [Arsitektur Populer DL untuk CV](#10-arsitektur-populer-dl-untuk-cv)
11. [Peran Computer Vision](#11-peran-computer-vision)
12. [Cara Kerja Object Detection](#12-cara-kerja-object-detection)
13. [Pengenalan YOLO & Bounding Box](#13-pengenalan-yolo--bounding-box)
14. [Evaluasi Bounding Box: IoU & NMS](#14-evaluasi-bounding-box-iou--nms)
15. [Siklus Hidup Pengembangan Model](#15-siklus-hidup-pengembangan-model)
16. [Pembagian Dataset & Augmentasi](#16-pembagian-dataset--augmentasi)
17. [Fine-Tuning Model Pretrained](#17-fine-tuning-model-pretrained)
18. [Feature Extraction vs Full Fine-Tuning](#18-feature-extraction-vs-full-fine-tuning)

---

## 1. Deep Learning & Object Detection: Pengantar

Modul ini menutup rangkaian IMV: dari filter manual (Modul 1) → face detection klasik (Modul 2) → ke **Deep Learning end-to-end** di modul ini.

Tema utama:
- Arsitektur **CNN** (Convolutional Neural Network).
- Deteksi objek **YOLO** (real-time, single-shot).
- Alur **pelatihan data**: kurasi → label → train → inferensi.
- Strategi **fine-tuning** model pretrained.

---

## 2. CV Konvensional vs Deep Learning

- **CV Konvensional:** ekstraksi fitur **manual** memakai algoritma seperti **SIFT**, **HOG**, atau **Canny edge** (lihat Modul 1 untuk Canny).
- **Deep Learning:** jaringan saraf **mempelajari hierarki fitur visual otomatis** langsung dari **piksel mentah**. Tidak ada feature engineering manual.

Perbedaan filosofis: di konvensional **manusia** memutuskan "fitur apa yang penting"; di DL **model** yang memutuskan dari data.

---

## 3. Alur Kerja CV Konvensional

Tiga tahap tipikal:

1. **Image Pre-Processing** — Gaussian blur, Canny edge, transformasi skala.
2. **Feature Extraction** — titik kunci manual: **SIFT**, **SURF**, **HOG**.
3. **Feature Matching** — pencocokan pola via **FLANN** atau **RANSAC**.

Arsitektur ini dipakai sebelum DL dominan; masih relevan untuk kasus data terbatas dan perangkat hemat daya.

---

## 4. Perbandingan Teknis: Konvensional vs DL

| Aspek Kunci | **Konvensional** | **Deep Learning** |
|---|---|---|
| **Feature Engineering** | Fitur dirancang manual oleh user | Fitur dipelajari otomatis end-to-end |
| **Kebutuhan Data** | Efektif pada dataset terbatas | Butuh dataset besar berlabel |
| **Interpretabilitas** | Transparan dan mudah ditelusuri | Cenderung bersifat **black box** |
| **Fleksibilitas & Adaptasi** | Terbatas untuk tugas spesifik | Adaptif pada berbagai tugas baru |
| **Contoh Algoritma** | SIFT, SURF, HOG, Canny Edge | CNN, ResNet, YOLO, Vision Transformer |

---

## 5. Kapan Memakai Mana?

### Pakai CV Konvensional jika:
- **Data terbatas**: sampel gambar berlabel sangat sedikit.
- **Perangkat hemat daya**: mikrokontroler **tanpa akselerasi GPU**.
- **Aturan geometris jelas**: inspeksi dimensi, warna, atau **kode batang**.

### Pakai Deep Learning jika:
- **Variasi kompleks**: perubahan **pencahayaan**, **sudut pandang**, **skala**, dan **oklusi** objek.
- **Skala data besar**: **ribuan** gambar tersedia untuk ditrain.
- **Pemahaman semantik**: pengenalan wajah, **kendaraan otonom**, **medis**.

Aturan praktis: coba konvensional dulu kalau data terbatas dan aturan jelas; pindah ke DL saat variasi domain mulai memukul akurasi.

---

## 6. Struktur Lapisan Neural Network

Setiap jaringan saraf dibagi menjadi tiga blok fungsional:

### Input Layer
Menerima **nilai intensitas piksel mentah** dari gambar.

### Hidden Layers & Backpropagation
Menyesuaikan **bobot koneksi** antar-neuron untuk **meminimalkan error prediksi**. Algoritma pelatihan standar: **backpropagation** + optimisasi gradien (SGD, Adam, dst.).

### Output Layer
Menghasilkan **skor probabilitas klasifikasi akhir** (misal: via softmax).

---

## 7. Arsitektur CNN

**CNN** disusun dari tiga jenis lapisan berurutan:

### Convolution Layer
**Filter geser** mendeteksi **tepi**, **tekstur**, dan **sudut**. Ini adalah operasi konvolusi 2D yang sama secara matematis dengan konvolusi di Modul 1, hanya saja **kernelnya dipelajari lewat training**, bukan ditentukan manual.

### Pooling Layer
**Kompresi dimensi spasial** untuk efisiensi komputasi. Mengurangi ukuran feature map sambil mempertahankan informasi dominan.

### Fully Connected Layer
**Klasifikasi akhir** berdasarkan fitur visual yang sudah terkompilasi di lapisan sebelumnya. Keluaran biasanya masuk ke softmax untuk probabilitas kelas.

Alur umum CNN klasifikasi:

```
Image → [Conv → ReLU → Pool] × N → Flatten → FC → Softmax → Kelas
```

---

## 8. Mekanisme Operasi Konvolusi (Kernel & Filter)

### Kernel / Filter
Matriks bobot kecil berukuran **3×3** atau **5×5** yang **bergeser melintasi piksel gambar (stride)** untuk **perkalian elemen** (element-wise multiply + sum).

### Feature Map & Aktivasi ReLU
Hasil konvolusi disebut **feature map**. Nilai tiap pikselnya menyoroti **lokasi pola spesifik** seperti **garis vertikal**, **lengkungan**, atau **tekstur** objek.

Setelah konvolusi, dipasang fungsi aktivasi **ReLU**:

```
ReLU(x) = max(0, x)
```

ReLU membuang nilai negatif, memperkenalkan non-linearitas, dan membantu training lebih cepat (gradien stabil pada x > 0).

---

## 9. Max Pooling & Hierarki Fitur

### Max Pooling (Downsampling)
Mengambil **nilai aktivasi tertinggi** di tiap **jendela 2×2** untuk **mengurangi ukuran peta fitur hingga 75%** (karena 2×2 → 1 nilai berarti sisa 25% dari jumlah piksel).

Efek: representasi lebih ringkas, tahan sedikit translasi, dan komputasi di layer berikutnya lebih murah.

### Hierarki Fitur Berlapis
- **Layer awal**: menangkap **tepi dasar** (horizontal, vertikal, diagonal).
- **Layer tengah**: mengenali **bentuk** (lingkaran, pola tekstur kompleks).
- **Layer akhir**: mengenali **objek utuh** (wajah, mobil, angka).

Hierarki ini **tidak dirancang manual** — muncul otomatis dari training.

---

## 10. Arsitektur Populer DL untuk CV

### AlexNet (2012)
**Pelopor pelatihan GPU**, pemakaian aktivasi **ReLU**, dan teknik **dropout**. Pemenang ImageNet 2012 yang memicu ledakan DL di CV.

### VGG-16 / VGG-19
**Tumpukan filter konvolusi kecil 3×3** untuk kedalaman fitur. Sederhana dan sering jadi backbone untuk transfer learning.

### YOLO (Real-Time)
**Deteksi grid single-shot berkecepatan tinggi.** Dirancang untuk inferensi real-time (video, kamera, robotika).

---

## 11. Peran Computer Vision

Tiga tugas inti CV:

| Tugas | Keluaran |
|---|---|
| **Image Classification** | **Satu label kategori** untuk keseluruhan citra |
| **Object Detection** | **Jenis + lokasi** objek via **bounding box** |
| **Image Segmentation** | **Label kategori hingga tingkat setiap piksel** |

Tingkat granularitas naik dari atas ke bawah: classification < detection < segmentation.

---

## 12. Cara Kerja Object Detection

Object detection menggabungkan dua tugas sekaligus dalam satu model:
1. **Klasifikasi**: jenis objek apa?
2. **Lokalisasi**: di mana objek itu, berupa **bounding box** `(x, y, w, h)`.

Keluaran per objek: `(kelas, x, y, w, h, confidence)`.

---

## 13. Pengenalan YOLO & Bounding Box

### You Only Look Once (Single-Stage)
YOLO **membagi gambar menjadi grid S×S** dalam **sekali lintasan jaringan** untuk **deteksi real-time**. Beda dengan arsitektur dua tahap (R-CNN) yang terpisah region proposal dan klasifikasi.

### Parameter Bounding Box
Tiap sel grid memprediksi:
- **Titik tengah** `(x, y)`
- **Lebar** `w`, **tinggi** `h`
- **Skor kepercayaan** `confidence` (seberapa yakin ada objek + seberapa cocok kotaknya).

---

## 14. Evaluasi Bounding Box: IoU & NMS

### Intersection over Union (IoU)

Rasio **luas irisan** dibanding **luas gabungan** kotak prediksi dan **ground-truth**:

```
IoU = Area(Prediksi ∩ Ground-Truth) / Area(Prediksi ∪ Ground-Truth)
```

**Threshold IoU ≥ 0.5** umum dipakai untuk menyatakan prediksi "benar".

### Non-Max Suppression (NMS)

**Memilih kotak dengan skor confidence tertinggi** dan **membuang duplikat bertumpuk**. Algoritma:
1. Urutkan kotak berdasarkan confidence turun.
2. Ambil kotak teratas → simpan.
3. Buang kotak lain yang IoU-nya terhadap kotak itu melebihi ambang (mis. `0.5`).
4. Ulangi sampai list kosong.

Hasil: satu kotak bersih per objek.

---

## 15. Siklus Hidup Pengembangan Model

Empat fase:

1. **Dataset Kurasi** — koleksi **citra beragam** dibagi ke set **train, validation, dan test**.
2. **Data Labeling** — **anotasi koordinat ground-truth bounding box** secara presisi.
3. **Model Training** — **optimasi bobot** melalui **backpropagation** untuk **meminimalkan loss**.
4. **Model Inference** — **prediksi objek cepat** pada gambar baru di **lingkungan produksi**.

---

## 16. Pembagian Dataset & Augmentasi

### Proporsi Train / Val / Test — **70 : 15 : 15**

Tujuan: **mencegah overfitting** dan **mengukur kemampuan generalisasi** model pada **data tak terlihat**.

- **Train (70%)** — model belajar dari sini.
- **Val (15%)** — tuning hyperparameter, pilih checkpoint terbaik.
- **Test (15%)** — evaluasi akhir sekali, **tidak boleh** dipakai untuk tuning.

### Data Augmentation

Teknik untuk **memperkaya keragaman data latih** tanpa mengumpulkan gambar baru:
- **Rotasi**
- **Flipping** (horizontal / vertical)
- **Cropping**
- **Variasi kecerahan**

Augmentasi membuat model lebih tahan terhadap variasi orientasi, posisi, dan pencahayaan.

---

## 17. Fine-Tuning Model Pretrained

Ide: pakai model yang sudah dilatih dari dataset besar (**COCO**, **ImageNet**), lalu adaptasi ke kelas target dengan sedikit data.

### Freeze Backbone Layers
**Mempertahankan bobot ekstraktor fitur awal** yang sudah terlatih dari dataset COCO atau ImageNet. Layer-layer ini sudah tahu tepi, tekstur, bentuk umum — tidak perlu diubah.

### Adaptasi Detection Head
**Melatih ulang lapisan akhir** memakai **learning rate kecil** untuk **kelas target spesifik**. Hanya kepala (head) yang berubah.

Keuntungan: **butuh data jauh lebih sedikit** dan **training jauh lebih cepat** daripada melatih dari nol.

---

## 18. Feature Extraction vs Full Fine-Tuning

| Strategi | Yang dilatih | Kapan dipakai |
|---|---|---|
| **Feature Extraction** (**Bekukan Semua**) | Hanya **classifier akhir** | Dataset baru **kecil** dan **mirip domain asal** |
| **Unfreeze Sebagian / Penuh** | Membuka **blok konvolusi atas** agar fitur beradaptasi | Domain spesifik yang **berbeda** dari pretrained (contoh: **citra medis**) |

Aturan praktis:
- Dataset mirip ImageNet, kecil → **feature extraction**.
- Dataset beda domain (medis, satelit, radar) → **unfreeze sebagian / penuh** dengan **learning rate kecil**.

---

## Rangkuman

- CV konvensional = fitur manual; DL = fitur otomatis end-to-end.
- CNN = Conv + Pool + FC. Kernel dipelajari, bukan dirancang.
- Max pooling mengecilkan feature map 75% per 2×2.
- Hierarki fitur: tepi → bentuk → objek, muncul otomatis.
- YOLO = single-shot, grid S×S, output `(x, y, w, h, confidence)`.
- IoU ≥ 0.5 standar; NMS buang duplikat bertumpuk.
- Siklus: kurasi → label → train → inferensi.
- Split 70:15:15; augmentasi untuk tahan variasi.
- Fine-tuning: freeze backbone, latih head; unfreeze lebih dalam kalau domain berbeda.

---

## Sesi Hands-on

Lihat halaman "SESI HANDS-ON" pada slide — detail diisi oleh asisten study group. Umumnya meliputi:
- Setup **Ultralytics YOLOv8** (`pip install ultralytics`).
- Buat dataset dalam format YOLO (`.txt` label per gambar, `data.yaml`).
- Jalankan training: `yolo detect train data=data.yaml model=yolov8n.pt epochs=50 imgsz=640`.
- Inferensi: `yolo detect predict model=runs/detect/train/weights/best.pt source=test.jpg`.
- Eksperimen fine-tuning: bandingkan freeze backbone vs unfreeze.
