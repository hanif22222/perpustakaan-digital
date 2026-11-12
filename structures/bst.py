"""Binary Search Tree (BST) buatan sendiri.

Dipakai pada fitur: data buku berdasarkan ID Buku (key = id_buku).
Aturan penempatan: key lebih kecil ke kiri, key lebih besar ke kanan, tidak ada key kembar.
Yang dibuat sendiri: node, insert, search, delete, preorder, inorder, postorder, tinggi.

Catatan implementasi:
- insert, search, delete ditulis ITERATIF (perulangan) agar aman untuk pohon miring
  yang dalam (tidak kena RecursionError).
- Traversal, tinggi, dan display ditulis rekursif agar mudah dibaca. Untuk pohon
  miring, panggil hanya pada data kecil (kedalaman di bawah sekitar 900).
"""


class Node:
    """Satu simpul BST: menyimpan key, value, dan penunjuk ke anak kiri dan kanan."""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.kiri = None
        self.kanan = None


class BST:
    """ADT Binary Search Tree dengan key berupa string (misalnya 'B00042')."""

    def __init__(self):
        self._root = None
        self._ukuran = 0

    @staticmethod
    def _cek_key(key):
        if not isinstance(key, str) or key.strip() == "":
            raise ValueError("Key harus berupa string yang tidak kosong.")

    def size(self):
        return self._ukuran

    def __len__(self):
        return self._ukuran

    def is_empty(self):
        return self._root is None

    # ---------- insert, search, delete ----------
    def insert(self, key, value):
        """Menambah (key, value). Jika key sudah ada, value diperbarui.

        Rata-rata O(log n); terburuk O(n) bila pohon miring (skewed).
        Mengembalikan True jika key baru, False jika hanya memperbarui.
        """
        self._cek_key(key)
        if self._root is None:
            self._root = Node(key, value)
            self._ukuran += 1
            return True
        saat_ini = self._root
        while True:
            if key == saat_ini.key:
                saat_ini.value = value
                return False
            if key < saat_ini.key:
                if saat_ini.kiri is None:
                    saat_ini.kiri = Node(key, value)
                    break
                saat_ini = saat_ini.kiri
            else:
                if saat_ini.kanan is None:
                    saat_ini.kanan = Node(key, value)
                    break
                saat_ini = saat_ini.kanan
        self._ukuran += 1
        return True

    def search(self, key):
        """Mencari value berdasarkan key. Mengembalikan None jika tidak ada.

        Rata-rata O(log n); terburuk O(n).
        """
        self._cek_key(key)
        saat_ini = self._root
        while saat_ini is not None:
            if key == saat_ini.key:
                return saat_ini.value
            saat_ini = saat_ini.kiri if key < saat_ini.key else saat_ini.kanan
        return None

    def delete(self, key):
        """Menghapus key. Mengembalikan True jika berhasil, False jika tidak ditemukan.

        Tiga kasus: (1) daun, (2) satu anak, (3) dua anak -> diganti inorder successor
        (key terkecil di subtree kanan). Rata-rata O(log n); terburuk O(n).
        """
        self._cek_key(key)
        induk = None
        saat_ini = self._root
        while saat_ini is not None and saat_ini.key != key:
            induk = saat_ini
            saat_ini = saat_ini.kiri if key < saat_ini.key else saat_ini.kanan
        if saat_ini is None:
            return False

        # Kasus dua anak: salin data successor, lalu yang dilepas adalah node
        # successor itu (pasti tidak punya anak kiri).
        if saat_ini.kiri is not None and saat_ini.kanan is not None:
            induk_successor = saat_ini
            successor = saat_ini.kanan
            while successor.kiri is not None:
                induk_successor = successor
                successor = successor.kiri
            saat_ini.key, saat_ini.value = successor.key, successor.value
            induk, saat_ini = induk_successor, successor

        # Kasus daun / satu anak: sambungkan induk langsung ke anak (atau None).
        anak = saat_ini.kiri if saat_ini.kiri is not None else saat_ini.kanan
        if induk is None:
            self._root = anak
        elif induk.kiri is saat_ini:
            induk.kiri = anak
        else:
            induk.kanan = anak
        self._ukuran -= 1
        return True

    # ---------- traversal (mengembalikan list key) ----------
    def preorder(self):
        """Akar -> kiri -> kanan. O(n)."""
        hasil = []
        self._preorder(self._root, hasil)
        return hasil

    def inorder(self):
        """Kiri -> akar -> kanan. Hasilnya selalu terurut naik. O(n)."""
        hasil = []
        self._inorder(self._root, hasil)
        return hasil

    def postorder(self):
        """Kiri -> kanan -> akar. O(n)."""
        hasil = []
        self._postorder(self._root, hasil)
        return hasil

    def items_inorder(self):
        """Daftar pasangan (key, value) terurut menurut key. O(n)."""
        hasil = []
        self._items(self._root, hasil)
        return hasil

    def _preorder(self, node, hasil):
        if node is not None:
            hasil.append(node.key)
            self._preorder(node.kiri, hasil)
            self._preorder(node.kanan, hasil)

    def _inorder(self, node, hasil):
        if node is not None:
            self._inorder(node.kiri, hasil)
            hasil.append(node.key)
            self._inorder(node.kanan, hasil)

    def _postorder(self, node, hasil):
        if node is not None:
            self._postorder(node.kiri, hasil)
            self._postorder(node.kanan, hasil)
            hasil.append(node.key)

    def _items(self, node, hasil):
        if node is not None:
            self._items(node.kiri, hasil)
            hasil.append((node.key, node.value))
            self._items(node.kanan, hasil)

    # ---------- bentuk pohon ----------
    def tinggi(self):
        """Tinggi pohon dalam jumlah level. Pohon kosong = 0, pohon miring = n."""
        return self._tinggi(self._root)

    def _tinggi(self, node):
        if node is None:
            return 0
        return 1 + max(self._tinggi(node.kiri), self._tinggi(node.kanan))

    def display(self):
        """Mencetak bentuk pohon dimiringkan 90 derajat: akar paling kiri,
        cabang kanan di atas, cabang kiri di bawah. O(n)."""
        if self.is_empty():
            print("BST kosong.")
            return
        print(f"BST (n={self._ukuran}, tinggi={self.tinggi()}), akar di kiri:")
        self._cetak(self._root, 0)

    def _cetak(self, node, level):
        if node is not None:
            self._cetak(node.kanan, level + 1)
            print("      " * level + node.key)
            self._cetak(node.kiri, level + 1)


if __name__ == "__main__":
    def kode(nomor):
        return f"B{nomor:05d}"

    print("=== Demo BST: data buku berdasarkan ID Buku ===")
    pohon = BST()

    print("\n1) Insert 7 buku:")
    for nomor in [50, 30, 70, 20, 40, 60, 80]:
        pohon.insert(kode(nomor), f"Buku Contoh {nomor}")
        print(f"  insert {kode(nomor)}")
    pohon.display()

    print("\n2) Tiga traversal:")
    print(f"  Preorder : {' '.join(pohon.preorder())}")
    print(f"  Inorder  : {' '.join(pohon.inorder())}  (terurut naik)")
    print(f"  Postorder: {' '.join(pohon.postorder())}")

    print("\n3) Search:")
    print(f"  search {kode(60)} -> {pohon.search(kode(60))}")
    print(f"  search {kode(99)} -> {pohon.search(kode(99))}  (tidak ditemukan)")

    print("\n4) Insert key yang sudah ada (value diperbarui):")
    print(f"  insert {kode(60)} -> {pohon.insert(kode(60), 'Judul Diperbarui')}  (False = bukan key baru)")

    print("\n5) Delete tiga kasus:")
    print(f"  delete {kode(20)} (daun)       -> {pohon.delete(kode(20))}")
    print(f"  delete {kode(30)} (satu anak)  -> {pohon.delete(kode(30))}")
    print(f"  delete {kode(50)} (dua anak, akar) -> {pohon.delete(kode(50))}")
    print(f"  delete {kode(99)} (tidak ada)  -> {pohon.delete(kode(99))}")
    pohon.display()
    print(f"  Inorder setelah delete: {' '.join(pohon.inorder())}")

    print("\n6) Bentuk pohon: seimbang vs miring (15 data):")
    seimbang, miring = BST(), BST()
    for nomor in [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]:   # urutan level
        seimbang.insert(kode(nomor), nomor)
    for nomor in range(1, 16):                                            # urutan naik
        miring.insert(kode(nomor), nomor)
    print(f"  Urutan seimbang: tinggi = {seimbang.tinggi()}  (mencari paling banyak 4 langkah)")
    print(f"  Urutan naik    : tinggi = {miring.tinggi()}  (seperti linked list, mencari sampai 15 langkah)")

    print("\n7) Validasi input:")
    try:
        pohon.insert("", "kosong")
    except ValueError as e:
        print(f"  Error ditangani: {e}")