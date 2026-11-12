"""Tes otomatis untuk logika aplikasi (perpustakaan.py).
Jalankan dari folder paling luar project:  python tes_aplikasi.py
"""
from perpustakaan import Perpustakaan


def harus_error(fungsi, kata_kunci):
    try:
        fungsi()
    except ValueError as e:
        assert kata_kunci in str(e), f"Pesan error tidak sesuai: {e}"
        return
    raise AssertionError(f"Seharusnya ValueError ({kata_kunci})")


app = Perpustakaan()
r = app.muat_data("data")
assert r["buku"] == 100 and r["anggota"] == 100 and r["transaksi"] == 100
assert r["sedang_dipinjam"] == 15 and r["rak"] == 5

assert app.pohon_buku.tinggi() < 20          # BST seimbang, bukan miring 100 level
aktif = app.daftar_dipinjam()
assert len(aktif) == 15
buku_dipinjam = aktif[0].id_buku
peminjam = aktif[0].id_anggota
anggota_lain = next(a for a in ("A001", "A002", "A003") if a != peminjam)
anggota_lain2 = next(a for a in ("A010", "A011", "A012") if a != peminjam)

# ---- buku: array + BST ----
b = app.cari_buku("b001")                      # huruf kecil tetap ketemu
assert b is not None and b.id_buku == "B001"
assert app.cari_buku("B999") is None
baru = app.tambah_buku("B101", "Buku Baru", "Penulis Baru", "Novel", 2024, "rak-nov")
assert len(app.daftar_buku) == 101 and app.cari_buku("B101") is baru and baru.id_rak == "RAK-NOV"
harus_error(lambda: app.tambah_buku("B101", "X", "Y", "Z", 2020, "RAK-NOV"), "sudah dipakai")
harus_error(lambda: app.tambah_buku("B102", "X", "Y", "Z", 2020, "RAK-XXX"), "tidak ditemukan")
harus_error(lambda: app.tambah_buku("B102", "", "Y", "Z", 2020, "RAK-NOV"), "Judul")
ubah = app.ubah_buku("B101", judul="Judul Diubah", tahun_terbit=2023)
assert app.cari_buku("B101").judul == "Judul Diubah" and app.daftar_buku.search("B101").tahun_terbit == 2023
assert app.cari_buku("B101") is app.daftar_buku.search("B101")       # Array dan BST sinkron
harus_error(lambda: app.ubah_buku("B101", id_rak="RAK-XXX"), "tidak ditemukan")
harus_error(lambda: app.ubah_buku("B999", judul="X"), "tidak ditemukan")
buku, rak = app.lokasi_buku("B001")
assert rak.id_rak == buku.id_rak
assert app.hapus_buku("B101").id_buku == "B101"
assert app.cari_buku("B101") is None and len(app.daftar_buku) == 100 and app.daftar_buku.search("B101") is None
harus_error(lambda: app.hapus_buku(buku_dipinjam), "sedang dipinjam")

# ---- anggota: hash table ----
assert app.cari_anggota("a001").id_anggota == "A001"
app.tambah_anggota("A101", "Anggota Baru", "081200000101")
assert len(app.tabel_anggota) == 101
harus_error(lambda: app.tambah_anggota("A101", "X", "Y"), "sudah dipakai")
assert app.hapus_anggota("A101").nama == "Anggota Baru" and app.cari_anggota("A101") is None
harus_error(lambda: app.hapus_anggota(peminjam), "masih meminjam")

# ---- pinjam, antre, kembalikan ----
status, hasil = app.pinjam(anggota_lain, buku_dipinjam)          # buku sedang dipinjam -> antre
assert status == "ANTRE" and hasil == 1
status, hasil = app.pinjam(anggota_lain2, buku_dipinjam)
assert status == "ANTRE" and hasil == 2
harus_error(lambda: app.pinjam(anggota_lain, buku_dipinjam), "sudah ada dalam antrean")
harus_error(lambda: app.pinjam(peminjam, buku_dipinjam), "sedang meminjam")
harus_error(lambda: app.pinjam("A999", "B001"), "Anggota A999")
harus_error(lambda: app.pinjam("A001", "B999"), "Buku B999")
assert len(app.antrean_untuk(buku_dipinjam)) == 2

lama, baru_trx = app.kembalikan(buku_dipinjam, "2026-11-12")      # FIFO: anggota_lain dilayani
assert not lama.sedang_dipinjam() and lama.tanggal_kembali == "2026-11-12"
assert baru_trx.id_anggota == anggota_lain and baru_trx.sedang_dipinjam()
assert len(app.antrean_untuk(buku_dipinjam)) == 1
assert app.pinjaman_aktif.search(buku_dipinjam) is baru_trx
harus_error(lambda: app.kembalikan("B001"), "tidak sedang dipinjam")   # B001 tidak dipinjam di data

# ---- pinjam normal + undo (Stack) ----
buku_bebas = next(x.id_buku for x in app.daftar_buku if app.pinjaman_aktif.search(x.id_buku) is None)
jumlah_awal = len(app.riwayat)
status, t = app.pinjam("A050", buku_bebas, "2026-11-12")
assert status == "DIPINJAM" and len(app.riwayat) == jumlah_awal + 1 and t.id_transaksi == "T102"
aksi = app.batalkan_aksi_terakhir()                              # urutan LIFO: PINJAM terakhir dulu
assert aksi.jenis == "PINJAM" and len(app.riwayat) == jumlah_awal
assert app.pinjaman_aktif.search(buku_bebas) is None
aksi = app.batalkan_aksi_terakhir()                              # sekarang PINJAM otomatis dari antrean
assert aksi.jenis == "PINJAM" and aksi.transaksi.id_anggota == anggota_lain
aksi = app.batalkan_aksi_terakhir()                              # lalu KEMBALI
assert aksi.jenis == "KEMBALI" and aksi.transaksi.sedang_dipinjam()
assert app.pinjaman_aktif.search(buku_dipinjam) is aksi.transaksi
harus_error(lambda: app.kembalikan(buku_dipinjam, "2020-01-01"), "lebih awal")

# ---- riwayat ----
assert all(x.id_anggota == "A004" for x in app.riwayat_anggota("a004"))
harus_error(lambda: app.riwayat_anggota("A999"), "tidak ditemukan")

# ---- graph rak ----
rute, total = app.rute_rak("rak-kom", "RAK-JUR")
assert rute[0] == "RAK-KOM" and rute[-1] == "RAK-JUR" and total > 0
assert len(app.graph_rak.bfs("RAK-KOM")) == 5 and len(app.graph_rak.dfs("RAK-KOM")) == 5
harus_error(lambda: app.rute_rak("RAK-KOM", "RAK-XXX"), "harus ada")

# ---- undo sampai habis ----
while not app.riwayat_aksi.is_empty():
    try:
        app.batalkan_aksi_terakhir()
    except ValueError:
        break
print("SEMUA TES APLIKASI LULUS")