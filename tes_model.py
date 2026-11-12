"""Tes otomatis untuk kelas model (Buku, Anggota, Transaksi, Rak) dan pemuatan CSV.
Jalankan dari folder paling luar project:  python tes_model.py

Butuh file di folder data/: buku.csv, anggota.csv, transaksi.csv, rak.csv, koneksi_rak.csv
(ganti nama file CSV kalian dulu jika masih berakhiran _v2).
"""
import csv
import os
import sys

from models.anggota import Anggota
from models.buku import Buku
from models.rak import Rak
from models.transaksi import Transaksi
from structures.bst import BST
from structures.graph import Graph
from structures.hash_table import HashTable
from structures.linked_list import LinkedList

FILE = {
    "buku": "data/buku.csv",
    "anggota": "data/anggota.csv",
    "transaksi": "data/transaksi.csv",
    "rak": "data/rak.csv",
    "koneksi": "data/koneksi_rak.csv",
}
hilang = [path for path in FILE.values() if not os.path.exists(path)]
if hilang:
    print("File CSV belum ditemukan:", ", ".join(hilang))
    print("Pastikan nama file di folder data/ sudah diganti (tanpa akhiran _v2).")
    sys.exit(1)


def baca_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def harus_error(fungsi, kata_kunci):
    """Memastikan fungsi melempar ValueError yang pesannya memuat kata_kunci."""
    try:
        fungsi()
    except ValueError as e:
        assert kata_kunci in str(e), f"Pesan error tidak sesuai: {e}"
        return
    raise AssertionError(f"Seharusnya ValueError ({kata_kunci})")


# ---------- Validasi kelas model ----------
b = Buku("B001", "Bumi", "Tere Liye", "Novel", 2017, "RAK-NOV")
assert "Bumi" in str(b) and b.ke_baris()["tahun_terbit"] == 2017
harus_error(lambda: Buku("", "Bumi", "X", "Novel", 2017, "RAK-NOV"), "ID Buku")
harus_error(lambda: Buku("B002", "  ", "X", "Novel", 2017, "RAK-NOV"), "Judul")
harus_error(lambda: Buku("B002", "J", "X", "Novel", "2017", "RAK-NOV"), "angka bulat")
harus_error(lambda: Buku("B002", "J", "X", "Novel", 1500000, "RAK-NOV"), "antara")
harus_error(lambda: Buku.dari_baris({"id_buku": "B1"}), "Kolom")
harus_error(lambda: Buku.dari_baris({"id_buku": "B1", "judul": "J", "penulis": "P",
                                     "kategori": "K", "tahun_terbit": "abc", "id_rak": "R"}), "bukan angka")

harus_error(lambda: Anggota("A001", "", "0812"), "Nama")
harus_error(lambda: Rak("RAK-X", "Rak X", None), "Lokasi")

t = Transaksi("T001", "A001", "B001", "2026-11-01")
assert t.sedang_dipinjam() and t.tanggal_kembali is None
harus_error(lambda: t.kembalikan("2026-10-01"), "lebih awal")
harus_error(lambda: t.kembalikan("12/11/2026"), "YYYY-MM-DD")
harus_error(lambda: t.kembalikan("2026-13-40"), "valid")
t.kembalikan("2026-11-05")
assert not t.sedang_dipinjam() and t.status == "Dikembalikan"
harus_error(lambda: t.kembalikan("2026-11-06"), "sudah dikembalikan")
t.batalkan_pengembalian()
assert t.sedang_dipinjam() and t.tanggal_kembali is None
harus_error(lambda: t.batalkan_pengembalian(), "belum dikembalikan")
harus_error(lambda: Transaksi("T2", "A1", "B1", "2026-11-01", "2026-11-02", "Dipinjam"), "tidak boleh punya")
harus_error(lambda: Transaksi("T2", "A1", "B1", "2026-11-01", None, "Dikembalikan"), "wajib punya")
harus_error(lambda: Transaksi("T2", "A1", "B1", "2026-11-01", None, "Hilang"), "Status")
assert Transaksi("T2", "A1", "B1", "2026-11-01", "", "Dipinjam").tanggal_kembali is None  # "" dari CSV -> None

# ---------- Memuat CSV asli ----------
baris_buku = baca_csv(FILE["buku"])
baris_anggota = baca_csv(FILE["anggota"])
baris_trx = baca_csv(FILE["transaksi"])
baris_rak = baca_csv(FILE["rak"])
daftar_buku = [Buku.dari_baris(r) for r in baris_buku]
daftar_anggota = [Anggota.dari_baris(r) for r in baris_anggota]
daftar_trx = [Transaksi.dari_baris(r) for r in baris_trx]
daftar_rak = [Rak.dari_baris(r) for r in baris_rak]
assert len(daftar_buku) >= 100 and len(daftar_anggota) >= 100 and len(daftar_trx) >= 100
print(f"Dimuat: {len(daftar_buku)} buku, {len(daftar_anggota)} anggota, "
      f"{len(daftar_trx)} transaksi, {len(daftar_rak)} rak")

# bolak-balik (dari_baris -> ke_baris) harus sama dengan isi CSV asli
for baris, obj in list(zip(baris_buku, daftar_buku)) + list(zip(baris_anggota, daftar_anggota)) \
        + list(zip(baris_trx, daftar_trx)) + list(zip(baris_rak, daftar_rak)):
    assert {k: str(v) for k, v in obj.ke_baris().items()} == baris

# integritas antar-tabel
id_buku = {x.id_buku for x in daftar_buku}
id_anggota = {x.id_anggota for x in daftar_anggota}
id_rak = {x.id_rak for x in daftar_rak}
assert all(x.id_rak in id_rak for x in daftar_buku)
assert all(x.id_buku in id_buku and x.id_anggota in id_anggota for x in daftar_trx)
aktif = [x for x in daftar_trx if x.sedang_dipinjam()]
print(f"Transaksi aktif (Dipinjam): {len(aktif)}")

# ---------- Digabung dengan struktur data ----------
pohon = BST()
for x in daftar_buku:
    pohon.insert(x.id_buku, x)
tabel = HashTable()
for x in daftar_anggota:
    tabel.insert(x.id_anggota, x)
riwayat = LinkedList(key_func=lambda tr: tr.id_transaksi)
for x in daftar_trx:
    riwayat.insert(x)
assert pohon.search("B001").judul == daftar_buku[0].judul
assert tabel.search("A001").nama == daftar_anggota[0].nama
assert riwayat.search("T001").id_buku == daftar_trx[0].id_buku
assert pohon.search("B999") is None

graph = Graph(berarah=False, berbobot=True)
for r in daftar_rak:
    graph.tambah_simpul(r.id_rak)
for k in baca_csv(FILE["koneksi"]):
    graph.tambah_sisi(k["rak_asal"], k["rak_tujuan"], int(k["jarak_m"]))
assert len(graph.bfs(daftar_rak[0].id_rak)) == len(daftar_rak)
print("SEMUA TES MODEL LULUS")