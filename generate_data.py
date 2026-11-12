"""Generator data simulasi untuk PENGUKURAN KINERJA (benchmark).

Data demo 100 record sudah dibuat manual (data/buku.csv dst). File ini membuat
data tambahan dengan ukuran lebih besar (default 100, 1.000, 10.000 record) dengan
kolom yang SAMA dengan data demo, sehingga bisa dimuat lewat kelas model.

Semua data fiktif (nama, kontak, ID). Hasil selalu sama selama seed sama.

Contoh:
    python generate_data.py                      # ukuran 100, 1000, 10000 -> data/bench/
    python generate_data.py --ukuran 5000        # satu ukuran saja
    python generate_data.py --seed 7 --out data/bench7

Catatan: ID dibuat berurutan (B0001, B0002, ...). Jika dimasukkan ke BST sesuai urutan,
pohon menjadi miring (skewed). Untuk kasus rata-rata, acak urutannya di benchmark.py
dengan random.Random(42).shuffle(...).
"""

import argparse
import csv
import os
import random
from datetime import date, timedelta

from models.anggota import Anggota
from models.buku import Buku
from models.transaksi import Transaksi

KATEGORI_RAK = (("Novel", "RAK-NOV"), ("Komik", "RAK-KOM"), ("Sejarah", "RAK-SEJ"),
                ("Jurnal", "RAK-JUR"), ("Ilmu Pengetahuan", "RAK-ILM"))
PROPORSI_DIPINJAM = 0.15
TANGGAL_AWAL = date(2026, 1, 1)
TANGGAL_AKHIR = date(2026, 11, 10)


def lebar(n):
    """Jumlah digit ID: minimal 3 (B001), bertambah untuk data besar (B10000)."""
    return max(3, len(str(n)))


def buat_buku(n, rng):
    w = lebar(n)
    baris = []
    for i in range(1, n + 1):
        kategori, id_rak = KATEGORI_RAK[(i - 1) % len(KATEGORI_RAK)]
        baris.append({
            "id_buku": f"B{i:0{w}d}",
            "judul": f"Judul {kategori} {i}",
            "penulis": f"Penulis {rng.randint(1, max(10, n // 5))}",
            "kategori": kategori,
            "tahun_terbit": rng.randint(1990, 2025),
            "id_rak": id_rak,
        })
    return baris


def buat_anggota(n):
    w = lebar(n)
    return [{"id_anggota": f"A{i:0{w}d}", "nama": f"Anggota Contoh {i}",
             "kontak": f"0812{i:08d}"} for i in range(1, n + 1)]


def buat_transaksi(n, rng):
    """n transaksi; sekitar 15% berstatus Dipinjam dan tiap buku aktif hanya dipinjam sekali."""
    w = lebar(n)
    jumlah_aktif = max(1, round(n * PROPORSI_DIPINJAM))
    buku_aktif = rng.sample(range(1, n + 1), jumlah_aktif)
    buku_lain = [i for i in range(1, n + 1) if i not in set(buku_aktif)]
    rentang = (TANGGAL_AKHIR - TANGGAL_AWAL).days

    mentah = []
    for nomor_buku in buku_aktif:
        mentah.append((TANGGAL_AWAL + timedelta(days=rng.randint(rentang - 30, rentang)),
                       nomor_buku, None))
    for _ in range(n - jumlah_aktif):
        pinjam = TANGGAL_AWAL + timedelta(days=rng.randint(0, rentang))
        kembali = pinjam + timedelta(days=rng.randint(1, 14))
        mentah.append((pinjam, rng.choice(buku_lain), kembali))
    mentah.sort(key=lambda x: x[0])                   # urut kejadian

    baris = []
    for nomor, (pinjam, nomor_buku, kembali) in enumerate(mentah, start=1):
        baris.append({
            "id_transaksi": f"T{nomor:0{w}d}",
            "id_anggota": f"A{rng.randint(1, n):0{w}d}",
            "id_buku": f"B{nomor_buku:0{w}d}",
            "tanggal_pinjam": pinjam.isoformat(),
            "tanggal_kembali": kembali.isoformat() if kembali else "",
            "status": "Dikembalikan" if kembali else "Dipinjam",
        })
    return baris


def tulis_csv(path, kolom, baris):
    with open(path, "w", newline="", encoding="utf-8") as f:
        penulis = csv.DictWriter(f, fieldnames=kolom)
        penulis.writeheader()
        penulis.writerows(baris)


def periksa(buku, anggota, transaksi):
    """Memastikan data lolos validasi kelas model dan antar-tabel konsisten."""
    for b in buku:
        Buku.dari_baris(b)
    for a in anggota:
        Anggota.dari_baris(a)
    id_buku = {b["id_buku"] for b in buku}
    id_anggota = {a["id_anggota"] for a in anggota}
    aktif = []
    for t in transaksi:
        Transaksi.dari_baris(t)
        assert t["id_buku"] in id_buku and t["id_anggota"] in id_anggota
        if t["status"] == "Dipinjam":
            aktif.append(t["id_buku"])
    assert len(aktif) == len(set(aktif)), "Ada buku dipinjam ganda"


def buat_dataset(n, seed, folder):
    rng = random.Random(seed + n)                     # seed berbeda per ukuran, tetap konsisten
    buku, anggota, transaksi = buat_buku(n, rng), buat_anggota(n), buat_transaksi(n, rng)
    periksa(buku, anggota, transaksi)
    tulis_csv(os.path.join(folder, f"buku_{n}.csv"), Buku.KOLOM, buku)
    tulis_csv(os.path.join(folder, f"anggota_{n}.csv"), Anggota.KOLOM, anggota)
    tulis_csv(os.path.join(folder, f"transaksi_{n}.csv"), Transaksi.KOLOM, transaksi)
    aktif = sum(1 for t in transaksi if t["status"] == "Dipinjam")
    print(f"  ukuran {n:>6}: {len(buku)} buku, {len(anggota)} anggota, "
          f"{len(transaksi)} transaksi ({aktif} dipinjam)")


def main():
    parser = argparse.ArgumentParser(description="Generator data simulasi untuk benchmark.")
    parser.add_argument("--ukuran", type=int, nargs="+", default=[100, 1000, 10000],
                        help="jumlah record per entitas (default: 100 1000 10000)")
    parser.add_argument("--seed", type=int, default=42, help="seed acak (default 42)")
    parser.add_argument("--out", default=os.path.join("data", "bench"),
                        help="folder keluaran (default data/bench)")
    argumen = parser.parse_args()
    if any(n < 10 for n in argumen.ukuran):
        parser.error("ukuran minimal 10 record")

    os.makedirs(argumen.out, exist_ok=True)
    print(f"Membuat data simulasi di '{argumen.out}' (seed {argumen.seed}):")
    for n in argumen.ukuran:
        buat_dataset(n, argumen.seed, argumen.out)
    print("Selesai.")


if __name__ == "__main__":
    main()