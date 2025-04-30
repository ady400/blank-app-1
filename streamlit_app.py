import streamlit as st
import random

st.title("Simulasi Sampling dan Sub-Sampling Produk Industri")

# -----------------------------
# Bagian 1: Sampling Penerimaan Produk
# -----------------------------
st.header("1. Sampling Penerimaan Produk (Bilangan Acak)")

N = st.number_input("Ukuran lot (N)", min_value=1, value=1000)
n = st.number_input("Ukuran sampel (n)", min_value=1, max_value=N, value=50)
c = st.number_input("Acceptance number (c)", min_value=0, max_value=n, value=2)

if st.button("Ambil Sampel"):
    sampel = random.sample(range(1, N + 1), n)
    jumlah_cacat = random.randint(0, n)  # Simulasi jumlah cacat
    produk_cacat = random.sample(sampel, jumlah_cacat)

    st.write("Nomor unit sampel:", sampel)
    st.write("Nomor unit cacat:", produk_cacat)
    st.write("Jumlah cacat ditemukan:", len(produk_cacat))
    rejection_number = c + 1
    st.write("Rejection number:", rejection_number)

    if len(produk_cacat) <= c:
        st.success("Lot DITERIMA")
    else:
        st.error("Lot DITOLAK")

# -----------------------------
# Bagian 2: Sub Sampling - Cone and Quartering
# -----------------------------
st.header("2. Sub-Sampling Padatan (Cone and Quartering)")

jumlah_awal = st.number_input("Jumlah awal sampel (gram)", min_value=10, value=1000, step=10)
jumlah_akhir = st.number_input("Jumlah akhir yang diinginkan (gram)", min_value=1, value=250, step=1)

if st.button("Mulai Cone and Quartering"):
    jumlah = jumlah_awal
    langkah = 0
    riwayat = []

    while jumlah > jumlah_akhir:
        jumlah = jumlah / 2
        langkah += 1
        riwayat.append(jumlah)

    st.write(f"Diperlukan **{langkah} kali** quartering.")
    st.write("Perkiraan jumlah sampel tiap langkah:")
    for i, j in enumerate(riwayat, 1):
        st.write(f"  Langkah {i}: {j:.2f} gram")

    st.success(f"Sampel akhir sekitar {jumlah:.2f} gram")
