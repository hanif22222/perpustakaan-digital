"""Tes otomatis untuk struktur data Hanif: DynamicArray, LinkedList, BST.
Jalankan dari folder paling luar project:  python tes_hanif.py
"""
import random
import time
from structures.array_list import DynamicArray
from structures.linked_list import LinkedList
from structures.bst import BST


def kode(n):
    return f"B{n:05d}"


# ---------- Array dinamis ----------
a = DynamicArray(key_func=lambda b: b[0])
for i in range(1, 11):
    a.insert((kode(i), f"Judul {i}"))
assert a.size() == 10 and a.kapasitas() == 16
assert a.search(kode(5))[1] == "Judul 5" and a.search("B99999") is None
a.set(0, (kode(1), "Judul Baru"))
assert a.get(0)[1] == "Judul Baru"
a.insert_at(2, ("B77777", "Sisipan"))
assert a.get(2)[0] == "B77777" and a.size() == 11
assert a.delete("B77777") is True and a.size() == 10
assert a.delete("B77777") is False
for index_salah in (50, -1):
    try:
        a.get(index_salah)
        assert False
    except IndexError:
        pass
for _ in range(9):
    a.delete_at(0)
assert a.size() == 1 and a.kapasitas() < 16

# ---------- Linked list ----------
ll = LinkedList(key_func=lambda t: t)
for x in ["T1", "T2", "T3", "T4"]:
    ll.insert(x)
ll.insert_front("T0")
assert list(ll) == ["T0", "T1", "T2", "T3", "T4"]
assert ll.search("T3") == "T3" and ll.search("T9") is None
assert ll.delete("T0") and ll.delete("T4") and ll.delete("T2")   # head, tail, tengah
assert ll.delete("T9") is False
ll.insert("T5")                                                  # tail harus tetap benar
assert list(ll) == ["T1", "T3", "T5"] and ll.size() == 3

# ---------- BST ----------
pohon = BST()
for n in [50, 30, 70, 20, 40, 60, 80]:
    assert pohon.insert(kode(n), f"v{n}") is True
K = kode
assert pohon.preorder() == [K(50), K(30), K(20), K(40), K(70), K(60), K(80)]
assert pohon.inorder() == [K(20), K(30), K(40), K(50), K(60), K(70), K(80)]
assert pohon.postorder() == [K(20), K(40), K(30), K(60), K(80), K(70), K(50)]
assert pohon.search(K(60)) == "v60" and pohon.search(K(99)) is None
assert pohon.tinggi() == 3
assert pohon.insert(K(50), "baru") is False and pohon.search(K(50)) == "baru"
assert pohon.size() == 7
assert pohon.delete(K(20)) and pohon.delete(K(30)) and pohon.delete(K(50))
assert pohon.delete(K(99)) is False
assert pohon.inorder() == [K(40), K(60), K(70), K(80)] and pohon.size() == 4
assert pohon.preorder()[0] == K(60)          # successor menjadi akar baru
for key_salah in ("", None, 5):
    try:
        pohon.insert(key_salah, "x")
        assert False
    except ValueError:
        pass

# acak: setelah banyak delete, inorder tetap terurut dan lengkap
rng = random.Random(42)
semua = [kode(i) for i in range(1, 2001)]
rng.shuffle(semua)
p = BST()
for k in semua:
    p.insert(k, k)
for k in semua[:1000]:
    assert p.delete(k) is True
assert p.inorder() == sorted(semua[1000:]) and p.size() == 1000

# pohon miring 10.000 data: insert dan search tidak boleh RecursionError
besar = BST()
for i in range(1, 10001):
    besar.insert(kode(i), i)
assert besar.search(kode(10000)) == 10000 and besar.size() == 10000
mulai = time.perf_counter()
for i in range(1, 10001):
    besar.search(kode(i))
print(f"search 10.000 kali di pohon miring 10.000 node: {time.perf_counter() - mulai:.2f} detik")
print("SEMUA TES HANIF LULUS")