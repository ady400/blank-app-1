import streamlit as st
import random

st.title("Sampling Penerimaan Produk - Metode Bilangan Acak")

N = st.number_input("Ukuran lot (N)", min_value=1, value=1000)
n = st.number_input("Ukuran sampel (n)", min_value=1, max_value=N, value=50)
c = st.number_input("Acceptance number (c)", min_value=0, max_value=n, value=2)

if st.button("Ambil Sampel"):
    sampel = random.sample(range(1, N + 1), n)
    produk_cacat = random.sample(sampel, random.randint(0, n))  # jumlah cacat acak

    st.write("Jumlah cacat ditemukan:", len(produk_cacat))
    st.write("Nomor unit cacat:", produk_cacat)

    if len(produk_cacat) <= c:
        st.success("Lot DITERIMA")
    else:
        st.error("Lot DITOLAK")
