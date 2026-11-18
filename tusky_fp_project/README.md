# Tusky - Functional Programming Project

Proyek mata kuliah **Pemrograman Fungsional** (Informatika UMM): satu library
reusable (`fplib.py`) yang dipakai oleh lima aplikasi console.

## Struktur folder

```text
tusky_fp_project/
├── fplib.py              # library fungsi bergaya fungsional
├── test_fplib.py         # unit test (pytest)
├── cek_matriks.py        # skrip bantu: matriks fungsi x aplikasi + nomor baris
├── README.md
└── apps/
    ├── app1_kasir_kantin.py
    ├── app2_presensi_kelas.py
    ├── app3_perpustakaan_mini.py
    ├── app4_keuangan_pribadi.py
    └── app5_nilai_mahasiswa.py
```

## Cara menjalankan

Pastikan terminal berada di folder `tusky_fp_project`, lalu:

```bash
python -m apps.app1_kasir_kantin
python -m apps.app2_presensi_kelas
python -m apps.app3_perpustakaan_mini
python -m apps.app4_keuangan_pribadi
python -m apps.app5_nilai_mahasiswa
```

(di Windows boleh memakai `py -m apps.app1_kasir_kantin`, dst.)

Menjalankan test:

```bash
pip install pytest
pytest -v
```

Aplikasi tidak membutuhkan library eksternal (hanya `pytest` untuk test).
Python 3.10+ disarankan.

## Prinsip fungsional

- **Pure function**: hasil hanya bergantung pada argumen, tanpa efek samping.
- **Immutable**: koleksi input tidak pernah diubah; selalu mengembalikan nilai baru
  (diuji di `test_input_tidak_berubah`).
- **Higher-order function**: fungsi menerima fungsi lain (lambda/callback).
- **Komposisi**: fungsi kecil digabung dengan `fp_compose`.

## Daftar fungsi di fplib.py

| Fungsi | Kegunaan |
|---|---|
| `fp_filter(items, predicate)` | menyaring item yang memenuhi kondisi |
| `fp_map(items, transform)` | mengubah tiap item menjadi bentuk lain |
| `fp_reduce(items, reducer, initial)` | menggabungkan item menjadi satu nilai |
| `fp_sort(items, key, reverse)` | mengurutkan, mengembalikan salinan baru |
| `fp_group_by(items, key_func)` | mengelompokkan item berdasarkan kunci |
| `fp_sum_by(items, value_func)` | menjumlahkan nilai yang diambil dari tiap item |
| `fp_count_by(items, key_func)` | menghitung jumlah item per kunci |
| `fp_partition(items, predicate)` | memisahkan menjadi (memenuhi, tidak memenuhi) |
| `fp_find(items, predicate, default)` | mencari item pertama yang cocok |
| `fp_top_n(items, n, key, reverse)` | mengambil n item teratas |
| `fp_compose(*funcs)` | menyusun fungsi: `fp_compose(f, g)(x) == f(g(x))` |
| `fp_format_rupiah(amount)` | format angka menjadi `Rp15.000` |

## Matriks fungsi x aplikasi

Setiap fungsi dipakai oleh minimal 3 dari 5 aplikasi.

| Fungsi | Kasir | Presensi | Perpus | Keuangan | Nilai | Jumlah |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| `fp_filter` | ✓ | ✓ | ✓ | ✓ | ✓ | 5 |
| `fp_map` | ✓ | ✓ | ✓ | ✓ | ✓ | 5 |
| `fp_reduce` | ✓ | ✓ |  | ✓ | ✓ | 4 |
| `fp_sort` | ✓ | ✓ | ✓ | ✓ | ✓ | 5 |
| `fp_group_by` | ✓ | ✓ | ✓ | ✓ | ✓ | 5 |
| `fp_sum_by` | ✓ |  | ✓ | ✓ | ✓ | 4 |
| `fp_count_by` |  | ✓ | ✓ | ✓ | ✓ | 4 |
| `fp_partition` |  | ✓ | ✓ | ✓ | ✓ | 4 |
| `fp_find` | ✓ | ✓ | ✓ | ✓ | ✓ | 5 |
| `fp_top_n` | ✓ | ✓ | ✓ | ✓ | ✓ | 5 |
| `fp_compose` | ✓ |  | ✓ | ✓ | ✓ | 4 |
| `fp_format_rupiah` | ✓ |  | ✓ | ✓ |  | 3 |

Untuk bukti file dan nomor baris pemanggilan (bahan laporan), jalankan:

```bash
python cek_matriks.py
```

## Ringkasan aplikasi

| Aplikasi | Isi |
|---|---|
| Kasir Kantin | menu tersedia, keranjang, struk, subtotal per kategori, diskon member 10% jika >= Rp50.000 |
| Presensi Kelas | rekap hadir/izin/sakit/alpa, persentase per mahasiswa, syarat minimal 75% |
| Perpustakaan Mini | katalog, status tersedia/dipinjam, keterlambatan, denda Rp1.000/hari (masa pinjam 7 hari) |
| Keuangan Pribadi | pemasukan, pengeluaran, saldo, total per kategori, cek anggaran |
| Nilai Mahasiswa | bobot tugas 30% / UTS 30% / UAS 40%, nilai huruf, peringkat, remedial |

## Catatan

Data pada tiap aplikasi adalah data contoh (simulasi) agar output selalu sama.
Tanggal acuan Perpustakaan Mini dikunci ke 2026-11-18 supaya hasil denda
deterministik. Bobot nilai, batas lulus (60), dan tarif denda dapat diubah di
konstanta bagian atas masing-masing file.
