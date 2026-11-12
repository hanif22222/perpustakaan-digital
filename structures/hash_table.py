"""Hash Table buatan sendiri dengan collision handling chaining.

Dipakai pada fitur: pencarian anggota berdasarkan ID Anggota.
Yang dibuat sendiri: fungsi hash, penentuan indeks, chaining, load factor, resizing.
Tidak memakai dict, set, maupun hash() bawaan Python.
Satu-satunya bawaan yang dipakai hanyalah list sebagai penampung array dasar.
"""


class Node:
    """Satu elemen dalam rantai (chain) pada sebuah slot tabel."""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.berikutnya = None


class HashTable:
    """ADT Hash Table: menyimpan pasangan (key, value) dengan key berupa string."""

    BATAS_LOAD_FACTOR = 0.75   # resizing terjadi jika load factor melewati ini
    KAPASITAS_AWAL = 8

    def __init__(self, kapasitas=KAPASITAS_AWAL):
        if not isinstance(kapasitas, int) or kapasitas < 1:
            raise ValueError("Kapasitas harus bilangan bulat positif.")
        self._kapasitas = kapasitas
        self._slot = [None] * kapasitas   # tiap slot: kepala rantai (Node) atau None
        self._jumlah = 0                  # n = jumlah elemen
        self._collision = 0               # berapa kali collision terjadi saat insert
        self._jumlah_resize = 0

    # ---------- fungsi hash ----------
    @staticmethod
    def hash_kunci(key):
        """Mengubah string key menjadi bilangan bulat (polynomial rolling hash).

        h = (h * 31 + kode_karakter) mod 1.000.000.007, diulang untuk tiap karakter.
        """
        h = 0
        for karakter in key:
            h = (h * 31 + ord(karakter)) % 1_000_000_007
        return h

    def _indeks(self, key):
        """Indeks slot = hash(key) mod kapasitas."""
        return self.hash_kunci(key) % self._kapasitas

    @staticmethod
    def _cek_key(key):
        if not isinstance(key, str) or key.strip() == "":
            raise ValueError("Key harus berupa string yang tidak kosong.")

    # ---------- operasi utama ----------
    def insert(self, key, value):
        """Menambah (key, value). Jika key sudah ada, value diperbarui.

        Rata-rata O(1); terburuk O(n) bila semua key menumpuk di satu slot.
        Mengembalikan True jika key baru, False jika hanya memperbarui.
        """
        self._cek_key(key)
        i = self._indeks(key)
        saat_ini = self._slot[i]
        while saat_ini is not None:          # key sudah ada -> perbarui
            if saat_ini.key == key:
                saat_ini.value = value
                return False
            saat_ini = saat_ini.berikutnya

        baru = Node(key, value)
        if self._slot[i] is not None:        # slot sudah terisi key lain = collision
            self._collision += 1
        baru.berikutnya = self._slot[i]      # sambung di kepala rantai
        self._slot[i] = baru
        self._jumlah += 1

        if self.load_factor() > self.BATAS_LOAD_FACTOR:
            self._resize()
        return True

    def search(self, key):
        """Mencari value berdasarkan key. Mengembalikan None jika tidak ada.

        Rata-rata O(1); terburuk O(n).
        """
        self._cek_key(key)
        saat_ini = self._slot[self._indeks(key)]
        while saat_ini is not None:
            if saat_ini.key == key:
                return saat_ini.value
            saat_ini = saat_ini.berikutnya
        return None

    def delete(self, key):
        """Menghapus key. Mengembalikan True jika berhasil, False jika tidak ditemukan.

        Rata-rata O(1); terburuk O(n).
        """
        self._cek_key(key)
        i = self._indeks(key)
        sebelumnya = None
        saat_ini = self._slot[i]
        while saat_ini is not None:
            if saat_ini.key == key:
                if sebelumnya is None:
                    self._slot[i] = saat_ini.berikutnya
                else:
                    sebelumnya.berikutnya = saat_ini.berikutnya
                self._jumlah -= 1
                return True
            sebelumnya = saat_ini
            saat_ini = saat_ini.berikutnya
        return False

    # ---------- load factor dan resizing ----------
    def load_factor(self):
        """Load factor = n / m (jumlah elemen dibagi kapasitas)."""
        return self._jumlah / self._kapasitas

    def _resize(self):
        """Menggandakan kapasitas lalu menghitung ulang indeks semua elemen. O(n)."""
        kapasitas_lama = self._kapasitas
        slot_lama = self._slot
        self._kapasitas = kapasitas_lama * 2
        self._slot = [None] * self._kapasitas
        for kepala in slot_lama:
            saat_ini = kepala
            while saat_ini is not None:
                berikutnya = saat_ini.berikutnya      # simpan sebelum node dipindah
                i = self._indeks(saat_ini.key)        # indeks baru (m berubah)
                saat_ini.berikutnya = self._slot[i]
                self._slot[i] = saat_ini
                saat_ini = berikutnya
        self._jumlah_resize += 1
        print(f"[RESIZE] kapasitas {kapasitas_lama} -> {self._kapasitas} "
              f"(n={self._jumlah}, load factor sekarang {self.load_factor():.2f})")

    # ---------- informasi dan tampilan ----------
    def size(self):
        return self._jumlah

    def __len__(self):
        return self._jumlah

    def kapasitas(self):
        return self._kapasitas

    def jumlah_collision(self):
        return self._collision

    def jumlah_resize(self):
        return self._jumlah_resize

    def rantai_terpanjang(self):
        """Panjang rantai terpanjang saat ini (indikator sebaran hash)."""
        terpanjang = 0
        for kepala in self._slot:
            panjang = 0
            saat_ini = kepala
            while saat_ini is not None:
                panjang += 1
                saat_ini = saat_ini.berikutnya
            if panjang > terpanjang:
                terpanjang = panjang
        return terpanjang

    def display(self):
        """Mencetak isi tabel slot demi slot. O(m + n)."""
        print(f"Hash Table: n={self._jumlah}, m={self._kapasitas}, "
              f"load factor={self.load_factor():.2f}")
        for i in range(self._kapasitas):
            teks = f"  [{i:2d}]"
            saat_ini = self._slot[i]
            if saat_ini is None:
                teks += " kosong"
            while saat_ini is not None:
                teks += f" -> {saat_ini.key}"
                saat_ini = saat_ini.berikutnya
            print(teks)


if __name__ == "__main__":
    print("=== Demo Hash Table (chaining) ===")
    tabel = HashTable(kapasitas=5)

    print("\n1) Fungsi hash dan indeks (m = 5):")
    for id_anggota in ["A00001", "A00006"]:
        h = HashTable.hash_kunci(id_anggota)
        print(f"  {id_anggota}: hash = {h}, indeks = {h} mod 5 = {h % 5}")
    print("  -> A00001 dan A00006 mendapat indeks sama = akan terjadi COLLISION")

    print("\n2) Insert bertahap (perhatikan collision, load factor, resizing):")
    urutan = ["A00001", "A00006", "A00002", "A00003", "A00011", "A00004", "A00005"]
    for id_anggota in urutan:
        indeks = tabel._indeks(id_anggota)
        collision_sebelum = tabel.jumlah_collision()
        tabel.insert(id_anggota, f"Anggota {id_anggota}")
        tanda = "  <- COLLISION (chaining)" if tabel.jumlah_collision() > collision_sebelum else ""
        print(f"  insert {id_anggota} -> n={tabel.size()}, m={tabel.kapasitas()}, "
              f"load factor={tabel.load_factor():.2f}{tanda}")

    print("\n3) Isi tabel (cari slot yang punya rantai):")
    tabel.display()
    print(f"  total collision: {tabel.jumlah_collision()}, "
          f"rantai terpanjang: {tabel.rantai_terpanjang()}")

    print("\n4) Insert satu lagi sampai load factor melewati 0.75:")
    tabel.insert("A00007", "Anggota A00007")
    tabel.display()

    print("\n5) Search:")
    print(f"  search A00011 -> {tabel.search('A00011')}")
    print(f"  search A99999 -> {tabel.search('A99999')}  (tidak ditemukan)")

    print("\n6) Delete:")
    print(f"  delete A00011 -> {tabel.delete('A00011')}")
    print(f"  delete A00011 lagi -> {tabel.delete('A00011')}  (sudah tidak ada)")
    print(f"  search A00011 -> {tabel.search('A00011')}")
    print(f"  n sekarang = {tabel.size()}, load factor = {tabel.load_factor():.2f}")

    print("\n7) Validasi input:")
    try:
        tabel.insert("", "kosong")
    except ValueError as e:
        print(f"  Error ditangani: {e}")
