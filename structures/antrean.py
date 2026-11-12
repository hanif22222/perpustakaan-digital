"""Queue (FIFO) buatan sendiri menggunakan node bertaut dengan penunjuk front dan rear.

Dipakai pada fitur: antrean peminjaman buku yang stoknya habis.
Nama file 'antrean.py' (bukan 'queue.py') agar tidak bentrok dengan modul bawaan Python.
Tidak memakai collections.deque maupun list.pop(0).
"""


class Node:
    """Satu elemen queue: menyimpan data dan penunjuk ke elemen di belakangnya."""

    def __init__(self, data):
        self.data = data
        self.berikutnya = None


class Queue:
    """ADT Queue: masuk lewat belakang (rear), keluar lewat depan (front)."""

    def __init__(self):
        self._front = None
        self._rear = None
        self._ukuran = 0

    def enqueue(self, data):
        """Menambah data di belakang antrean. O(1) berkat penunjuk rear."""
        baru = Node(data)
        if self.is_empty():
            self._front = baru
        else:
            self._rear.berikutnya = baru
        self._rear = baru
        self._ukuran += 1

    def dequeue(self):
        """Mengambil dan mengembalikan data paling depan. O(1).

        Raises:
            IndexError: jika queue kosong.
        """
        if self.is_empty():
            raise IndexError("Queue kosong, tidak ada yang bisa di-dequeue.")
        data = self._front.data
        self._front = self._front.berikutnya
        if self._front is None:
            self._rear = None
        self._ukuran -= 1
        return data

    def front(self):
        """Melihat data paling depan tanpa mengambilnya. O(1).

        Raises:
            IndexError: jika queue kosong.
        """
        if self.is_empty():
            raise IndexError("Queue kosong, tidak ada data di depan.")
        return self._front.data

    def is_empty(self):
        return self._front is None

    def size(self):
        return self._ukuran

    def __len__(self):
        return self._ukuran

    def display(self):
        """Mencetak isi queue dari depan ke belakang. O(n)."""
        if self.is_empty():
            print("Queue kosong.")
            return
        print("Queue (depan di atas):")
        saat_ini = self._front
        nomor = 1
        while saat_ini is not None:
            penanda = "  <- front" if nomor == 1 else ""
            print(f"  {nomor}. {saat_ini.data}{penanda}")
            saat_ini = saat_ini.berikutnya
            nomor += 1


if __name__ == "__main__":
    print("=== Demo Queue: bukti prinsip FIFO ===")
    antrean = Queue()
    for peminjam in [("A00003", "B00042"), ("A00010", "B00042"), ("A00007", "B00042")]:
        antrean.enqueue(peminjam)
        print(f"enqueue {peminjam}")
    antrean.display()
    print(f"front   -> {antrean.front()}")
    print(f"dequeue -> {antrean.dequeue()}  (masuk duluan, keluar duluan)")
    print(f"dequeue -> {antrean.dequeue()}")
    antrean.display()
    print(f"ukuran sekarang: {antrean.size()}")
    antrean.dequeue()
    try:
        antrean.dequeue()
    except IndexError as e:
        print(f"Error ditangani: {e}")
