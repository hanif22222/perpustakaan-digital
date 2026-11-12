"""Fungsi validasi sederhana yang dipakai bersama oleh semua kelas model.

Setiap fungsi mengembalikan nilai yang sudah bersih, atau melempar ValueError
dengan pesan yang jelas (pesan ini bisa langsung ditampilkan di menu CLI).
"""

from datetime import date


def wajib_teks(nilai, nama_field):
    """Nilai harus berupa string yang tidak kosong. Spasi di tepi dibuang."""
    if not isinstance(nilai, str) or nilai.strip() == "":
        raise ValueError(f"{nama_field} harus berupa teks yang tidak kosong.")
    return nilai.strip()


def wajib_tahun(nilai, nama_field="Tahun terbit", minimum=1000, maksimum=2100):
    """Nilai harus bilangan bulat dalam rentang tahun yang wajar."""
    if isinstance(nilai, bool) or not isinstance(nilai, int):
        raise ValueError(f"{nama_field} harus berupa angka bulat.")
    if nilai < minimum or nilai > maksimum:
        raise ValueError(f"{nama_field} harus antara {minimum} dan {maksimum}.")
    return nilai


def wajib_tanggal(nilai, nama_field):
    """Nilai harus tanggal valid berformat YYYY-MM-DD (contoh: 2026-11-12)."""
    teks = wajib_teks(nilai, nama_field)
    if len(teks) != 10 or teks[4] != "-" or teks[7] != "-":
        raise ValueError(f"{nama_field} harus berformat YYYY-MM-DD, bukan '{teks}'.")
    try:
        date.fromisoformat(teks)
    except ValueError:
        raise ValueError(f"{nama_field} '{teks}' bukan tanggal yang valid.") from None
    return teks


def periksa_kolom(baris, kolom_wajib):
    """Memastikan satu baris CSV (dict) memuat semua kolom yang dibutuhkan."""
    for kolom in kolom_wajib:
        if kolom not in baris:
            raise ValueError(f"Kolom '{kolom}' tidak ditemukan pada baris data.")