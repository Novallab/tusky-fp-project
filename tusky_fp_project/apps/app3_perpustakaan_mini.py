"""Tusky App 3: Perpustakaan Mini - katalog, peminjaman, denda."""
from datetime import date, timedelta
from fplib import (fp_filter, fp_map, fp_group_by, fp_sort, fp_sum_by, fp_count_by,
                   fp_partition, fp_find, fp_top_n, fp_compose, fp_format_rupiah)

HARI_INI = date(2026, 11, 18)
MASA_PINJAM_HARI = 7
DENDA_PER_HARI = 1000

KATALOG = [
    {"id": "B01", "judul": "Pemrograman Python", "kategori": "teknologi"},
    {"id": "B02", "judul": "Struktur Data", "kategori": "teknologi"},
    {"id": "B03", "judul": "Laskar Pelangi", "kategori": "novel"},
    {"id": "B04", "judul": "Bumi Manusia", "kategori": "novel"},
    {"id": "B05", "judul": "Sejarah Indonesia", "kategori": "sejarah"},
]
PEMINJAMAN = [
    {"buku": "B01", "peminjam": "Andi", "pinjam": date(2026, 11, 1), "kembali": date(2026, 11, 7)},
    {"buku": "B02", "peminjam": "Budi", "pinjam": date(2026, 11, 3), "kembali": None},
    {"buku": "B03", "peminjam": "Andi", "pinjam": date(2026, 11, 10), "kembali": None},
    {"buku": "B04", "peminjam": "Citra", "pinjam": date(2026, 10, 25), "kembali": date(2026, 11, 8)},
]


def hari_terlambat(p, hari_ini=HARI_INI):
    batas = p["pinjam"] + timedelta(days=MASA_PINJAM_HARI)
    selesai = p["kembali"] or hari_ini
    return max(0, (selesai - batas).days)


def laporan_pinjam(katalog, peminjaman):
    def bentuk(p):
        buku = fp_find(katalog, lambda b: b["id"] == p["buku"])
        telat = hari_terlambat(p)
        return {**p, "judul": buku["judul"], "telat": telat, "denda": telat * DENDA_PER_HARI}
    return fp_map(peminjaman, bentuk)


def buku_tersedia(katalog, peminjaman):
    sedang_dipinjam = fp_map(fp_filter(peminjaman, lambda p: p["kembali"] is None), lambda p: p["buku"])
    return fp_partition(katalog, lambda b: b["id"] not in sedang_dipinjam)


total_denda_rupiah = fp_compose(fp_format_rupiah, lambda laporan: fp_sum_by(laporan, lambda l: l["denda"]))


def main():
    laporan = laporan_pinjam(KATALOG, PEMINJAMAN)
    tersedia, dipinjam = buku_tersedia(KATALOG, PEMINJAMAN)
    terlambat = fp_filter(laporan, lambda l: l["telat"] > 0)
    per_peminjam = fp_group_by(laporan, lambda l: l["peminjam"])

    print("=== TUSKY PERPUSTAKAAN MINI ===")
    print("Tanggal acuan:", HARI_INI.isoformat())
    print("Katalog per kategori:", fp_count_by(KATALOG, lambda b: b["kategori"]))
    print("Buku tersedia:", fp_map(tersedia, lambda b: b["judul"]))
    print("Buku sedang dipinjam:", fp_map(dipinjam, lambda b: b["judul"]))
    print("Peminjaman terlambat:")
    for l in fp_sort(terlambat, key=lambda l: l["denda"], reverse=True):
        print(f'- {l["peminjam"]} | {l["judul"]} | telat {l["telat"]} hari | denda {fp_format_rupiah(l["denda"])}')
    print("Denda per peminjam:", {n: fp_format_rupiah(fp_sum_by(ls, lambda l: l["denda"]))
                                  for n, ls in per_peminjam.items()})
    print("Denda terbesar:", fp_map(fp_top_n(laporan, 1, key=lambda l: l["denda"]), lambda l: l["peminjam"]))
    print("Total denda:", total_denda_rupiah(laporan))


if __name__ == "__main__":
    main()
