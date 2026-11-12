"""Kelas model Anggota.

Dipakai pada fitur: pencarian anggota berdasarkan ID Anggota (Hash Table,
key = id_anggota). Seluruh data adalah data simulasi, bukan data pribadi asli.
"""

from .validasi import periksa_kolom, wajib_teks


class Anggota:
    """ADT Anggota: satu anggota perpustakaan.

    Atribut:
        id_anggota: kode unik anggota, misalnya 'A001' (key Hash Table).
        nama: nama anggota (simulasi).
        kontak: nomor kontak (simulasi).
    """

    KOLOM = ("id_anggota", "nama", "kontak")

    def __init__(self, id_anggota, nama, kontak):
        self.id_anggota = wajib_teks(id_anggota, "ID Anggota")
        self.nama = wajib_teks(nama, "Nama")
        self.kontak = wajib_teks(kontak, "Kontak")

    @classmethod
    def dari_baris(cls, baris):
        """Membuat Anggota dari satu baris CSV (dict dari csv.DictReader)."""
        periksa_kolom(baris, cls.KOLOM)
        return cls(baris["id_anggota"], baris["nama"], baris["kontak"])

    def ke_baris(self):
        """Mengubah Anggota menjadi dict untuk ditulis ke CSV."""
        return {"id_anggota": self.id_anggota, "nama": self.nama, "kontak": self.kontak}

    def __str__(self):
        return f"[{self.id_anggota}] {self.nama} | Kontak: {self.kontak}"

    def __repr__(self):
        return f"Anggota({self.id_anggota!r}, {self.nama!r})"