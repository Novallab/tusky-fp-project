"""Tusky App 5: Nilai Mahasiswa - komponen nilai, nilai akhir, peringkat."""
from fplib import (fp_filter, fp_map, fp_reduce, fp_group_by, fp_sort, fp_sum_by,
                   fp_count_by, fp_partition, fp_find, fp_top_n, fp_compose)

BOBOT = {"tugas": 0.3, "uts": 0.3, "uas": 0.4}
NILAI_LULUS = 60
MAHASISWA = [
    {"nim": "2101", "nama": "Andi", "tugas": 85, "uts": 80, "uas": 90},
    {"nim": "2102", "nama": "Budi", "tugas": 70, "uts": 55, "uas": 60},
    {"nim": "2103", "nama": "Citra", "tugas": 95, "uts": 90, "uas": 92},
    {"nim": "2104", "nama": "Dewi", "tugas": 60, "uts": 50, "uas": 45},
    {"nim": "2105", "nama": "Eko", "tugas": 75, "uts": 72, "uas": 78},
]


def nilai_akhir(m):
    """Rata-rata berbobot dari komponen nilai."""
    return fp_reduce(BOBOT.items(), lambda total, kv: total + m[kv[0]] * kv[1], 0)


def huruf(nilai):
    batas = [(85, "A"), (75, "B"), (65, "C"), (50, "D")]
    cocok = fp_find(batas, lambda b: nilai >= b[0])
    return cocok[1] if cocok else "E"


huruf_mahasiswa = fp_compose(huruf, nilai_akhir)


def hitung_nilai(mahasiswa):
    return fp_map(mahasiswa, lambda m: {**m, "akhir": round(nilai_akhir(m), 1), "huruf": huruf_mahasiswa(m)})


def main():
    hasil = hitung_nilai(MAHASISWA)
    lulus, remedial = fp_partition(hasil, lambda m: m["akhir"] >= NILAI_LULUS)
    peringkat = fp_sort(hasil, key=lambda m: m["akhir"], reverse=True)
    rata_rata = fp_sum_by(hasil, lambda m: m["akhir"]) / len(hasil)

    print("=== TUSKY NILAI MAHASISWA ===")
    print(f"Bobot: {BOBOT}")
    print("Peringkat:")
    for urutan, m in enumerate(peringkat, start=1):
        print(f'{urutan}. {m["nama"]} - {m["akhir"]} ({m["huruf"]})')
    print("Distribusi huruf:", fp_count_by(hasil, lambda m: m["huruf"]))
    print("Mahasiswa per huruf:", {h: fp_map(ms, lambda m: m["nama"]) for h, ms in fp_group_by(hasil, lambda m: m["huruf"]).items()})
    print(f"Rata-rata kelas: {rata_rata:.1f}")
    print("Lulus:", fp_map(lulus, lambda m: m["nama"]))
    print("Perlu remedial:", fp_map(remedial, lambda m: m["nama"]))
    print("Tiga terbaik:", fp_map(fp_top_n(hasil, 3, key=lambda m: m["akhir"]), lambda m: m["nama"]))
    print("Cari NIM 2103:", fp_find(hasil, lambda m: m["nim"] == "2103"))
    print("Nilai UAS di bawah 60:", fp_map(fp_filter(hasil, lambda m: m["uas"] < 60), lambda m: m["nama"]))


if __name__ == "__main__":
    main()
