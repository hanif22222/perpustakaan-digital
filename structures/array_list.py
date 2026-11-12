"""Array Dinamis buatan sendiri (kapasitas bertambah otomatis).

Dipakai pada fitur: penyimpanan koleksi buku dan data anggota.
Yang dibuat sendiri: penggandaan kapasitas (resizing), penggeseran elemen saat
sisip/hapus, dan pencarian linear.
list Python hanya dipakai sebagai penampung array berukuran tetap ([None] * kapasitas);
append, pop, insert, remove, dan sort bawaan tidak dipakai.
"""


class DynamicArray:
    """ADT Array Dinamis: elemen berurutan, diakses lewat index.

    Args:
        kapasitas_awal: kapasitas awal array (bilangan bulat positif).
        key_func: fungsi pengambil key dari sebuah item, dipakai search dan delete.
            Contoh: DynamicArray(key_func=lambda buku: buku.id_buku)
    """

    KAPASITAS_MINIMAL = 4

    def __init__(self, kapasitas_awal=KAPASITAS_MINIMAL, key_func=None):
        if not isinstance(kapasitas_awal, int) or kapasitas_awal < 1:
            raise ValueError("Kapasitas awal harus bilangan bulat positif.")
        self._data = [None] * kapasitas_awal
        self._ukuran = 0
        self._key = key_func if key_func is not None else (lambda item: item)

    # ---------- informasi ----------
    def size(self):
        return self._ukuran

    def __len__(self):
        return self._ukuran

    def kapasitas(self):
        return len(self._data)

    def is_empty(self):
        return self._ukuran == 0

    def __iter__(self):
        for i in range(self._ukuran):
            yield self._data[i]

    def __getitem__(self, index):
        return self.get(index)

    # ---------- bantu ----------
    def _ubah_kapasitas(self, kapasitas_baru):
        """Menyalin semua elemen ke array baru berukuran kapasitas_baru. O(n)."""
        baru = [None] * kapasitas_baru
        for i in range(self._ukuran):
            baru[i] = self._data[i]
        self._data = baru

    def _cek_index(self, index):
        if not isinstance(index, int) or index < 0 or index >= self._ukuran:
            raise IndexError(f"Index {index} di luar jangkauan (ukuran {self._ukuran}).")

    # ---------- operasi utama ----------
    def insert(self, item):
        """Menambah item di akhir. O(1) amortized (kadang O(n) saat kapasitas digandakan)."""
        if self._ukuran == len(self._data):
            self._ubah_kapasitas(len(self._data) * 2)
        self._data[self._ukuran] = item
        self._ukuran += 1

    def insert_at(self, index, item):
        """Menyisipkan item di posisi tertentu, elemen sesudahnya digeser. O(n)."""
        if not isinstance(index, int) or index < 0 or index > self._ukuran:
            raise IndexError(f"Index {index} tidak valid untuk penyisipan.")
        if self._ukuran == len(self._data):
            self._ubah_kapasitas(len(self._data) * 2)
        for i in range(self._ukuran, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = item
        self._ukuran += 1

    def get(self, index):
        """Mengakses item pada index. O(1).

        Raises:
            IndexError: jika index di luar jangkauan.
        """
        self._cek_index(index)
        return self._data[index]

    def set(self, index, item):
        """Mengubah item pada index. O(1).

        Raises:
            IndexError: jika index di luar jangkauan.
        """
        self._cek_index(index)
        self._data[index] = item

    def index_of(self, key):
        """Pencarian linear. Mengembalikan index, atau -1 jika tidak ada.

        Best O(1) (di depan), average dan worst O(n).
        """
        for i in range(self._ukuran):
            if self._key(self._data[i]) == key:
                return i
        return -1

    def search(self, key):
        """Mengembalikan item dengan key tersebut, atau None jika tidak ada. O(n)."""
        i = self.index_of(key)
        return self._data[i] if i != -1 else None

    def delete_at(self, index):
        """Menghapus item pada index lalu menggeser elemen sesudahnya. O(n).

        Mengembalikan item yang dihapus.
        Raises:
            IndexError: jika index di luar jangkauan.
        """
        self._cek_index(index)
        item = self._data[index]
        for i in range(index, self._ukuran - 1):
            self._data[i] = self._data[i + 1]
        self._data[self._ukuran - 1] = None
        self._ukuran -= 1
        if (len(self._data) > self.KAPASITAS_MINIMAL
                and self._ukuran <= len(self._data) // 4):
            self._ubah_kapasitas(len(self._data) // 2)
        return item

    def delete(self, key):
        """Menghapus item berdasarkan key. Mengembalikan True jika berhasil, False jika tidak ada. O(n)."""
        i = self.index_of(key)
        if i == -1:
            return False
        self.delete_at(i)
        return True

    def display(self):
        """Mencetak isi array. O(n)."""
        print(f"Array Dinamis: n={self._ukuran}, kapasitas={len(self._data)}")
        if self.is_empty():
            print("  (kosong)")
            return
        for i in range(self._ukuran):
            print(f"  [{i}] {self._data[i]}")


if __name__ == "__main__":
    print("=== Demo Array Dinamis: koleksi buku ===")
    koleksi = DynamicArray(key_func=lambda buku: buku[0])

    print("\n1) Tambah 6 buku (perhatikan kapasitas bertambah):")
    for nomor in range(1, 7):
        koleksi.insert((f"B{nomor:05d}", f"Buku Contoh {nomor}"))
        print(f"  insert B{nomor:05d} -> n={koleksi.size()}, kapasitas={koleksi.kapasitas()}")
    koleksi.display()

    print("\n2) Akses dan ubah:")
    print(f"  get(2)  -> {koleksi.get(2)}")
    koleksi.set(2, ("B00003", "Judul Diperbarui"))
    print(f"  set(2)  -> {koleksi.get(2)}")

    print("\n3) Sisip di posisi 1:")
    koleksi.insert_at(1, ("B00099", "Buku Sisipan"))
    koleksi.display()

    print("\n4) Search dan delete:")
    print(f"  search B00005 -> {koleksi.search('B00005')}")
    print(f"  search B77777 -> {koleksi.search('B77777')}  (tidak ditemukan)")
    print(f"  delete B00099 -> {koleksi.delete('B00099')}")
    print(f"  delete B00099 lagi -> {koleksi.delete('B00099')}  (sudah tidak ada)")
    koleksi.display()

    print("\n5) Validasi index:")
    try:
        koleksi.get(50)
    except IndexError as e:
        print(f"  Error ditangani: {e}")