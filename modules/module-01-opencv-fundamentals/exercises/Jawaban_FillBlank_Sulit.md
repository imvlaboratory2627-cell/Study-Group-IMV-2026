# Kunci jawaban fill in the blank (sulit)

Blank [3], [4], serta ukuran kernel dan sigma boleh berbeda selama hasilnya baik.

| No | Jawaban |
|---|---|
| 1 | `cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)` |
| 2 | `np.percentile(piksel, [5, 50, 95], axis=0)` |
| 3 | `[35, 50, 50]` |
| 4 | `[85, 255, 255]` |
| 5 | `cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)` |
| 6 | `cv2.inRange(citra_hsv, lo, hi)` |
| 7 | `cv2.inRange(citra_hsv, lo, np.array([179, hi[1], hi[2]]))` |
| 8 | `cv2.inRange(citra_hsv, np.array([0, lo[1], lo[2]]), hi)` |
| 9 | `cv2.bitwise_or(atas, bawah)` |
| 10 | `np.mean(potong(m, roi['latar']) == 255)` |
| 11 | `np.mean(potong(m, roi['subjek']) == 0)` |
| 12 | `np.percentile(piksel, [1, 99], axis=0)` |
| 13 | `cv2.connectedComponentsWithStats(cv2.bitwise_not(m), connectivity=8)` |
| 14 | `stat[1:, cv2.CC_STAT_AREA]` |
| 15 | `np.where(np.isin(label, simpan), 0, 255)` |
| 16 | `cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)` |
| 17 | `cv2.bitwise_not(mask_bg)` |
| 18 | `cv2.bitwise_and(frame, frame, mask=mask_subjek)` |
| 19 | `cv2.bitwise_and(bg, bg, mask=mask_bg)` |
| 20 | `cv2.add(fg, bg_cut)` |
| 21 | `(m, cv2.bitwise_not(m))` |
| 22 | `cv2.connectedComponentsWithStats(biner, connectivity=8)` |
| 23 | `stats[1:, cv2.CC_STAT_AREA]` |
| 24 | `np.sum(luas < luas_maks)` |
| 25 | `cv2.medianBlur(mask, 5)` |
| 26 | `(m == 255).astype(np.float32)` |
| 27 | `cv2.boxFilter` |
| 28 | `False` |
| 29 | `cv2.BORDER_REPLICATE` |
| 30 | `jumlah > (k * k) // 2` |
| 31 | `cv2.connectedComponentsWithStats(cv2.bitwise_not(mask_median), connectivity=8)` |
| 32 | `1 + np.argmax(stat[1:, cv2.CC_STAT_AREA])` |
| 33 | `stat[utama, cv2.CC_STAT_TOP]` |
| 34 | `(7, 7)` |
| 35 | `1.5` |
| 36 | `cv2.GaussianBlur(mask_bg, ksize, sigma)` |
| 37 | `1.0 - halus.astype(np.float32) / 255.0` |
| 38 | `alpha[..., None]` |
| 39 | `alpha * subjek.astype(np.float32) + (1.0 - alpha) * bg.astype(np.float32)` |
| 40 | `np.clip(np.rint(campur), 0, 255).astype(np.uint8)` |
| 41 | `[hasil_dasar, hasil_median, hasil_feather]` |
| 42 | `[rgb(a) for a in daftar] + [rgb(a[y0:y1, x0:x1]) for a in daftar]` |
| 43 | `cv2.dilate(mask_median, k_pita) != cv2.erode(mask_median, k_pita)` |
| 44 | `np.abs(hasil_feather.astype(np.float32) - hasil_median.astype(np.float32))` |
| 45 | `('di pita tepi ', pita), ('di luar pita ', ~pita)` |
| 46 | `buat_alpha(mask_median, (0, 0), s)` |
| 47 | `cv2.Canny(mask, 50, 150)` |
| 48 | `cv2.bitwise_not(mask_bg)` |
| 49 | `cv2.findContours(subjek, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)` |
| 50 | `max(kontur, key=cv2.contourArea)` |
| 51 | `cv2.approxPolyDP(utama, 2.0, True)` |
| 52 | `cv2.arcLength(utama, True) / keliling` |
| 53 | `np.count_nonzero(e)` |
| 54 | `kekasaran(m)` |
