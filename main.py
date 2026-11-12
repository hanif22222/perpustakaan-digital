"""Aplikasi CLI Sistem Manajemen Perpustakaan Digital (UAS Struktur Data, Kelompok 1).

Jalankan dari folder paling luar project:  python main.py
Logika aplikasi ada di perpustakaan.py; file ini hanya menampilkan menu dan membaca input.
"""

from perpustakaan import Perpustakaan
from structures.antrean import Queue
from structures.bst import BST
from structures.graph import Graph
from structures.hash_table import HashTable
from structures.stack import Stack

UKURAN_HALAMAN = 20


# ---------------- bantuan input ----------------
def tanya(pesan):
    return input(pesan).strip()


def tanya_angka(pesan):
    teks = tanya(pesan)
    try:
        return int(teks)
    except ValueError:
        raise ValueError(f"'{teks}' bukan angka bulat.") from None


def tanya_opsional(pesan):
    """Input yang boleh dikosongkan (Enter = tidak diubah). Mengembalikan None jika kosong."""
    teks = tanya(pesan)
    return teks if teks else None


def garis(judul):
    print(f"\n=== {judul} ===")


def jalankan(aksi, app):
    """Menjalankan satu aksi menu; pesan kesalahan input ditampilkan, program tidak berhenti."""
    try:
        aksi(app)
    except ValueError as e:
        print(f"[!] {e}")
    except IndexError as e:
        print(f"[!] {e}")


# ---------------- menu 1: buku (Array + BST) ----------------
def lihat_semua_buku(app):
    total = len(app.daftar_buku)
    print(f"Total {total} buku (dibaca dari Array Dinamis, {UKURAN_HALAMAN} per halaman)")
    for i in range(total):
        print(f"  {i + 1:3d}. {app.daftar_buku.get(i)}")
        if (i + 1) % UKURAN_HALAMAN == 0 and i + 1 < total:
            if tanya("   [Enter] lanjut, [q] berhenti: ").lower() == "q":
                break


def cari_buku(app):
    id_buku = tanya("ID Buku: ")
    buku = app.cari_buku(id_buku)
    print(buku if buku else f"Buku {id_buku.upper()} tidak ditemukan.")
    if buku:
        status = "sedang dipinjam" if app.pinjaman_aktif.search(buku.id_buku) else "tersedia"
        print(f"  Status: {status}")


def tambah_buku(app):
    buku = app.tambah_buku(tanya("ID Buku (contoh B101): "), tanya("Judul: "),
                           tanya("Penulis: "), tanya("Kategori: "),
                           tanya_angka("Tahun terbit: "), tanya("ID Rak (contoh RAK-NOV): "))
    print(f"Berhasil ditambahkan: {buku}")


def ubah_buku(app):
    id_buku = tanya("ID Buku yang diubah: ")
    print("Kosongkan (Enter) bagian yang tidak ingin diubah.")
    judul = tanya_opsional("Judul baru: ")
    penulis = tanya_opsional("Penulis baru: ")
    kategori = tanya_opsional("Kategori baru: ")
    tahun_teks = tanya_opsional("Tahun terbit baru: ")
    tahun = None
    if tahun_teks is not None:
        try:
            tahun = int(tahun_teks)
        except ValueError:
            raise ValueError(f"'{tahun_teks}' bukan angka bulat.") from None
    id_rak = tanya_opsional("ID Rak baru: ")
    print(f"Berhasil diubah: {app.ubah_buku(id_buku, judul, penulis, kategori, tahun, id_rak)}")


def hapus_buku(app):
    print(f"Berhasil dihapus: {app.hapus_buku(tanya('ID Buku yang dihapus: '))}")


def lokasi_buku(app):
    buku, rak = app.lokasi_buku(tanya("ID Buku: "))
    print(buku)
    print(f"  Lokasi: {rak}")


def menu_buku(app):
    pilihan_menu = {"1": lihat_semua_buku, "2": cari_buku, "3": tambah_buku,
                    "4": ubah_buku, "5": hapus_buku, "6": lokasi_buku}
    while True:
        garis("KELOLA BUKU (Array Dinamis + BST)")
        print("1. Lihat semua buku (Array)\n2. Cari buku berdasarkan ID (BST)\n3. Tambah buku"
              "\n4. Ubah data buku\n5. Hapus buku\n6. Lokasi rak sebuah buku\n0. Kembali")
        pilihan = tanya("Pilih: ")
        if pilihan == "0":
            return
        if pilihan in pilihan_menu:
            jalankan(pilihan_menu[pilihan], app)
        else:
            print("[!] Pilihan tidak valid.")


# ---------------- menu 2: anggota (Hash Table) ----------------
def cari_anggota(app):
    id_anggota = tanya("ID Anggota: ")
    anggota = app.cari_anggota(id_anggota)
    if anggota is None:
        print(f"Anggota {id_anggota.upper()} tidak ditemukan.")
        return
    tabel = app.tabel_anggota
    hash_nilai = HashTable.hash_kunci(anggota.id_anggota)
    print(anggota)
    print(f"  Hash('{anggota.id_anggota}') = {hash_nilai}, "
          f"indeks slot = {hash_nilai} mod {tabel.kapasitas()} = {hash_nilai % tabel.kapasitas()}")


def tambah_anggota(app):
    anggota = app.tambah_anggota(tanya("ID Anggota (contoh A101): "), tanya("Nama: "),
                                 tanya("Kontak: "))
    print(f"Berhasil ditambahkan: {anggota}")


def hapus_anggota(app):
    print(f"Berhasil dihapus: {app.hapus_anggota(tanya('ID Anggota yang dihapus: '))}")


def info_hash_table(app):
    tabel = app.tabel_anggota
    print(f"Hash Table anggota: n = {tabel.size()}, m = {tabel.kapasitas()}, "
          f"load factor = n/m = {tabel.load_factor():.2f}")
    print(f"  Collision saat insert : {tabel.jumlah_collision()}")
    print(f"  Jumlah resizing       : {tabel.jumlah_resize()}")
    print(f"  Rantai terpanjang     : {tabel.rantai_terpanjang()}")


def menu_anggota(app):
    pilihan_menu = {"1": cari_anggota, "2": tambah_anggota, "3": hapus_anggota,
                    "4": info_hash_table}
    while True:
        garis("KELOLA ANGGOTA (Hash Table)")
        print("1. Cari anggota berdasarkan ID\n2. Tambah anggota\n3. Hapus anggota"
              "\n4. Info Hash Table (load factor, collision, resizing)\n0. Kembali")
        pilihan = tanya("Pilih: ")
        if pilihan == "0":
            return
        if pilihan in pilihan_menu:
            jalankan(pilihan_menu[pilihan], app)
        else:
            print("[!] Pilihan tidak valid.")


# ---------------- menu 3: peminjaman (Linked List + Stack + Queue) ----------------
def pinjam_buku(app):
    status, hasil = app.pinjam(tanya("ID Anggota: "), tanya("ID Buku: "))
    if status == "DIPINJAM":
        print(f"Peminjaman berhasil: {hasil}")
    else:
        print(f"Buku sedang dipinjam anggota lain. Anda masuk antrean (Queue) pada posisi {hasil}.")


def kembalikan_buku(app):
    selesai, berikutnya = app.kembalikan(tanya("ID Buku yang dikembalikan: "))
    print(f"Pengembalian berhasil: {selesai}")
    if berikutnya:
        print(f"Antrean dilayani (FIFO), anggota terdepan otomatis meminjam:\n  {berikutnya}")


def batalkan_aksi(app):
    aksi = app.batalkan_aksi_terakhir()
    print(f"Aksi dibatalkan (LIFO, aksi terakhir lebih dulu): {aksi}")


def lihat_aksi(app):
    app.riwayat_aksi.display()


def lihat_riwayat(app):
    pilihan = tanya("[1] 10 transaksi terakhir  [2] Riwayat satu anggota: ")
    if pilihan == "2":
        daftar = app.riwayat_anggota(tanya("ID Anggota: "))
        print(f"{len(daftar)} transaksi:")
    else:
        semua = list(app.riwayat)
        daftar = semua[-10:]
        print(f"10 transaksi terakhir dari {len(semua)} (Linked List):")
    for transaksi in daftar:
        print(f"  {transaksi}")


def lihat_antrean(app):
    antrean = app.antrean_untuk(tanya("ID Buku: "))
    if antrean is None:
        print("Tidak ada antrean untuk buku ini.")
    else:
        antrean.display()


def lihat_dipinjam(app):
    daftar = app.daftar_dipinjam()
    print(f"{len(daftar)} buku sedang dipinjam:")
    for transaksi in daftar:
        print(f"  {transaksi}")


def menu_peminjaman(app):
    pilihan_menu = {"1": pinjam_buku, "2": kembalikan_buku, "3": batalkan_aksi,
                    "4": lihat_aksi, "5": lihat_riwayat, "6": lihat_antrean,
                    "7": lihat_dipinjam}
    while True:
        garis("PEMINJAMAN (Linked List + Stack + Queue)")
        print("1. Pinjam buku\n2. Kembalikan buku\n3. Batalkan aksi terakhir (Stack, undo)"
              "\n4. Lihat riwayat aksi (isi Stack)\n5. Lihat riwayat transaksi (Linked List)"
              "\n6. Lihat antrean sebuah buku (Queue)\n7. Daftar buku yang sedang dipinjam\n0. Kembali")
        pilihan = tanya("Pilih: ")
        if pilihan == "0":
            return
        if pilihan in pilihan_menu:
            jalankan(pilihan_menu[pilihan], app)
        else:
            print("[!] Pilihan tidak valid.")


# ---------------- menu 4: rak (Graph) ----------------
def daftar_rak(app):
    for rak in app.daftar_rak:
        print(f"  {rak}")


def tampil_graph(app):
    app.graph_rak.display()
    print("Jenis graph utama: tidak berarah (orang berjalan dua arah antar rak) dan "
          "berbobot (jarak dalam meter).")


def telusuri(app, nama, fungsi):
    awal = tanya("Rak awal (contoh RAK-KOM): ").upper()
    print(f"{nama} dari {awal}: {' -> '.join(fungsi(awal))}")


def bfs_rak(app):
    telusuri(app, "BFS", app.graph_rak.bfs)


def dfs_rak(app):
    telusuri(app, "DFS", app.graph_rak.dfs)


def rute_rak(app):
    rute, total = app.rute_rak(tanya("Rak asal: "), tanya("Rak tujuan: "))
    if rute is None:
        print("Tidak ada rute antar kedua rak.")
    else:
        print(f"Rute dengan langkah paling sedikit: {' -> '.join(rute)} (total jarak {total} m)")


def menu_rak(app):
    pilihan_menu = {"1": daftar_rak, "2": tampil_graph, "3": bfs_rak, "4": dfs_rak, "5": rute_rak}
    while True:
        garis("RAK DAN GRAPH (Adjacency List, BFS, DFS)")
        print("1. Daftar rak\n2. Tampilkan graph (adjacency list)\n3. Telusuri BFS"
              "\n4. Telusuri DFS\n5. Cari rute antar rak\n0. Kembali")
        pilihan = tanya("Pilih: ")
        if pilihan == "0":
            return
        if pilihan in pilihan_menu:
            jalankan(pilihan_menu[pilihan], app)
        else:
            print("[!] Pilihan tidak valid.")


# ---------------- menu 5: demo struktur data ----------------
def demo_bst(app):
    pohon = app.pohon_buku
    garis("DEMO BST (data buku, key = ID Buku)")
    print(f"Jumlah node = {pohon.size()}, tinggi pohon = {pohon.tinggi()} level")
    print("\nPreorder (akar, kiri, kanan):\n ", " ".join(pohon.preorder()))
    print("\nInorder (kiri, akar, kanan; selalu terurut):\n ", " ".join(pohon.inorder()))
    print("\nPostorder (kiri, kanan, akar):\n ", " ".join(pohon.postorder()))
    if tanya("\nTampilkan bentuk pohon (panjang)? [y/N]: ").lower() == "y":
        pohon.display()
    print("\nPerbandingan bentuk pohon, 15 data:")
    seimbang, miring = BST(), BST()
    for nomor in [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]:
        seimbang.insert(f"B{nomor:03d}", nomor)
    for nomor in range(1, 16):
        miring.insert(f"B{nomor:03d}", nomor)
    print(f"  Dimasukkan berurutan seimbang: tinggi {seimbang.tinggi()} (balanced, cari <= 4 langkah)")
    print(f"  Dimasukkan urut naik         : tinggi {miring.tinggi()} (skewed, cari sampai 15 langkah)")


def demo_hash_table(app):
    garis("DEMO HASH TABLE (tabel kecil, m = 5)")
    tabel = HashTable(kapasitas=5)
    # A001, A006, dan A011 sengaja dipilih: nilai hash-nya selisih kelipatan 5, sehingga
    # pada m = 5 (juga m = 10) mendapat indeks slot yang sama -> terjadi COLLISION.
    for id_anggota in ["A001", "A006", "A002", "A003", "A011", "A004", "A005", "A007"]:
        sebelum = tabel.jumlah_collision()
        tabel.insert(id_anggota, f"Anggota {id_anggota}")
        indeks = HashTable.hash_kunci(id_anggota) % tabel.kapasitas()
        tanda = "  <- COLLISION (ditangani chaining)" if tabel.jumlah_collision() > sebelum else ""
        print(f"insert {id_anggota}: indeks {indeks}, n={tabel.size()}, m={tabel.kapasitas()}, "
              f"load factor={tabel.load_factor():.2f}{tanda}")
    tabel.display()
    print(f"Total collision: {tabel.jumlah_collision()}, jumlah resizing: {tabel.jumlah_resize()}")


def demo_stack_queue(app):
    garis("DEMO STACK (LIFO) DAN QUEUE (FIFO)")
    tumpukan, antrean = Stack(), Queue()
    for item in ["Aksi 1", "Aksi 2", "Aksi 3"]:
        tumpukan.push(item)
        antrean.enqueue(item)
    print("Dimasukkan berurutan: Aksi 1, Aksi 2, Aksi 3")
    print(f"Stack pop    -> {tumpukan.pop()} (terakhir masuk, pertama keluar)")
    print(f"Queue dequeue -> {antrean.dequeue()} (pertama masuk, pertama keluar)")
    tumpukan.display()
    antrean.display()


def demo_variasi_graph(app):
    garis("DEMO 4 VARIASI GRAPH (Pintu, R01, R02, Layanan)")
    for berarah, berbobot, judul in [(False, False, "tidak berarah, tidak berbobot"),
                                     (False, True, "tidak berarah, berbobot (jenis graph utama)"),
                                     (True, False, "berarah, tidak berbobot"),
                                     (True, True, "berarah, berbobot (jalur satu arah ke meja layanan)")]:
        print(f"\n[{judul}]")
        g = Graph(berarah=berarah, berbobot=berbobot)
        for nama in ["Pintu", "R01", "R02", "Layanan"]:
            g.tambah_simpul(nama)
        g.tambah_sisi("Pintu", "R01", 5)
        g.tambah_sisi("R01", "R02", 3)
        g.tambah_sisi("R02", "Layanan", 4)
        g.display()
        print(f"  BFS dari Pintu  : {' -> '.join(g.bfs('Pintu'))}")
        print(f"  BFS dari Layanan: {' -> '.join(g.bfs('Layanan'))}")


def menu_demo(app):
    pilihan_menu = {"1": demo_bst, "2": demo_hash_table, "3": demo_stack_queue,
                    "4": demo_variasi_graph}
    while True:
        garis("DEMO STRUKTUR DATA")
        print("1. BST dan tiga traversal\n2. Hash Table: collision, load factor, resizing"
              "\n3. Stack (LIFO) dan Queue (FIFO)\n4. Variasi graph (berarah/berbobot)\n0. Kembali")
        pilihan = tanya("Pilih: ")
        if pilihan == "0":
            return
        if pilihan in pilihan_menu:
            jalankan(pilihan_menu[pilihan], app)
        else:
            print("[!] Pilihan tidak valid.")


# ---------------- ringkasan dan menu utama ----------------
def tampil_ringkasan(app):
    r = app.ringkasan()
    garis("RINGKASAN DATA")
    print(f"Buku {r['buku']} | Anggota {r['anggota']} | Transaksi {r['transaksi']} | "
          f"Sedang dipinjam {r['sedang_dipinjam']} | Rak {r['rak']} | Aksi tercatat {r['aksi_tercatat']}")
    print(f"Tinggi BST buku: {app.pohon_buku.tinggi()} | "
          f"Load factor Hash Table anggota: {app.tabel_anggota.load_factor():.2f}")


def main():
    app = Perpustakaan()
    try:
        app.muat_data("data")
    except (FileNotFoundError, ValueError) as e:
        print(f"Gagal memuat data: {e}")
        print("Pastikan folder data/ berisi buku.csv, anggota.csv, transaksi.csv, rak.csv, koneksi_rak.csv")
        return

    print("=" * 52)
    print(" SISTEM MANAJEMEN PERPUSTAKAAN DIGITAL")
    print(" UAS Struktur Data - Kelompok 1")
    print("=" * 52)
    tampil_ringkasan(app)

    pilihan_menu = {"1": menu_buku, "2": menu_anggota, "3": menu_peminjaman,
                    "4": menu_rak, "5": menu_demo, "6": tampil_ringkasan}
    try:
        while True:
            garis("MENU UTAMA")
            print("1. Kelola buku\n2. Kelola anggota\n3. Peminjaman dan pengembalian"
                  "\n4. Rak dan graph\n5. Demo struktur data\n6. Ringkasan data\n0. Keluar")
            pilihan = tanya("Pilih: ")
            if pilihan == "0":
                break
            if pilihan in pilihan_menu:
                pilihan_menu[pilihan](app)
            else:
                print("[!] Pilihan tidak valid.")
    except (EOFError, KeyboardInterrupt):
        print()
    print("Terima kasih. Program selesai.")


if __name__ == "__main__":
    main()