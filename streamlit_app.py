import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ==========================================
# CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="EcoWater COD Analyzer",
    page_icon="🌱",
    layout="centered",
)

# Database Riwayat Perhitungan (CSV)
NAMA_FILE_HISTORY = "riwayat_cod.csv"

# Inisialisasi Database jika belum ada file-nya
if not os.path.exists(NAMA_FILE_HISTORY):
    df_init = pd.DataFrame(columns=["Waktu", "Petugas", "Sampel", "Baku Mutu (mg/L)", "Hasil (mg/L)", "Status", "Interpretasi"])
    df_init.to_csv(NAMA_FILE_HISTORY, index=False)

# Custom CSS Global untuk mempercantik UI & komponen internal
st.markdown("""
    <style>
    /* Latar belakang utama putih bersih */
    .stApp {
        background-color: #ffffff !important;
    }
    /* Sidebar tetap hijau pastel agar adem */
    section[data-testid="stSidebar"] {
        background-color: #f0fdf4 !important;
    }
    section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label {
        color: #334155 !important;
    }
    div.stButton > button:first-child {
        background-color: #10b981;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #059669;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    
    /* Membuat foto otomatis di tengah dan proporsional */
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    [data-testid="stImage"] img {
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
        border-radius: 15px;
        max-width: 80% !important;
        height: auto !important;
    }
    
    /* Khusus untuk logo kecil di dalam sidebar agar tidak merusak posisi */
    section[data-testid="stSidebar"] [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
    }
    section[data-testid="stSidebar"] [data-testid="stImage"] img {
        max-width: 100px !important;
    }

    /* Membuat semua judul utama dan sub-judul di tengah secara global */
    .stApp h1, .stApp h2, .stApp h3 {
        text-align: center !important;
    }
    
    /* Gaya untuk custom card teks */
    .custom-card {
        background-color: #f8fafc;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #10b981;
        margin-bottom: 20px;
    }

    /* Memastikan tabel dataframe di tengah */
    [data-testid="stDataFrame"] {
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.image("https://i.pinimg.com/736x/a0/92/58/a09258df83907bc5d1f8f506a037cd76.jpg")
    st.title("EcoWater")
    menu = st.sidebar.radio(
        "Navigasi Halaman:",
        ["🏠 Beranda", "🧮 Kalkulator COD", "📜 Riwayat & Laporan", "ℹ️ Tentang & Referensi"],
    )
    st.markdown("---")
    st.success("Status: Sistem Aktif 🟢")

# ==========================================
# HALAMAN 1: HOME (BERANDA)
# ==========================================
if menu == "🏠 Beranda":
    st.markdown("<h1 style='text-align: center; color: #047857; font-weight: 800; margin-bottom: 20px;'>🌱 EcoWater COD Analyzer</h1>", unsafe_allow_html=True)
    
    # Foto Halaman Beranda
    st.image("https://i.pinimg.com/1200x/48/81/54/4881545ab4580b32e5bb0ce8679b8598.jpg")
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 14px; margin-top: -10px;'>Melindungi sumber daya air untuk masa depan hijau.</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="custom-card">
        <h3 style="text-align: left !important; color: #1e293b; margin-top: 0;">Selamat Datang!</h3>
        <p><b>EcoWater COD Analyzer</b> adalah aplikasi berbasis web yang dirancang untuk membantu profesional lingkungan 
        menghitung kadar <i>Chemical Oxygen Demand</i> (COD) secara instan dan akurat.</p>
        <p>Aplikasi ini mengintegrasikan data laboratorium dengan standar regulasi pemerintah untuk memberikan analisis cepat 
        mengenai status kelayakan air limbah sebelum dilepas ke lingkungan.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Membuat 3 kolom untuk box HTML Metrik yang menarik
    box_col1, box_col2, box_col3 = st.columns(3)
    
    with box_col1:
        st.markdown("""
            <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #10b981; text-align: center;">
                <span style="font-size: 14px; color: #64748b; font-weight: 600; letter-spacing: 0.5px;">AKURASI ANALISIS</span><br>
                <span style="font-size: 28px; font-weight: 800; color: #1e293b; display: block; margin-top: 5px;">99.9%</span>
            </div>
        """, unsafe_allow_html=True)
    
    with box_col2:
        st.markdown("""
            <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #3b82f6; text-align: center;">
                <span style="font-size: 14px; color: #64748b; font-weight: 600; letter-spacing: 0.5px;">KECEPATAN RESPON</span><br>
                <span style="font-size: 28px; font-weight: 800; color: #1e293b; display: block; margin-top: 5px;">Instant</span>
            </div>
        """, unsafe_allow_html=True)
    
    with box_col3:
        st.markdown("""
            <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #f59e0b; text-align: center;">
                <span style="font-size: 14px; color: #64748b; font-weight: 600; letter-spacing: 0.5px;">STANDAR ACUAN</span><br>
                <span style="font-size: 28px; font-weight: 800; color: #1e293b; display: block; margin-top: 5px;">SNI / LHK</span>
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# HALAMAN 2: KALKULATOR COD
# ==========================================
elif menu == "🧮 Kalkulator COD":
    st.markdown("<h1 style='text-align: center; color: #047857;'>Kalkulator Kadar COD</h1>", unsafe_allow_html=True)
    
    # Foto Halaman Kalkulator
    st.image("https://i.pinimg.com/736x/2d/f4/4c/2df44ccf0de9728ae2ba1f623cf3a937.jpg")
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 14px; margin-top: -10px;'>Proses Titrasi Laboratorium untuk Penentuan Kadar COD.</p>", unsafe_allow_html=True)

    # Bagian Rumus Perhitungan (Masuk Kotak Expander Rapi)
    with st.expander("📝 Lihat Rumus Perhitungan (Metode Titrimetri)"):
        st.latex(r"COD (mg/L) = \frac{(A - B) \times N \times 8000}{V_{sampel}}")
        st.markdown("""
        **Keterangan:**
        * **A:** Volume penitar (FAS) untuk blanko (mL)
        * **B:** Volume penitar (FAS) untuk sampel (mL)
        * **N:** Normalitas larutan FAS (N)
        * **8000:** Berat setara oksigen (mg/ekivalen)
        * **V:** Volume sampel air yang diuji (mL)
        """)

    st.markdown("---")
    
    # Form Input Identitas Petugas & Jenis Sampel
    st.subheader("👤 Informasi Sampel & Petugas")
    col_petugas1, col_petugas2 = st.columns(2)
    with col_petugas1:
        nama_petugas = st.text_input("Nama Petugas Pengambil Contoh:", placeholder="Masukkan nama lengkap petugas")
    with col_petugas2:
        nama_sampel = st.text_input("Kode / Lokasi Sampel Air:", placeholder="Contoh: Inlet IPAL / Sungai Cileungsi")

    # Form Input Angka Parameter Hasil Uji
    st.subheader("📥 Masukkan Parameter Hasil Uji")
    col_a, col_b = st.columns(2)
    
    with col_a:
        v_blanko = st.number_input("Volume Penitar Blanko (A) - mL", min_value=0.0, value=10.0, step=0.1)
        v_sampel = st.number_input("Volume Penitar Sampel (B) - mL", min_value=0.0, value=6.5, step=0.1)
        norm = st.number_input("Normalitas Penitar (N)", min_value=0.0000, value=0.1000, format="%.4f", step=0.001)
        v_air = st.number_input("Volume Sampel Air (mL)", min_value=1.0, value=25.0, step=1.0)
        
    with col_b:
        st.write("**Pilih Acuan Standar Baku Mutu:**")
        baku_opsi = {
            "Limbah Domestik (100 mg/L)": 100,
            "Industri Tekstil (150 mg/L)": 150,
            "Industri Cat (100 mg/L)": 100,
            "Custom Input": 0
        }
        pilihan = st.selectbox("Pilih Jenis Baku Mutu LHK:", list(baku_opsi.keys()))
        
        if pilihan == "Custom Input":
            limit = st.number_input("Batas Maksimal Kustom (mg/L)", value=50)
        else:
            limit = baku_opsi[pilihan]
            st.info(f"Batas Maksimal Regulasi: **{limit} mg/L**")

    # Tombol Hitung & Simpan Otomatis
    if st.button("🚀 HITUNG & SIMPAN HASIL"):
        if not nama_petugas.strip() or not nama_sampel.strip():
            st.error("⚠️ Gagal! Nama Petugas dan Kode/Lokasi Sampel wajib diisi untuk pencatatan laporan.")
        else:
            if v_blanko < v_sampel:
                st.warning("⚠️ Perhatian: Volume penitar blanko (A) umumnya lebih besar daripada sampel (B). Mohon cek kembali data laboratorium Anda.")
            
            # Rumus Perhitungan Utama
            hasil = ((v_blanko - v_sampel) * norm * 8000) / v_air
            waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Sistem Interpretasi Cerdas
            if hasil <= limit:
                status = "LOLOS MENCUKUPI ✅"
                warna_box = "#10b981" # hijau
                interpretasi_teks = f"Kadar COD sebesar <b>{hasil:.2f} mg/L</b> berada di bawah atau sama dengan batas standar baku mutu ({limit} mg/L). Air sampel ini dinyatakan aman dan memenuhi regulasi lingkungan untuk dialirkan."
            else:
                status = "MELEBIHI AMBANG BATAS ❌"
                warna_box = "#ef4444" # merah
                interpretasi_teks = f"Kadar COD sebesar <b>{hasil:.2f} mg/L</b> telah melewati batas maksimal regulasi lingkungan ({limit} mg/L). Air limbah dikategorikan tidak aman dan memerlukan proses purifikasi atau pengolahan ulang di unit IPAL."

            st.markdown("---")
            
            # Tampilan Output Interpretasi Box yang Menarik
            st.markdown(f"""
                <div style="background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); border-left: 6px solid {warna_box}; margin-top: 10px;">
                    <h3 style="text-align: left !important; color: {warna_box}; margin-top: 0;">📊 Hasil Analisis Kadar COD</h3>
                    <p style="color: #475569; font-size: 15px; margin-bottom: 5px;"><b>Nama Petugas:</b> {nama_petugas} &nbsp;|&nbsp; <b>Lokasi Sampel:</b> {nama_sampel}</p>
                    <p style="color: #475569; font-size: 14px; margin-top: 0;"><b>Waktu Pengujian:</b> {waktu_sekarang}</p>
                    <h1 style="text-align: left !important; font-size: 42px; margin: 15px 0; color: #1e293b;">{hasil:.2f} <span style="font-size: 20px; color: #64748b;">mg/L</span></h1>
                    <p style="font-size: 16px; color: #1e293b;"><b>Status Kelayakan:</b> <span style="color: {warna_box}; font-weight: bold;">{status}</span></p>
                    <p style="font-size: 15px; color: #334155; line-height: 1.6; margin-bottom: 0;"><b>Interpretasi Teknis:</b> {interpretasi_teks}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if hasil <= limit:
                st.balloons()
                
            # Logika menyimpan data baru ke file riwayat CSV
            row_baru = pd.DataFrame([[waktu_sekarang, nama_petugas, nama_sampel, limit, round(hasil, 2), status, interpretasi_teks.replace("<b>", "").replace("</b>", "")]],
                                    columns=["Waktu", "Petugas", "Sampel", "Baku Mutu (mg/L)", "Hasil (mg/L)", "Status", "Interpretasi"])
            row_baru.to_csv(NAMA_FILE_HISTORY, mode='a', header=False, index=False)
            st.toast("Data sukses terekam ke sistem logbook riwayat!", icon="💾")

# ==========================================
# HALAMAN 3: RIWAYAT & LAPORAN (FITUR BARU UNTUK UNDUH)
# ==========================================
elif menu == "📜 Riwayat & Laporan":
    st.markdown("<h1 style='text-align: center; color: #047857;'>Riwayat Pengujian COD</h1>", unsafe_allow_html=True)
    st.write("Berikut adalah rangkuman riwayat perhitungan logbook yang tersimpan di dalam sistem:")
    
    # Membaca data riwayat dari file CSV
    df_riwayat = pd.read_csv(NAMA_FILE_HISTORY)
    
    if df_riwayat.empty:
        st.info("Belum ada riwayat pengujian yang tersimpan dari kalkulator.")
    else:
        # Menampilkan tabel data yang rapi dan interaktif
        st.dataframe(df_riwayat, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Kolom tombol aksi unduh dan pembersihan data
        kolom_aksi1, kolom_aksi2 = st.columns([3, 1])
        
        with kolom_aksi1:
            # Mengonversi dataframe ke csv agar bisa langsung diunduh
            csv_data = df_riwayat.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 UNDUH LAPORAN RESMI (FORMAT EXCEL/CSV)",
                data=csv_data,
                file_name=f"Laporan_EcoWater_COD_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )
            
        with kolom_aksi2:
            if st.button("🗑️ Bersihkan Riwayat"):
                df_kosong = pd.DataFrame(columns=["Waktu", "Petugas", "Sampel", "Baku Mutu (mg/L)", "Hasil (mg/L)", "Status", "Interpretasi"])
                df_kosong.to_csv(NAMA_FILE_HISTORY, index=False)
                st.success("Riwayat dibersihkan!")
                st.rerun()

# ==========================================
# HALAMAN 4: TENTANG APLIKASI
# ==========================================
elif menu == "ℹ️ Tentang & Referensi":
    st.markdown("<h1 style='text-align: center; color: #047857;'>Tentang Aplikasi</h1>", unsafe_allow_html=True)
    
    # Foto Halaman Tentang
    st.image("https://i.pinimg.com/1200x/80/e5/df/80e5df94c2c611c566909ad629a86cd8.jpg")
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 14px; margin-top: -10px;'>Teknologi untuk Keberlanjutan Lingkungan.</p>", unsafe_allow_html=True)

    col_dev, col_ref = st.columns(2)
    
    with col_dev:
        st.markdown("""
        <div class="custom-card">
            <h3 style="text-align: left !important; color: #1e293b; margin-top: 0;">👤 Pembuat Aplikasi</h3>
            <p>Aplikasi ini dikembangkan oleh:</p>
            <ul>
                <li><b>Nama:</b> Kelompok</li>
                <li><b>Role:</b> Developer & Environmental Analyst</li>
                <li><b>Tujuan:</b> Alat bantu praktikum & monitoring IPAL</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_ref:
        st.markdown("""
        <div class="custom-card">
            <h3 style="text-align: left !important; color: #1e293b; margin-top: 0;">📚 Referensi Utama</h3>
            <p>Metode perhitungan dan data baku mutu didasarkan pada:</p>
            <ol>
                <li><b>SNI 6989.2:2019</b> (Cara Uji COD)</li>
                <li><b>Permen LHK No. 68/2016</b></li>
                <li><b>PP No. 22 Tahun 2021</b></li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
    st.info("Aplikasi ini sukses berjalan menggunakan Python dan Streamlit Framework.")
