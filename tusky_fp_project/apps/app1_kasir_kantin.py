"""Tusky App 1: Kasir Kantin - menu, keranjang, total belanja."""
from fplib import (fp_filter, fp_map, fp_reduce, fp_group_by, fp_sort, fp_sum_by,
                   fp_find, fp_top_n, fp_compose, fp_format_rupiah)

MENU = [
    {"id": "M01", "nama": "Nasi Goreng", "kategori": "makanan", "harga": 15000, "tersedia": True},
    {"id": "M02", "nama": "Mie Ayam", "kategori": "makanan", "harga": 13000, "tersedia": True},
    {"id": "M03", "nama": "Es Teh", "kategori": "minuman", "harga": 4000, "tersedia": True},
    {"id": "M04", "nama": "Kopi Susu", "kategori": "minuman", "harga": 8000, "tersedia": True},
    {"id": "M05", "nama": "Gorengan", "kategori": "snack", "harga": 2000, "tersedia": True},
    {"id": "M06", "nama": "Soto Ayam", "kategori": "makanan", "harga": 14000, "tersedia": False},
]
KERANJANG = [("M01", 2), ("M03", 3), ("M05", 5), ("M04", 1), ("M99", 1)]
BATAS_DISKON = 50000


def menu_tersedia(menu):
    return fp_filter(menu, lambda item: item["tersedia"])


def baris_keranjang(menu, keranjang):
    """Ubah (id, qty) menjadi baris belanja; id yang tidak ada di menu diabaikan."""
    ditemukan = fp_map(keranjang, lambda k: (fp_find(menu_tersedia(menu), lambda m: m["id"] == k[0]), k[1]))
    valid = fp_filter(ditemukan, lambda pasangan: pasangan[0] is not None)
    return fp_map(valid, lambda p: {**p[0], "qty": p[1], "subtotal": p[0]["harga"] * p[1]})


def diskon_member(total):
    return total * 0.9 if total >= BATAS_DISKON else total


def bulatkan_ratusan(total):
    return round(total / 100) * 100


hitung_total_akhir = fp_compose(bulatkan_ratusan, diskon_member)


def main():
    baris = baris_keranjang(MENU, KERANJANG)
    subtotal = fp_sum_by(baris, lambda b: b["subtotal"])
    per_kategori = fp_group_by(baris, lambda b: b["kategori"])
    terlaris = fp_top_n(baris, 2, key=lambda b: b["qty"])
    total_item = fp_reduce(baris, lambda total, b: total + b["qty"], 0)

    print("=== TUSKY KASIR KANTIN ===")
    print("Menu tersedia:", fp_map(menu_tersedia(MENU), lambda m: m["nama"]))
    print("Struk belanja:")
    for b in fp_sort(baris, key=lambda b: b["nama"]):
        print(f'- {b["nama"]} x{b["qty"]} = {fp_format_rupiah(b["subtotal"])}')
    print("Subtotal per kategori:", {
        kat: fp_format_rupiah(fp_sum_by(items, lambda b: b["subtotal"]))
        for kat, items in per_kategori.items()})
    print("Item paling banyak dibeli:", fp_map(terlaris, lambda b: b["nama"]))
    print("Total item dibeli:", total_item)
    print("Subtotal:", fp_format_rupiah(subtotal))
    print("Total bayar (diskon member jika >= 50.000):", fp_format_rupiah(hitung_total_akhir(subtotal)))


if __name__ == "__main__":
    main()
