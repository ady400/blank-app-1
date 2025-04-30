import random

N = 1000  # ukuran lot
n = 50    # ukuran sampel
c = 2     # acceptance number

# Simulasi ambil 50 sampel acak dari 1000
sampel = random.sample(range(1, N + 1), n)

# Misal kita punya data cacat secara acak
produk_cacat = random.sample(sampel, 3)  # misalnya 3 dari 50 cacat

print("Jumlah cacat:", len(produk_cacat))
if len(produk_cacat) <= c:
    print("Lot DITERIMA")
else:
    print("Lot DITOLAK")
