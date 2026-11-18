"""Unit test untuk fplib.py. Jalankan dengan: pytest -v"""
import copy
from fplib import (fp_filter, fp_map, fp_reduce, fp_sort, fp_group_by, fp_sum_by,
                   fp_count_by, fp_partition, fp_find, fp_top_n, fp_compose,
                   fp_format_rupiah)

DATA = [
    {"nama": "a", "kat": "x", "nilai": 3},
    {"nama": "b", "kat": "y", "nilai": 1},
    {"nama": "c", "kat": "x", "nilai": 2},
]


def test_filter():
    assert fp_filter([1, 2, 3, 4], lambda n: n % 2 == 0) == [2, 4]
    assert fp_filter([], lambda n: True) == []


def test_map():
    assert fp_map([1, 2, 3], lambda n: n * 2) == [2, 4, 6]
    assert fp_map([], str) == []


def test_reduce():
    assert fp_reduce([1, 2, 3, 4], lambda a, b: a + b, 0) == 10
    assert fp_reduce([], lambda a, b: a + b, 99) == 99


def test_sort_dan_reverse():
    assert fp_sort(DATA, key=lambda d: d["nilai"]) == [DATA[1], DATA[2], DATA[0]]
    assert [d["nilai"] for d in fp_sort(DATA, key=lambda d: d["nilai"], reverse=True)] == [3, 2, 1]


def test_group_by():
    hasil = fp_group_by(DATA, lambda d: d["kat"])
    assert set(hasil) == {"x", "y"}
    assert [d["nama"] for d in hasil["x"]] == ["a", "c"]


def test_sum_by():
    assert fp_sum_by(DATA, lambda d: d["nilai"]) == 6
    assert fp_sum_by([], lambda d: d) == 0


def test_count_by():
    assert fp_count_by(DATA, lambda d: d["kat"]) == {"x": 2, "y": 1}


def test_partition():
    genap, ganjil = fp_partition([1, 2, 3, 4, 5], lambda n: n % 2 == 0)
    assert genap == [2, 4]
    assert ganjil == [1, 3, 5]


def test_find():
    assert fp_find(DATA, lambda d: d["nama"] == "b") == DATA[1]
    assert fp_find(DATA, lambda d: d["nama"] == "z") is None
    assert fp_find(DATA, lambda d: d["nama"] == "z", default="kosong") == "kosong"


def test_top_n():
    assert [d["nama"] for d in fp_top_n(DATA, 2, key=lambda d: d["nilai"])] == ["a", "c"]
    assert [d["nama"] for d in fp_top_n(DATA, 1, key=lambda d: d["nilai"], reverse=False)] == ["b"]


def test_compose_urutan_kanan_ke_kiri():
    tambah_satu = lambda n: n + 1
    kali_dua = lambda n: n * 2
    assert fp_compose(tambah_satu, kali_dua)(5) == 11   # tambah_satu(kali_dua(5))
    assert fp_compose(kali_dua, tambah_satu)(5) == 12   # kali_dua(tambah_satu(5))
    assert fp_compose()(7) == 7


def test_format_rupiah():
    assert fp_format_rupiah(0) == "Rp0"
    assert fp_format_rupiah(15000) == "Rp15.000"
    assert fp_format_rupiah(1250000) == "Rp1.250.000"
    assert fp_format_rupiah(-5000) == "-Rp5.000"


def test_input_tidak_berubah():
    asli = copy.deepcopy(DATA)
    fp_filter(DATA, lambda d: d["nilai"] > 1)
    fp_map(DATA, lambda d: d["nilai"])
    fp_sort(DATA, key=lambda d: d["nilai"])
    fp_group_by(DATA, lambda d: d["kat"])
    fp_partition(DATA, lambda d: d["nilai"] > 1)
    fp_top_n(DATA, 2, key=lambda d: d["nilai"])
    assert DATA == asli
