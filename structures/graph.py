"""Graph buatan sendiri dengan representasi adjacency list (node bertaut).

Dipakai pada fitur: keterhubungan lokasi rak perpustakaan dan rute antar rak.
Mendukung 4 variasi: berarah / tidak berarah, berbobot / tidak berbobot.
BFS memakai Queue buatan sendiri (structures/antrean.py).
Tidak memakai dict, deque, atau library graph bawaan.
"""

from .antrean import Queue


class Sisi:
    """Satu sisi (edge) dalam daftar tetangga: menunjuk simpul tujuan dan bobotnya."""

    def __init__(self, tujuan, bobot):
        self.tujuan = tujuan          # indeks simpul tujuan
        self.bobot = bobot
        self.berikutnya = None


class Simpul:
    """Satu simpul (vertex): menyimpan id dan kepala daftar tetangganya."""

    def __init__(self, id_simpul):
        self.id = id_simpul
        self.kepala = None            # sisi pertama
        self.ekor = None              # sisi terakhir (agar penambahan O(1))


class Graph:
    """ADT Graph dengan adjacency list.

    Args:
        berarah: True jika sisi punya arah (A -> B tidak otomatis B -> A).
        berbobot: True jika sisi punya bobot (misalnya jarak). Jika False, bobot = 1.
    """

    def __init__(self, berarah=False, berbobot=True):
        self.berarah = berarah
        self.berbobot = berbobot
        self._simpul = []             # array simpul; indeks array = nomor simpul
        self._jumlah_sisi = 0

    # ---------- membangun graph ----------
    def cari_indeks(self, id_simpul):
        """Mencari indeks simpul berdasarkan id. Mengembalikan -1 jika tidak ada. O(V)."""
        for i in range(len(self._simpul)):
            if self._simpul[i].id == id_simpul:
                return i
        return -1

    def tambah_simpul(self, id_simpul):
        """Menambah simpul baru. O(V) karena mengecek duplikat."""
        if not isinstance(id_simpul, str) or id_simpul.strip() == "":
            raise ValueError("ID simpul harus berupa string yang tidak kosong.")
        if self.cari_indeks(id_simpul) != -1:
            raise ValueError(f"Simpul {id_simpul} sudah ada.")
        self._simpul.append(Simpul(id_simpul))

    def _sambung(self, dari, ke, bobot):
        """Menambahkan satu sisi searah dari indeks 'dari' ke indeks 'ke'. O(1)."""
        sisi = Sisi(ke, bobot)
        asal = self._simpul[dari]
        if asal.kepala is None:
            asal.kepala = sisi
        else:
            asal.ekor.berikutnya = sisi
        asal.ekor = sisi

    def _ada_sisi(self, dari, ke):
        saat_ini = self._simpul[dari].kepala
        while saat_ini is not None:
            if saat_ini.tujuan == ke:
                return True
            saat_ini = saat_ini.berikutnya
        return False

    def tambah_sisi(self, asal, tujuan, bobot=1):
        """Menambah sisi antar dua simpul.

        Graph tidak berarah: sisi dicatat di kedua simpul. Berarah: hanya di simpul asal.
        """
        a = self.cari_indeks(asal)
        b = self.cari_indeks(tujuan)
        if a == -1 or b == -1:
            raise ValueError("Kedua simpul harus sudah ada sebelum dihubungkan.")
        if a == b:
            raise ValueError("Simpul tidak boleh terhubung ke dirinya sendiri.")
        if self._ada_sisi(a, b):
            raise ValueError(f"Sisi {asal} -> {tujuan} sudah ada.")
        if not self.berbobot:
            bobot = 1
        elif not isinstance(bobot, (int, float)) or bobot <= 0:
            raise ValueError("Bobot harus berupa bilangan positif.")
        self._sambung(a, b, bobot)
        if not self.berarah:
            self._sambung(b, a, bobot)
        self._jumlah_sisi += 1

    # ---------- informasi ----------
    def jumlah_simpul(self):
        return len(self._simpul)

    def jumlah_sisi(self):
        return self._jumlah_sisi

    def jenis(self):
        arah = "berarah" if self.berarah else "tidak berarah"
        bobot = "berbobot" if self.berbobot else "tidak berbobot"
        return f"{arah}, {bobot}"

    def tetangga(self, id_simpul):
        """Daftar id tetangga sebuah simpul, sesuai urutan penambahan sisi."""
        i = self.cari_indeks(id_simpul)
        if i == -1:
            raise ValueError(f"Simpul {id_simpul} tidak ditemukan.")
        hasil = []
        saat_ini = self._simpul[i].kepala
        while saat_ini is not None:
            hasil.append(self._simpul[saat_ini.tujuan].id)
            saat_ini = saat_ini.berikutnya
        return hasil

    def display(self):
        """Mencetak adjacency list. O(V + E)."""
        print(f"Graph {self.jenis()}: {self.jumlah_simpul()} simpul, {self.jumlah_sisi()} sisi")
        for simpul in self._simpul:
            teks = f"  {simpul.id}:"
            saat_ini = simpul.kepala
            if saat_ini is None:
                teks += " (tidak punya tetangga)"
            while saat_ini is not None:
                nama = self._simpul[saat_ini.tujuan].id
                teks += f" -> {nama}({saat_ini.bobot})" if self.berbobot else f" -> {nama}"
                saat_ini = saat_ini.berikutnya
            print(teks)

    # ---------- penelusuran ----------
    def _bfs(self, awal):
        """BFS dari indeks 'awal'. Mengembalikan (urutan indeks, array induk)."""
        n = len(self._simpul)
        dikunjungi = [False] * n
        induk = [-1] * n
        urutan = []
        antrean = Queue()
        dikunjungi[awal] = True
        antrean.enqueue(awal)
        while not antrean.is_empty():
            u = antrean.dequeue()
            urutan.append(u)
            sisi = self._simpul[u].kepala
            while sisi is not None:
                v = sisi.tujuan
                if not dikunjungi[v]:
                    dikunjungi[v] = True
                    induk[v] = u
                    antrean.enqueue(v)
                sisi = sisi.berikutnya
        return urutan, induk

    def bfs(self, awal):
        """BFS: menelusuri level demi level dari simpul awal. O(V + E)."""
        i = self.cari_indeks(awal)
        if i == -1:
            raise ValueError(f"Simpul awal {awal} tidak ditemukan.")
        urutan, _ = self._bfs(i)
        return [self._simpul[x].id for x in urutan]

    def dfs(self, awal):
        """DFS: menelusuri sedalam mungkin lebih dulu, lalu mundur (rekursif). O(V + E)."""
        i = self.cari_indeks(awal)
        if i == -1:
            raise ValueError(f"Simpul awal {awal} tidak ditemukan.")
        dikunjungi = [False] * len(self._simpul)
        urutan = []
        self._dfs_rekursif(i, dikunjungi, urutan)
        return urutan

    def _dfs_rekursif(self, u, dikunjungi, urutan):
        dikunjungi[u] = True
        urutan.append(self._simpul[u].id)
        sisi = self._simpul[u].kepala
        while sisi is not None:
            if not dikunjungi[sisi.tujuan]:
                self._dfs_rekursif(sisi.tujuan, dikunjungi, urutan)
            sisi = sisi.berikutnya

    def rute_tersingkat_langkah(self, asal, tujuan):
        """Rute dengan JUMLAH LANGKAH paling sedikit (lewat BFS), bukan jarak terpendek.

        Mengembalikan (daftar id rak, total bobot sepanjang rute) atau (None, 0)
        jika tidak ada rute.
        """
        a = self.cari_indeks(asal)
        b = self.cari_indeks(tujuan)
        if a == -1 or b == -1:
            raise ValueError("Simpul asal dan tujuan harus ada.")
        _, induk = self._bfs(a)
        if a != b and induk[b] == -1:
            return None, 0
        indeks_rute = []
        x = b
        while x != -1:
            indeks_rute.append(x)
            x = induk[x]
        indeks_rute.reverse()
        total = 0
        for k in range(len(indeks_rute) - 1):
            sisi = self._simpul[indeks_rute[k]].kepala
            while sisi.tujuan != indeks_rute[k + 1]:
                sisi = sisi.berikutnya
            total += sisi.bobot
        return [self._simpul[x].id for x in indeks_rute], total


def buat_graph_rak():
    """Graph utama: 10 rak, tidak berarah, berbobot (jarak jalan kaki dalam meter)."""
    g = Graph(berarah=False, berbobot=True)
    for nomor in range(1, 11):
        g.tambah_simpul(f"R{nomor:02d}")
    sisi = [("R01", "R02", 4), ("R02", "R03", 6), ("R03", "R04", 4), ("R04", "R05", 7),
            ("R05", "R06", 4), ("R06", "R07", 6), ("R07", "R08", 4), ("R08", "R09", 7),
            ("R09", "R10", 4), ("R01", "R05", 9), ("R02", "R06", 9), ("R03", "R07", 8),
            ("R04", "R08", 8)]
    for asal, tujuan, bobot in sisi:
        g.tambah_sisi(asal, tujuan, bobot)
    return g


if __name__ == "__main__":
    print("=== Demo Graph rak perpustakaan ===")
    g = buat_graph_rak()

    print("\n1) Graph utama (adjacency list):")
    g.display()

    print("\n2) Penelusuran dari simpul awal R01:")
    print(f"  BFS: {' -> '.join(g.bfs('R01'))}")
    print(f"  DFS: {' -> '.join(g.dfs('R01'))}")

    print("\n3) Rute dengan langkah paling sedikit R01 ke R10:")
    rute, total = g.rute_tersingkat_langkah("R01", "R10")
    print(f"  {' -> '.join(rute)}  (total jarak {total} m)")

    print("\n4) Empat variasi graph (contoh kecil: Pintu, R01, R02, Layanan):")
    contoh = [
        (False, False, "tidak berarah, tidak berbobot"),
        (False, True, "tidak berarah, berbobot (jenis graph utama)"),
        (True, False, "berarah, tidak berbobot"),
        (True, True, "berarah, berbobot (misal jalur satu arah ke meja layanan)"),
    ]
    for berarah, berbobot, judul in contoh:
        print(f"\n  [{judul}]")
        kecil = Graph(berarah=berarah, berbobot=berbobot)
        for nama in ["Pintu", "R01", "R02", "Layanan"]:
            kecil.tambah_simpul(nama)
        kecil.tambah_sisi("Pintu", "R01", 5)
        kecil.tambah_sisi("R01", "R02", 3)
        kecil.tambah_sisi("R02", "Layanan", 4)
        kecil.display()
        print(f"  BFS dari Pintu: {' -> '.join(kecil.bfs('Pintu'))}")
        print(f"  BFS dari Layanan: {' -> '.join(kecil.bfs('Layanan'))}")

    print("\n5) Validasi input:")
    for aksi, fungsi in [
        ("simpul duplikat", lambda: g.tambah_simpul("R01")),
        ("sisi ke simpul tidak ada", lambda: g.tambah_sisi("R01", "R99", 3)),
        ("bobot negatif", lambda: g.tambah_sisi("R01", "R03", -2)),
        ("BFS dari simpul tidak ada", lambda: g.bfs("R99")),
    ]:
        try:
            fungsi()
        except ValueError as e:
            print(f"  {aksi}: error ditangani -> {e}")
