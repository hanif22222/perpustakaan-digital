"""Singly Linked List buatan sendiri dengan penunjuk head dan tail.

Dipakai pada fitur: riwayat peminjaman/pengembalian (data baru ditambah di akhir).
Yang dibuat sendiri: node, insert, search, delete, dan traversal.
Tidak memakai list.append/remove maupun collections.deque sebagai pengganti inti.
"""


class Node:
    """Satu elemen linked list: menyimpan data dan penunjuk ke elemen berikutnya."""

    def __init__(self, data):
        self.data = data
        self.berikutnya = None


class LinkedList:
    """ADT Linked List.

    Args:
        key_func: fungsi pengambil key dari sebuah data, dipakai search dan delete.
            Contoh: LinkedList(key_func=lambda t: t.id_transaksi)
    """

    def __init__(self, key_func=None):
        self._head = None
        self._tail = None
        self._ukuran = 0
        self._key = key_func if key_func is not None else (lambda data: data)

    def size(self):
        return self._ukuran

    def __len__(self):
        return self._ukuran

    def is_empty(self):
        return self._head is None

    # ---------- operasi utama ----------
    def insert(self, data):
        """Menambah data di akhir. O(1) berkat penunjuk tail."""
        baru = Node(data)
        if self.is_empty():
            self._head = baru
        else:
            self._tail.berikutnya = baru
        self._tail = baru
        self._ukuran += 1

    def insert_front(self, data):
        """Menambah data di awal. O(1)."""
        baru = Node(data)
        baru.berikutnya = self._head
        self._head = baru
        if self._tail is None:
            self._tail = baru
        self._ukuran += 1

    def search(self, key):
        """Mencari data berdasarkan key. Mengembalikan data, atau None jika tidak ada.

        Best O(1) (di head), average dan worst O(n).
        """
        saat_ini = self._head
        while saat_ini is not None:
            if self._key(saat_ini.data) == key:
                return saat_ini.data
            saat_ini = saat_ini.berikutnya
        return None

    def delete(self, key):
        """Menghapus node berdasarkan key. Mengembalikan True jika berhasil, False jika tidak ada.

        O(n) karena harus mencari dulu; penghapusan itu sendiri O(1).
        """
        sebelumnya = None
        saat_ini = self._head
        while saat_ini is not None:
            if self._key(saat_ini.data) == key:
                if sebelumnya is None:               # menghapus head
                    self._head = saat_ini.berikutnya
                else:
                    sebelumnya.berikutnya = saat_ini.berikutnya
                if saat_ini is self._tail:           # menghapus tail
                    self._tail = sebelumnya
                self._ukuran -= 1
                return True
            sebelumnya = saat_ini
            saat_ini = saat_ini.berikutnya
        return False

    def traverse(self):
        """Generator: menelusuri data dari head sampai tail. O(n)."""
        saat_ini = self._head
        while saat_ini is not None:
            yield saat_ini.data
            saat_ini = saat_ini.berikutnya

    def __iter__(self):
        return self.traverse()

    def display(self):
        """Mencetak isi linked list dari head ke tail. O(n)."""
        if self.is_empty():
            print("Linked List kosong.")
            return
        print(f"Linked List (n={self._ukuran}, head di atas):")
        for nomor, data in enumerate(self.traverse(), start=1):
            print(f"  {nomor}. {data}")


if __name__ == "__main__":
    print("=== Demo Linked List: riwayat peminjaman ===")
    riwayat = LinkedList(key_func=lambda t: t[0])

    print("\n1) Insert di akhir (urut kejadian):")
    for transaksi in [("T00001", "A00003", "B00042", "DIPINJAM"),
                      ("T00002", "A00010", "B00007", "DIPINJAM"),
                      ("T00003", "A00003", "B00042", "DIKEMBALIKAN")]:
        riwayat.insert(transaksi)
        print(f"  insert {transaksi[0]}")
    riwayat.display()

    print("\n2) Insert di depan:")
    riwayat.insert_front(("T00000", "A00001", "B00001", "DIKEMBALIKAN"))
    riwayat.display()

    print("\n3) Search:")
    print(f"  search T00002 -> {riwayat.search('T00002')}")
    print(f"  search T99999 -> {riwayat.search('T99999')}  (tidak ditemukan)")

    print("\n4) Delete (head, tengah, tail):")
    for key in ["T00000", "T00002", "T00003"]:
        print(f"  delete {key} -> {riwayat.delete(key)}")
    riwayat.display()
    print(f"  delete T00002 lagi -> {riwayat.delete('T00002')}  (sudah tidak ada)")

    print("\n5) Insert lagi setelah tail dihapus (tail harus tetap benar):")
    riwayat.insert(("T00004", "A00005", "B00009", "DIPINJAM"))
    riwayat.display()