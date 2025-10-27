from matplotlib import pyplot as plt

# --- Fungsi Keanggotaan Linear ---
def decrease(x, min_value, max_value):
    if x <= min_value:
        return 1
    if x >= max_value:
        return 0
    result = (max_value - x) / (max_value - min_value)
    return result

def increase(x, min_value, max_value):
    if x <= min_value:
        return 0
    if x >= max_value:
        return 1
    result = (x - min_value) / (max_value - min_value)
    return result


# --- PERMINTAAN ---
class Permintaan:
    range = [1000, 3000]

    def __init__(self, x=2300):
        self.min_value = self.range[0]
        self.max_value = self.range[1]
        self.x = x

    @property
    def turun(self):
        return decrease(self.x, self.min_value, self.max_value)

    @property
    def naik(self):
        return increase(self.x, self.min_value, self.max_value)

    def get_graph(self):
        fig, ax = plt.subplots()
        x_vals = [0, self.min_value, self.max_value, 5000]
        y_turun = [1, 1, 0, 0]
        y_naik = [0, 0, 1, 1]

        ax.plot(x_vals, y_turun, label='Turun', color='C0')
        ax.plot(x_vals, y_naik, label='Naik', color='C1')

        ax.plot([self.x, self.x], [0, self.turun], 'o--', color='C0')
        ax.plot([self.x, self.x], [0, self.naik], 'o--', color='C1')

        ax.set_title('Permintaan')
        ax.legend()
        plt.savefig("images/permintaan.png")
        plt.show()


# --- PERSEDIAAN ---
class Persediaan:
    range = [200, 800]

    def __init__(self, x=400):
        self.min_value = self.range[0]
        self.max_value = self.range[1]
        self.x = x

    @property
    def sedikit(self):
        return decrease(self.x, self.min_value, self.max_value)

    @property
    def banyak(self):
        return increase(self.x, self.min_value, self.max_value)

    @property
    def sedang(self):
        # segitiga di tengah (200–400–800)
        if self.x <= self.min_value or self.x >= self.max_value:
            return 0
        elif self.x == 400:
            return 1
        elif self.x < 400:
            return (self.x - self.min_value) / (400 - self.min_value)
        else:
            return (self.max_value - self.x) / (self.max_value - 400)

    def get_graph(self):
        fig, ax = plt.subplots()
        x_vals = [0, 200, 400, 800, 1000]
        y_sedikit = [1, 1, 0, 0, 0]
        y_sedang = [0, 0, 1, 0, 0]
        y_banyak = [0, 0, 0, 1, 1]

        ax.plot(x_vals, y_sedikit, label='Sedikit', color='C0')
        ax.plot(x_vals, y_sedang, label='Sedang', color='C1')
        ax.plot(x_vals, y_banyak, label='Banyak', color='C2')

        ax.set_title('Persediaan')
        ax.legend()
        plt.savefig("images/persediaan.png")
        plt.show()


# --- PRODUKSI (Defuzzifikasi Tsukamoto) ---
class Produksi:
    range = [2000, 7000]

    def __init__(self, permintaan: Permintaan, persediaan: Persediaan):
        self.permintaan = permintaan
        self.persediaan = persediaan

    def berkurang(self, fuzzy_value):
        return self.range[1] - fuzzy_value * (self.range[1] - self.range[0])

    def bertambah(self, fuzzy_value):
        return fuzzy_value * (self.range[1] - self.range[0]) + self.range[0]

    def rule(self):
        pmt = self.permintaan
        psd = self.persediaan

        a1 = min(pmt.turun, psd.banyak)   # BERKURANG
        a2 = min(pmt.turun, psd.sedang)   # BERKURANG
        a3 = min(pmt.turun, psd.sedikit)  # BERTAMBAH
        a4 = min(pmt.naik, psd.banyak)    # BERKURANG
        a5 = min(pmt.naik, psd.sedang)    # BERTAMBAH
        a6 = min(pmt.naik, psd.sedikit)   # BERTAMBAH

        z1 = self.berkurang(a1)
        z2 = self.berkurang(a2)
        z3 = self.bertambah(a3)
        z4 = self.berkurang(a4)
        z5 = self.bertambah(a5)
        z6 = self.bertambah(a6)

        return [a1, a2, a3, a4, a5, a6], [z1, z2, z3, z4, z5, z6]

    def defuzzifikasi(self):
        a, z = self.rule()
        num = sum([a[i] * z[i] for i in range(len(a))])
        den = sum(a)
        return num / den if den != 0 else 0


# --- Jalankan ---
pmt = Permintaan(2300)
psd = Persediaan(400)
prd = Produksi(pmt, psd)

hasil = prd.defuzzifikasi()

print(f"""
Permintaan:
  TURUN = {pmt.turun:.2f}
  NAIK = {pmt.naik:.2f}

Persediaan:
  SEDIKIT = {psd.sedikit:.2f}
  SEDANG = {psd.sedang:.2f}
  BANYAK = {psd.banyak:.2f}

=> Hasil defuzzifikasi (produksi) = {hasil:.2f} kemasan/hari
""")


pmt.get_graph()
psd.get_graph()
