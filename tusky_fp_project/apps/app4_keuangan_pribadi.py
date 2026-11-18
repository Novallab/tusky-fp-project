"""Tusky App 4: Keuangan Pribadi - pemasukan, pengeluaran, kategori."""
from fplib import (fp_filter, fp_map, fp_reduce, fp_group_by, fp_sort, fp_sum_by, fp_count_by,
                   fp_partition, fp_find, fp_top_n, fp_compose, fp_format_rupiah)

TRANSAKSI = [
    {"tanggal": "2026-11-01", "jenis": "masuk", "kategori": "uang saku", "jumlah": 2000000},
    {"tanggal": "2026-11-03", "jenis": "keluar", "kategori": "makan", "jumlah": 350000},
    {"tanggal": "2026-11-05", "jenis": "keluar", "kategori": "transport", "jumlah": 120000},
    {"tanggal": "2026-11-08", "jenis": "masuk", "kategori": "freelance", "jumlah": 500000},
    {"tanggal": "2026-11-10", "jenis": "keluar", "kategori": "hiburan", "jumlah": 200000},
    {"tanggal": "2026-11-12", "jenis": "keluar", "kategori": "makan", "jumlah": 300000},
    {"tanggal": "2026-11-15", "jenis": "keluar", "kategori": "kuota", "jumlah": 100000},
]
ANGGARAN = [
    {"kategori": "makan", "batas": 600000},
    {"kategori": "transport", "batas": 150000},
    {"kategori": "hiburan", "batas": 150000},
    {"kategori": "kuota", "batas": 100000},
]


def total_per_kategori(transaksi):
    """Daftar {kategori, total} dari transaksi yang diberikan."""
    return fp_map(list(fp_group_by(transaksi, lambda t: t["kategori"]).items()),
                  lambda pasangan: {"kategori": pasangan[0],
                                    "total": fp_sum_by(pasangan[1], lambda t: t["jumlah"])})


def cek_anggaran(rekap, anggaran):
    def periksa(r):
        batas = fp_find(anggaran, lambda a: a["kategori"] == r["kategori"])
        return {**r, "batas": batas["batas"] if batas else None,
                "melebihi": bool(batas) and r["total"] > batas["batas"]}
    return fp_map(rekap, periksa)


total_rupiah = fp_compose(fp_format_rupiah, lambda items: fp_sum_by(items, lambda t: t["jumlah"]))


def main():
    masuk, keluar = fp_partition(TRANSAKSI, lambda t: t["jenis"] == "masuk")
    rekap = total_per_kategori(keluar)
    hasil_anggaran = cek_anggaran(rekap, ANGGARAN)
    saldo = fp_reduce(TRANSAKSI, lambda s, t: s + t["jumlah"] if t["jenis"] == "masuk" else s - t["jumlah"], 0)
    besar = fp_filter(keluar, lambda t: t["jumlah"] >= 300000)

    print("=== TUSKY KEUANGAN PRIBADI ===")
    print("Jumlah transaksi:", fp_count_by(TRANSAKSI, lambda t: t["jenis"]))
    print("Total pemasukan:", total_rupiah(masuk))
    print("Total pengeluaran:", total_rupiah(keluar))
    print("Saldo akhir:", fp_format_rupiah(saldo))
    print("Pengeluaran per kategori (terbesar dulu):")
    for r in fp_sort(hasil_anggaran, key=lambda r: r["total"], reverse=True):
        status = "MELEBIHI ANGGARAN" if r["melebihi"] else "aman"
        print(f'- {r["kategori"]}: {fp_format_rupiah(r["total"])} / {fp_format_rupiah(r["batas"])} -> {status}')
    print("Tiga kategori terboros:", fp_map(fp_top_n(rekap, 3, key=lambda r: r["total"]), lambda r: r["kategori"]))
    print("Pengeluaran besar (>= Rp300.000):", fp_map(besar, lambda t: f'{t["tanggal"]} {t["kategori"]}'))


if __name__ == "__main__":
    main()
