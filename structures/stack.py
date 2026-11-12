"""Stack (LIFO) buatan sendiri menggunakan node bertaut (linked node).

Dipakai pada fitur: riwayat aksi terakhir / undo transaksi simulasi.
Tidak memakai list.append/pop maupun library bawaan sebagai pengganti inti.
"""


class Node:
    """Satu elemen stack: menyimpan data dan penunjuk ke elemen di bawahnya."""

    def __init__(self, data, berikutnya=None):
        self.data = data
        self.berikutnya = berikutnya


class Stack:
    """ADT Stack: tambah dan ambil hanya lewat satu ujung (top)."""

    def __init__(self):
        self._top = None
        self._ukuran = 0

    def push(self, data):
        """Menaruh data di puncak stack. O(1)."""
        self._top = Node(data, self._top)
        self._ukuran += 1

    def pop(self):
        """Mengambil dan mengembalikan data di puncak. O(1).

        Raises:
            IndexError: jika stack kosong.
        """
        if self.is_empty():
            raise IndexError("Stack kosong, tidak ada yang bisa di-pop.")
        data = self._top.data
        self._top = self._top.berikutnya
        self._ukuran -= 1
        return data

    def peek(self):
        """Melihat data di puncak tanpa mengambilnya. O(1).

        Raises:
            IndexError: jika stack kosong.
        """
        if self.is_empty():
            raise IndexError("Stack kosong, tidak ada data di puncak.")
        return self._top.data

    def is_empty(self):
        return self._top is None

    def size(self):
        return self._ukuran

    def __len__(self):
        return self._ukuran

    def display(self):
        """Mencetak isi stack dari puncak ke dasar. O(n)."""
        if self.is_empty():
            print("Stack kosong.")
            return
        print("Stack (puncak di atas):")
        saat_ini = self._top
        nomor = 1
        while saat_ini is not None:
            penanda = "  <- top" if nomor == 1 else ""
            print(f"  {nomor}. {saat_ini.data}{penanda}")
            saat_ini = saat_ini.berikutnya
            nomor += 1


if __name__ == "__main__":
    print("=== Demo Stack: bukti prinsip LIFO ===")
    riwayat = Stack()
    for aksi in [("PINJAM", "T00001"), ("PINJAM", "T00002"), ("KEMBALI", "T00001")]:
        riwayat.push(aksi)
        print(f"push {aksi}")
    riwayat.display()
    print(f"peek -> {riwayat.peek()}")
    print(f"pop  -> {riwayat.pop()}  (terakhir masuk, pertama keluar)")
    print(f"pop  -> {riwayat.pop()}")
    riwayat.display()
    print(f"ukuran sekarang: {riwayat.size()}")
    riwayat.pop()
    try:
        riwayat.pop()
    except IndexError as e:
        print(f"Error ditangani: {e}")
