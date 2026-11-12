"""Tes sinkronisasi: struktur data Hanif + Andra bekerja bersama dalam alur perpustakaan.
Jalankan dari folder paling luar project (setelah git pull):  python tes_sinkron.py
Tidak memakai kelas model asli, jadi tetap jalan walau models/ belum final.
"""
import contextlib
import io
import random
from structures.array_list import DynamicArray
from structures.linked_list import LinkedList
from structures.bst import BST
from structures.stack import Stack
from structures.antrean import Queue
from structures.hash_table import HashTable
from structures.graph import buat_graph_rak


class Buku:
    def __init__(self, id_buku, judul, id_rak, stok):
        self.id_buku, self.judul, self.id_rak, self.stok = id_buku, judul, id_rak, stok


class Anggota:
    def __init__(self, id_anggota, nama):
        self.id_anggota, self.nama = id_anggota, nama


rng = random.Random(42)

# 1) Muat 100 buku ke Array (urut) dan BST (urutan acak)
daftar_buku = DynamicArray(key_func=lambda b: b.id_buku)
pohon_buku = BST()
urutan = list(range(1, 101))
for i in urutan:
    daftar_buku.insert(Buku(f"B{i:05d}", f"Judul {i}", f"R{(i - 1) // 10 + 1:02d}", 1 if i % 10 == 0 else 3))
rng.shuffle(urutan)
for i in urutan:
    pohon_buku.insert(f"B{i:05d}", daftar_buku.search(f"B{i:05d}"))
assert len(daftar_buku) == len(pohon_buku) == 100
assert pohon_buku.inorder() == [b.id_buku for b in daftar_buku]

# 2) Muat 100 anggota ke Hash Table (resize memang mencetak pesan, kita senyapkan)
tabel_anggota = HashTable()
with contextlib.redirect_stdout(io.StringIO()):
    for i in range(1, 101):
        tabel_anggota.insert(f"A{i:05d}", Anggota(f"A{i:05d}", f"Anggota {i}"))
assert tabel_anggota.size() == 100 and tabel_anggota.jumlah_resize() >= 1
assert tabel_anggota.search("A00042").nama == "Anggota 42"

# 3) Alur peminjaman: buku stok 1 (B00010) dipinjam lalu peminjam berikutnya antre
riwayat = LinkedList(key_func=lambda t: t[0])
undo = Stack()
antrean = Queue()
nomor_transaksi = 0


def pinjam(id_anggota, id_buku):
    global nomor_transaksi
    anggota = tabel_anggota.search(id_anggota)       # Hash Table
    buku = pohon_buku.search(id_buku)                # BST
    assert anggota is not None and buku is not None
    if buku.stok == 0:
        antrean.enqueue((id_anggota, id_buku))       # Queue
        return "ANTRE"
    buku.stok -= 1
    nomor_transaksi += 1
    transaksi = (f"T{nomor_transaksi:05d}", id_anggota, id_buku, "DIPINJAM")
    riwayat.insert(transaksi)                        # Linked List
    undo.push(transaksi)                             # Stack
    return "BERHASIL"


assert pinjam("A00001", "B00010") == "BERHASIL"
assert pinjam("A00002", "B00010") == "ANTRE"
assert antrean.front() == ("A00002", "B00010")
assert riwayat.search("T00001")[1] == "A00001"

batal = undo.pop()                                   # undo transaksi terakhir
riwayat.delete(batal[0])
pohon_buku.search(batal[2]).stok += 1
assert len(riwayat) == 0 and pohon_buku.search("B00010").stok == 1
assert pinjam(*antrean.dequeue()) == "BERHASIL"      # antrean dilayani FIFO

# 4) Graph: rute dari rak buku ke rak lain, BFS dan DFS memuat semua rak
graph = buat_graph_rak()
rak_buku = pohon_buku.search("B00010").id_rak
rute, total = graph.rute_tersingkat_langkah(rak_buku, "R10")
assert rute[0] == rak_buku and rute[-1] == "R10" and total > 0
assert len(graph.bfs("R01")) == len(graph.dfs("R01")) == 10
assert pohon_buku.search("B00001") is not None and pohon_buku.search("B99999") is None

print("SINKRONISASI LULUS: Array, Linked List, BST, Stack, Queue, Hash Table, dan Graph bekerja bersama")