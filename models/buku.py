"""Kelas model Buku.

Dipakai pada fitur: koleksi buku (Array/List) dan pencarian buku berdasarkan
ID Buku (BST, key = id_buku).
Struktur data TIDAK perlu tahu isi kelas ini; mereka hanya menyimpan objek Buku
dan membandingkan lewat key yang diberikan (misalnya buku.id_buku).
"""

from .validasi import periksa_kolom, wajib_tahun, wajib_teks


class Buku:
    """ADT Buku: satu judul buku di koleksi perpustakaan.

    Atribut:
        id_buku: kode unik buku, misalnya 'B001' (key BST).
        judul, penulis, kategori: teks tidak kosong.
        tahun_terbit: bilangan bulat, misalnya 2017.
        id_rak: ID rak tempat buku disimpan, misalnya 'RAK-NOV'.
    """

    KOLOM = ("id_buku", "judul", "penulis", "kategori", "tahun_terbit", "id_rak")

    def __init__(self, id_buku, judul, penulis, kategori, tahun_terbit, id_rak):
        self.id_buku = wajib_teks(id_buku, "ID Buku")
        self.judul = wajib_teks(judul, "Judul")
        self.penulis = wajib_teks(penulis, "Penulis")
        self.kategori = wajib_teks(kategori, "Kategori")
        self.tahun_terbit = wajib_tahun(tahun_terbit)
        self.id_rak = wajib_teks(id_rak, "ID Rak")

    @classmethod
    def dari_baris(cls, baris):
        """Membuat Buku dari satu baris CSV (dict dari csv.DictReader)."""
        periksa_kolom(baris, cls.KOLOM)
        try:
            tahun = int(baris["tahun_terbit"])
        except (TypeError, ValueError):
            raise ValueError(f"Tahun terbit '{baris['tahun_terbit']}' bukan angka.") from None
        return cls(baris["id_buku"], baris["judul"], baris["penulis"],
                   baris["kategori"], tahun, baris["id_rak"])

    def ke_baris(self):
        """Mengubah Buku menjadi dict untuk ditulis ke CSV (csv.DictWriter)."""
        return {
            "id_buku": self.id_buku,
            "judul": self.judul,
            "penulis": self.penulis,
            "kategori": self.kategori,
            "tahun_terbit": self.tahun_terbit,
            "id_rak": self.id_rak,
        }

    def __str__(self):
        return (f"[{self.id_buku}] {self.judul} - {self.penulis} "
                f"({self.tahun_terbit}) | {self.kategori} | Rak: {self.id_rak}")

    def __repr__(self):
        return f"Buku({self.id_buku!r}, {self.judul!r})"