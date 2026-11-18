"""Tusky App 2: Presensi Kelas - kehadiran dan rekap per mahasiswa."""
from fplib import (fp_filter, fp_map, fp_reduce, fp_group_by, fp_sort, fp_count_by,
                   fp_partition, fp_find, fp_top_n)

MAHASISWA = {"2101": "Andi", "2102": "Budi", "2103": "Citra", "2104": "Dewi", "2105": "Eko"}
# (nim, pertemuan, status)
DATA_MENTAH = [
    ("2101", 1, "hadir"), ("2101", 2, "hadir"), ("2101", 3, "hadir"), ("2101", 4, "hadir"),
    ("2102", 1, "hadir"), ("2102", 2, "alpa"), ("2102", 3, "hadir"), ("2102", 4, "izin"),
    ("2103", 1, "hadir"), ("2103", 2, "hadir"), ("2103", 3, "sakit"), ("2103", 4, "hadir"),
    ("2104", 1, "alpa"), ("2104", 2, "alpa"), ("2104", 3, "hadir"), ("2104", 4, "izin"),
    ("2105", 1, "hadir"), ("2105", 2, "hadir"), ("2105", 3, "hadir"), ("2105", 4, "sakit"),
]
MIN_PERSEN = 75


def buat_record(baris):
    nim, pertemuan, status = baris
    return {"nim": nim, "nama": MAHASISWA[nim], "pertemuan": pertemuan, "status": status}


def rekap_mahasiswa(records):
    """Rekap per mahasiswa: jumlah hadir, total pertemuan, dan persentase."""
    def rekap(pasangan):
        nim, items = pasangan
        hadir = len(fp_filter(items, lambda r: r["status"] == "hadir"))
        return {"nim": nim, "nama": items[0]["nama"], "hadir": hadir,
                "total": len(items), "persen": hadir / len(items) * 100}
    return fp_map(list(fp_group_by(records, lambda r: r["nim"]).items()), rekap)


def main():
    records = fp_map(DATA_MENTAH, buat_record)
    rekap = rekap_mahasiswa(records)
    memenuhi, tidak = fp_partition(rekap, lambda r: r["persen"] >= MIN_PERSEN)
    pertemuan_2 = fp_filter(records, lambda r: r["pertemuan"] == 2)
    tidak_hadir_p2 = fp_filter(pertemuan_2, lambda r: r["status"] != "hadir")
    total_hadir = fp_reduce(rekap, lambda total, r: total + r["hadir"], 0)
    total_slot = fp_reduce(rekap, lambda total, r: total + r["total"], 0)

    print("=== TUSKY PRESENSI KELAS ===")
    print("Jumlah per status:", fp_count_by(records, lambda r: r["status"]))
    print(f"Kehadiran kelas keseluruhan: {total_hadir}/{total_slot} ({total_hadir / total_slot * 100:.0f}%)")
    print("Rekap kehadiran:")
    for r in fp_sort(rekap, key=lambda r: r["persen"], reverse=True):
        print(f'- {r["nama"]}: {r["hadir"]}/{r["total"]} ({r["persen"]:.0f}%)')
    print(f"Memenuhi syarat (>= {MIN_PERSEN}%):", fp_map(memenuhi, lambda r: r["nama"]))
    print("Tidak memenuhi syarat:", fp_map(tidak, lambda r: r["nama"]))
    print("Tidak hadir di pertemuan 2:", fp_map(tidak_hadir_p2, lambda r: f'{r["nama"]} ({r["status"]})'))
    print("Kehadiran terbaik:", fp_map(fp_top_n(rekap, 2, key=lambda r: r["persen"]), lambda r: r["nama"]))
    detail = fp_find(rekap, lambda r: r["nim"] == "2104")
    print("Detail NIM 2104:", detail)


if __name__ == "__main__":
    main()
