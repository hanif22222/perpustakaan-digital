"""Kelas Perpustakaan: menyatukan semua struktur data menjadi satu aplikasi.

Peran tiap struktur data dalam aplikasi:
    DynamicArray -> daftar koleksi buku dan daftar rak (akses, ubah, hapus, tampilkan semua)
    BST          -> pencarian buku berdasarkan ID Buku
    HashTable    -> pencarian anggota berdasarkan ID Anggota; juga untuk mencatat
                    pinjaman aktif per buku dan antrean per buku
    LinkedList   -> riwayat peminjaman/pengembalian (urut kejadian)
    Stack        -> riwayat aksi terakhir untuk simulasi pembatalan (undo)
    Queue        -> antrean anggota untuk buku yang sedang dipinjam
    Graph        -> keterhubungan antar-rak (BFS/DFS dan rute antar rak)

Kelas ini TIDAK memakai input() dan print(), sehingga logikanya mudah diuji.
Tampilan menu ada di main.py.
"""

import contextlib
import csv
import io
import os
import random
from datetime import date

from models.anggota import Anggota
from models.buku import Buku
from models.rak import Rak
from models.transaksi import Transaksi
from structures.antrean import Queue
from structures.array_list import DynamicArray
from structures.bst import BST
from structures.graph import Graph
from structures.hash_table import HashTable
from structures.linked_list import LinkedList
from structures.stack import Stack


class Aksi:
    """Satu catatan aksi di Stack (untuk undo): jenis aksi dan transaksi terkait."""

    def __init__(self, jenis, transaksi):
        self.jenis = jenis              # "PINJAM" atau "KEMBALI"
        self.transaksi = transaksi

    def __str__(self):
        t = self.transaksi
        return f"{self.jenis} {t.id_transaksi} (anggota {t.id_anggota}, buku {t.id_buku})"


def baca_csv(path):
    """Membaca file CSV menjadi list of dict."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File tidak ditemukan: {path}")
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class Perpustakaan:
    """Aplikasi Perpustakaan Digital (lapisan logika)."""

    def __init__(self):
        self.daftar_buku = DynamicArray(key_func=lambda b: b.id_buku)
        self.pohon_buku = BST()
        self.daftar_rak = DynamicArray(key_func=lambda r: r.id_rak)
        self.graph_rak = Graph(berarah=False, berbobot=True)
        self.tabel_anggota = HashTable()
        self.riwayat = LinkedList(key_func=lambda t: t.id_transaksi)
        self.pinjaman_aktif = HashTable()      # id_buku -> Transaksi yang sedang berjalan
        self.antrean_buku = HashTable()        # id_buku -> Queue berisi id_anggota
        self.penanda_antrean = HashTable()     # "id_anggota|id_buku" -> True (cegah antre ganda)
        self.riwayat_aksi = Stack()
        self._nomor_transaksi = 0

    @staticmethod
    def _id(teks):
        """Menyeragamkan ID: spasi dibuang, huruf jadi kapital (b001 -> B001)."""
        return teks.strip().upper() if isinstance(teks, str) else teks

    # ================= memuat data =================
    def muat_data(self, folder="data"):
        """Memuat rak, koneksi rak, buku, anggota, dan transaksi dari file CSV.

        Pesan [RESIZE] dari Hash Table disenyapkan selama pemuatan.
        """
        with contextlib.redirect_stdout(io.StringIO()):
            for baris in baca_csv(os.path.join(folder, "rak.csv")):
                rak = Rak.dari_baris(baris)
                self.daftar_rak.insert(rak)
                self.graph_rak.tambah_simpul(rak.id_rak)
            for baris in baca_csv(os.path.join(folder, "koneksi_rak.csv")):
                self.graph_rak.tambah_sisi(baris["rak_asal"], baris["rak_tujuan"],
                                           int(baris["jarak_m"]))
            semua_buku = []
            for baris in baca_csv(os.path.join(folder, "buku.csv")):
                buku = Buku.dari_baris(baris)
                if self.daftar_rak.search(buku.id_rak) is None:
                    raise ValueError(f"Buku {buku.id_buku} memakai rak {buku.id_rak} yang tidak ada.")
                if self.daftar_buku.search(buku.id_buku) is not None:
                    raise ValueError(f"ID Buku {buku.id_buku} kembar di buku.csv.")
                self.daftar_buku.insert(buku)           # Array: sesuai urutan file
                semua_buku.append(buku)
            # BST: dimasukkan dalam urutan acak (seed tetap) agar pohon tidak miring.
            # Jika dimasukkan sesuai urutan ID (B001, B002, ...), pohon menjadi skewed
            # setinggi jumlah buku dan pencarian berubah menjadi O(n).
            urutan = random.Random(42)
            urutan.shuffle(semua_buku)
            for buku in semua_buku:
                self.pohon_buku.insert(buku.id_buku, buku)
            for baris in baca_csv(os.path.join(folder, "anggota.csv")):
                anggota = Anggota.dari_baris(baris)
                if self.tabel_anggota.search(anggota.id_anggota) is not None:
                    raise ValueError(f"ID Anggota {anggota.id_anggota} kembar di anggota.csv.")
                self.tabel_anggota.insert(anggota.id_anggota, anggota)
            for baris in baca_csv(os.path.join(folder, "transaksi.csv")):
                transaksi = Transaksi.dari_baris(baris)
                self.riwayat.insert(transaksi)
                if transaksi.sedang_dipinjam():
                    if self.pinjaman_aktif.search(transaksi.id_buku) is not None:
                        raise ValueError(f"Buku {transaksi.id_buku} dipinjam ganda di transaksi.csv.")
                    self.pinjaman_aktif.insert(transaksi.id_buku, transaksi)
                try:
                    self._nomor_transaksi = max(self._nomor_transaksi, int(transaksi.id_transaksi[1:]))
                except ValueError:
                    pass
        return self.ringkasan()

    def ringkasan(self):
        """Jumlah data saat ini, dalam bentuk dict (untuk ditampilkan)."""
        return {
            "buku": len(self.daftar_buku),
            "anggota": len(self.tabel_anggota),
            "transaksi": len(self.riwayat),
            "sedang_dipinjam": len(self.pinjaman_aktif),
            "rak": len(self.daftar_rak),
            "aksi_tercatat": len(self.riwayat_aksi),
        }

    # ================= buku (Array + BST) =================
    def cari_buku(self, id_buku):
        """Mencari buku lewat BST. Mengembalikan Buku atau None."""
        return self.pohon_buku.search(self._id(id_buku))

    def tambah_buku(self, id_buku, judul, penulis, kategori, tahun_terbit, id_rak):
        id_buku, id_rak = self._id(id_buku), self._id(id_rak)
        if self.pohon_buku.search(id_buku) is not None:
            raise ValueError(f"ID Buku {id_buku} sudah dipakai.")
        if self.daftar_rak.search(id_rak) is None:
            raise ValueError(f"Rak {id_rak} tidak ditemukan.")
        buku = Buku(id_buku, judul, penulis, kategori, tahun_terbit, id_rak)
        self.daftar_buku.insert(buku)
        self.pohon_buku.insert(id_buku, buku)
        return buku

    def ubah_buku(self, id_buku, judul=None, penulis=None, kategori=None,
                  tahun_terbit=None, id_rak=None):
        """Mengubah data buku. Field yang bernilai None tidak diubah (ID Buku tidak bisa diubah).

        Array diperbarui lewat set(), BST lewat insert pada key yang sama (value diperbarui).
        """
        lama = self.cari_buku(id_buku)
        if lama is None:
            raise ValueError(f"Buku {self._id(id_buku)} tidak ditemukan.")
        data = lama.ke_baris()
        for nama, nilai in (("judul", judul), ("penulis", penulis), ("kategori", kategori),
                            ("tahun_terbit", tahun_terbit), ("id_rak", id_rak)):
            if nilai is not None:
                data[nama] = nilai
        data["id_rak"] = self._id(data["id_rak"])
        if self.daftar_rak.search(data["id_rak"]) is None:
            raise ValueError(f"Rak {data['id_rak']} tidak ditemukan.")
        baru = Buku(**data)
        self.daftar_buku.set(self.daftar_buku.index_of(lama.id_buku), baru)
        self.pohon_buku.insert(baru.id_buku, baru)
        return baru

    def hapus_buku(self, id_buku):
        buku = self.cari_buku(id_buku)
        if buku is None:
            raise ValueError(f"Buku {self._id(id_buku)} tidak ditemukan.")
        if self.pinjaman_aktif.search(buku.id_buku) is not None:
            raise ValueError("Buku sedang dipinjam, tidak bisa dihapus.")
        self.daftar_buku.delete(buku.id_buku)
        self.pohon_buku.delete(buku.id_buku)
        return buku

    def lokasi_buku(self, id_buku):
        """Mengembalikan (Buku, Rak) tempat buku disimpan."""
        buku = self.cari_buku(id_buku)
        if buku is None:
            raise ValueError(f"Buku {self._id(id_buku)} tidak ditemukan.")
        return buku, self.daftar_rak.search(buku.id_rak)

    # ================= anggota (Hash Table) =================
    def cari_anggota(self, id_anggota):
        return self.tabel_anggota.search(self._id(id_anggota))

    def tambah_anggota(self, id_anggota, nama, kontak):
        id_anggota = self._id(id_anggota)
        if self.tabel_anggota.search(id_anggota) is not None:
            raise ValueError(f"ID Anggota {id_anggota} sudah dipakai.")
        anggota = Anggota(id_anggota, nama, kontak)
        self.tabel_anggota.insert(id_anggota, anggota)
        return anggota

    def hapus_anggota(self, id_anggota):
        anggota = self.cari_anggota(id_anggota)
        if anggota is None:
            raise ValueError(f"Anggota {self._id(id_anggota)} tidak ditemukan.")
        for transaksi in self.riwayat:
            if transaksi.id_anggota == anggota.id_anggota and transaksi.sedang_dipinjam():
                raise ValueError("Anggota masih meminjam buku, tidak bisa dihapus.")
        self.tabel_anggota.delete(anggota.id_anggota)
        return anggota

    # ================= peminjaman (Linked List + Stack + Queue) =================
    def pinjam(self, id_anggota, id_buku, tanggal=None):
        """Meminjam buku.

        Mengembalikan ("DIPINJAM", Transaksi) jika berhasil, atau
        ("ANTRE", posisi) jika buku sedang dipinjam anggota lain (masuk Queue).
        """
        id_anggota, id_buku = self._id(id_anggota), self._id(id_buku)
        if self.tabel_anggota.search(id_anggota) is None:
            raise ValueError(f"Anggota {id_anggota} tidak ditemukan.")
        if self.pohon_buku.search(id_buku) is None:
            raise ValueError(f"Buku {id_buku} tidak ditemukan.")
        tanggal = tanggal or date.today().isoformat()

        aktif = self.pinjaman_aktif.search(id_buku)
        if aktif is not None:
            if aktif.id_anggota == id_anggota:
                raise ValueError("Anggota ini sedang meminjam buku tersebut.")
            kunci = f"{id_anggota}|{id_buku}"
            if self.penanda_antrean.search(kunci) is not None:
                raise ValueError("Anggota ini sudah ada dalam antrean buku tersebut.")
            antrean = self.antrean_buku.search(id_buku)
            if antrean is None:
                antrean = Queue()
                self.antrean_buku.insert(id_buku, antrean)
            antrean.enqueue(id_anggota)
            self.penanda_antrean.insert(kunci, True)
            return "ANTRE", len(antrean)

        nomor = self._nomor_transaksi + 1
        transaksi = Transaksi(f"T{nomor:03d}", id_anggota, id_buku, tanggal)
        self._nomor_transaksi = nomor
        self.riwayat.insert(transaksi)
        self.pinjaman_aktif.insert(id_buku, transaksi)
        self.riwayat_aksi.push(Aksi("PINJAM", transaksi))
        return "DIPINJAM", transaksi

    def kembalikan(self, id_buku, tanggal=None):
        """Mengembalikan buku. Jika ada antrean, anggota terdepan otomatis meminjam.

        Mengembalikan (transaksi yang dikembalikan, transaksi baru dari antrean atau None).
        """
        id_buku = self._id(id_buku)
        aktif = self.pinjaman_aktif.search(id_buku)
        if aktif is None:
            raise ValueError(f"Buku {id_buku} tidak sedang dipinjam.")
        aktif.kembalikan(tanggal or date.today().isoformat())
        self.pinjaman_aktif.delete(id_buku)
        self.riwayat_aksi.push(Aksi("KEMBALI", aktif))

        berikutnya = None
        antrean = self.antrean_buku.search(id_buku)
        while antrean is not None and not antrean.is_empty():
            id_anggota = antrean.dequeue()
            self.penanda_antrean.delete(f"{id_anggota}|{id_buku}")
            if self.tabel_anggota.search(id_anggota) is None:
                continue                                  # anggota sudah dihapus, lewati
            _, berikutnya = self.pinjam(id_anggota, id_buku, tanggal)
            break
        return aktif, berikutnya

    def batalkan_aksi_terakhir(self):
        """Simulasi undo: membatalkan aksi teratas di Stack. Mengembalikan Aksi yang dibatalkan.

        Catatan: pembatalan peminjaman otomatis dari antrean tidak mengembalikan
        anggota ke antrean (ini simulasi sederhana).
        """
        if self.riwayat_aksi.is_empty():
            raise ValueError("Tidak ada aksi yang bisa dibatalkan.")
        aksi = self.riwayat_aksi.peek()
        transaksi = aksi.transaksi
        if aksi.jenis == "PINJAM":
            self.riwayat.delete(transaksi.id_transaksi)
            self.pinjaman_aktif.delete(transaksi.id_buku)
        else:
            if self.pinjaman_aktif.search(transaksi.id_buku) is not None:
                raise ValueError("Pengembalian tidak bisa dibatalkan: buku sudah dipinjam anggota lain.")
            transaksi.batalkan_pengembalian()
            self.pinjaman_aktif.insert(transaksi.id_buku, transaksi)
        self.riwayat_aksi.pop()
        return aksi

    def riwayat_anggota(self, id_anggota):
        """Daftar transaksi milik seorang anggota (dibaca dari Linked List)."""
        id_anggota = self._id(id_anggota)
        if self.tabel_anggota.search(id_anggota) is None:
            raise ValueError(f"Anggota {id_anggota} tidak ditemukan.")
        return [t for t in self.riwayat if t.id_anggota == id_anggota]

    def daftar_dipinjam(self):
        """Daftar transaksi yang masih berstatus Dipinjam."""
        return [t for t in self.riwayat if t.sedang_dipinjam()]

    def antrean_untuk(self, id_buku):
        """Queue antrean sebuah buku, atau None jika tidak ada antrean."""
        id_buku = self._id(id_buku)
        if self.pohon_buku.search(id_buku) is None:
            raise ValueError(f"Buku {id_buku} tidak ditemukan.")
        antrean = self.antrean_buku.search(id_buku)
        return antrean if antrean is not None and not antrean.is_empty() else None

    # ================= rak (Graph) =================
    def rute_rak(self, asal, tujuan):
        """Rute dengan langkah paling sedikit antar dua rak (BFS).
        Mengembalikan (daftar id rak, total jarak) atau (None, 0) jika tidak ada rute."""
        return self.graph_rak.rute_tersingkat_langkah(self._id(asal), self._id(tujuan))