"""Kelas model Rak.

Dipakai pada fitur: lokasi rak buku dan graph keterhubungan antar-rak
(setiap rak menjadi satu simpul/vertex, id_rak menjadi id simpulnya).
"""

from .validasi import periksa_kolom, wajib_teks


class Rak:
    """ADT Rak: satu rak di perpustakaan.

    Atribut:
        id_rak: kode unik rak, misalnya 'RAK-NOV' (id simpul graph).
        nama_rak: nama rak, misalnya 'Rak Novel'.
        lokasi: posisi fisik, misalnya 'Lantai 1 - Zona B'.
    """

    KOLOM = ("id_rak", "nama_rak", "lokasi")

    def __init__(self, id_rak, nama_rak, lokasi):
        self.id_rak = wajib_teks(id_rak, "ID Rak")
        self.nama_rak = wajib_teks(nama_rak, "Nama Rak")
        self.lokasi = wajib_teks(lokasi, "Lokasi")

    @classmethod
    def dari_baris(cls, baris):
        """Membuat Rak dari satu baris CSV (dict dari csv.DictReader)."""
        periksa_kolom(baris, cls.KOLOM)
        return cls(baris["id_rak"], baris["nama_rak"], baris["lokasi"])

    def ke_baris(self):
        """Mengubah Rak menjadi dict untuk ditulis ke CSV."""
        return {"id_rak": self.id_rak, "nama_rak": self.nama_rak, "lokasi": self.lokasi}

    def __str__(self):
        return f"[{self.id_rak}] {self.nama_rak} ({self.lokasi})"

    def __repr__(self):
        return f"Rak({self.id_rak!r}, {self.nama_rak!r})"