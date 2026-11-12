"""Kelas model Transaksi.

Dipakai pada fitur: riwayat peminjaman/pengembalian (Linked List, urut kejadian),
simulasi undo (Stack), dan pengecekan buku yang sedang dipinjam (antrean).
Tanggal disimpan sebagai teks berformat YYYY-MM-DD.
"""

from .validasi import periksa_kolom, wajib_tanggal, wajib_teks


class Transaksi:
    """ADT Transaksi: satu peminjaman buku oleh satu anggota.

    Aturan (divalidasi saat objek dibuat):
        - status 'Dipinjam'     -> tanggal_kembali harus kosong (None)
        - status 'Dikembalikan' -> tanggal_kembali wajib ada dan tidak
                                   boleh lebih awal dari tanggal_pinjam
    """

    STATUS_DIPINJAM = "Dipinjam"
    STATUS_DIKEMBALIKAN = "Dikembalikan"
    KOLOM = ("id_transaksi", "id_anggota", "id_buku",
             "tanggal_pinjam", "tanggal_kembali", "status")

    def __init__(self, id_transaksi, id_anggota, id_buku, tanggal_pinjam,
                 tanggal_kembali=None, status=STATUS_DIPINJAM):
        self.id_transaksi = wajib_teks(id_transaksi, "ID Transaksi")
        self.id_anggota = wajib_teks(id_anggota, "ID Anggota")
        self.id_buku = wajib_teks(id_buku, "ID Buku")
        self.tanggal_pinjam = wajib_tanggal(tanggal_pinjam, "Tanggal pinjam")

        if status not in (self.STATUS_DIPINJAM, self.STATUS_DIKEMBALIKAN):
            raise ValueError(f"Status harus '{self.STATUS_DIPINJAM}' atau "
                             f"'{self.STATUS_DIKEMBALIKAN}', bukan '{status}'.")
        if tanggal_kembali is not None and str(tanggal_kembali).strip() == "":
            tanggal_kembali = None

        if status == self.STATUS_DIPINJAM:
            if tanggal_kembali is not None:
                raise ValueError("Transaksi berstatus Dipinjam tidak boleh punya tanggal kembali.")
        else:
            if tanggal_kembali is None:
                raise ValueError("Transaksi berstatus Dikembalikan wajib punya tanggal kembali.")
            tanggal_kembali = wajib_tanggal(tanggal_kembali, "Tanggal kembali")
            if tanggal_kembali < self.tanggal_pinjam:
                raise ValueError("Tanggal kembali tidak boleh lebih awal dari tanggal pinjam.")

        self.tanggal_kembali = tanggal_kembali
        self.status = status

    def sedang_dipinjam(self):
        """True jika buku belum dikembalikan."""
        return self.status == self.STATUS_DIPINJAM

    def kembalikan(self, tanggal_kembali):
        """Menandai transaksi sebagai dikembalikan pada tanggal tertentu.

        Raises:
            ValueError: jika sudah dikembalikan, format tanggal salah, atau
                        tanggal kembali lebih awal dari tanggal pinjam.
        """
        if not self.sedang_dipinjam():
            raise ValueError(f"Transaksi {self.id_transaksi} sudah dikembalikan.")
        tanggal = wajib_tanggal(tanggal_kembali, "Tanggal kembali")
        if tanggal < self.tanggal_pinjam:
            raise ValueError("Tanggal kembali tidak boleh lebih awal dari tanggal pinjam.")
        self.tanggal_kembali = tanggal
        self.status = self.STATUS_DIKEMBALIKAN

    @classmethod
    def dari_baris(cls, baris):
        """Membuat Transaksi dari satu baris CSV (dict dari csv.DictReader)."""
        periksa_kolom(baris, cls.KOLOM)
        return cls(baris["id_transaksi"], baris["id_anggota"], baris["id_buku"],
                   baris["tanggal_pinjam"], baris["tanggal_kembali"], baris["status"])

    def ke_baris(self):
        """Mengubah Transaksi menjadi dict untuk ditulis ke CSV (tanggal kosong = '')."""
        return {
            "id_transaksi": self.id_transaksi,
            "id_anggota": self.id_anggota,
            "id_buku": self.id_buku,
            "tanggal_pinjam": self.tanggal_pinjam,
            "tanggal_kembali": self.tanggal_kembali or "",
            "status": self.status,
        }

    def __str__(self):
        kembali = self.tanggal_kembali if self.tanggal_kembali else "-"
        return (f"[{self.id_transaksi}] {self.id_anggota} meminjam {self.id_buku} | "
                f"pinjam: {self.tanggal_pinjam}, kembali: {kembali} | {self.status}")

    def __repr__(self):
        return f"Transaksi({self.id_transaksi!r}, {self.id_anggota!r}, {self.id_buku!r})"