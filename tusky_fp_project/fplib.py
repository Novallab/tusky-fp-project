"""
fplib.py
Library fungsi umum bergaya fungsional untuk proyek Tusky.

Prinsip yang dipakai di seluruh library:
- Pure function: hasil hanya bergantung pada argumen, tanpa efek samping.
- Immutable: koleksi input tidak pernah diubah, selalu mengembalikan nilai baru.
- Higher-order function: fungsi menerima fungsi lain (lambda/callback).
"""
from functools import reduce
from typing import Any, Callable, Iterable, Optional, TypeVar

T = TypeVar("T")
U = TypeVar("U")
K = TypeVar("K")


def fp_filter(items: Iterable[T], predicate: Callable[[T], bool]) -> list[T]:
    """Ambil item yang memenuhi predicate."""
    return list(filter(predicate, items))


def fp_map(items: Iterable[T], transform: Callable[[T], U]) -> list[U]:
    """Ubah setiap item dengan transform, kembalikan list baru."""
    return list(map(transform, items))


def fp_reduce(items: Iterable[T], reducer: Callable[[U, T], U], initial: U) -> U:
    """Gabungkan seluruh item menjadi satu nilai akumulasi."""
    return reduce(reducer, items, initial)


def fp_sort(items: Iterable[T], key: Callable[[T], Any], reverse: bool = False) -> list[T]:
    """Kembalikan salinan item yang sudah diurutkan."""
    return sorted(items, key=key, reverse=reverse)


def fp_group_by(items: Iterable[T], key_func: Callable[[T], K]) -> dict[K, list[T]]:
    """Kelompokkan item berdasarkan kunci tanpa mengubah input."""
    def add_group(groups: dict[K, list[T]], item: T) -> dict[K, list[T]]:
        key = key_func(item)
        return {**groups, key: groups.get(key, []) + [item]}
    return fp_reduce(items, add_group, {})


def fp_sum_by(items: Iterable[T], value_func: Callable[[T], float]) -> float:
    """Jumlahkan nilai yang diambil dari tiap item (0 jika kosong)."""
    return fp_reduce(items, lambda total, item: total + value_func(item), 0)


def fp_count_by(items: Iterable[T], key_func: Callable[[T], K]) -> dict[K, int]:
    """Hitung banyaknya item untuk tiap kunci."""
    return {key: len(group) for key, group in fp_group_by(items, key_func).items()}


def fp_partition(items: Iterable[T], predicate: Callable[[T], bool]) -> tuple[list[T], list[T]]:
    """Pisahkan item menjadi (memenuhi, tidak memenuhi) predicate."""
    materialized = list(items)
    return (
        fp_filter(materialized, predicate),
        fp_filter(materialized, lambda item: not predicate(item)),
    )


def fp_find(items: Iterable[T], predicate: Callable[[T], bool],
            default: Optional[T] = None) -> Optional[T]:
    """Kembalikan item pertama yang memenuhi predicate, atau default."""
    return next(iter(fp_filter(items, predicate)), default)


def fp_top_n(items: Iterable[T], n: int, key: Callable[[T], Any], reverse: bool = True) -> list[T]:
    """Ambil n item teratas menurut key (default: nilai terbesar)."""
    return fp_sort(items, key=key, reverse=reverse)[:n]


def fp_compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Susun fungsi secara matematis: fp_compose(f, g)(x) == f(g(x))."""
    return lambda value: fp_reduce(reversed(funcs), lambda acc, func: func(acc), value)


def fp_format_rupiah(amount: float) -> str:
    """Format angka menjadi teks Rupiah, contoh 15000 -> 'Rp15.000'."""
    sign = "-" if amount < 0 else ""
    return f"{sign}Rp{abs(round(amount)):,}".replace(",", ".")
