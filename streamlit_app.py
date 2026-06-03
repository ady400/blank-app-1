import streamlit as st
import pandas as pd
from datetime import datetime, date
import requests
from streamlit_lottie import st_lottie

# 1. PENGATURAN HALAMAN
st.set_page_config(
    page_title="Storify Waste",
    page_icon="☣️",
    layout="wide"
)

# Custom CSS untuk mempercantik UI global
st.markdown("""
    <style>
    /* Mengubah font dan background card global */
    .stApp {
        background-color: #fdfdfd;
    }
    /* Mempercantik tampilan sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {
        color: #f8fafc !important;
    }
    /* Kustomisasi tombol utama */
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
    </style>
""", unsafe_allow_html=True)

# 2. FUNGSI MEMUAT ANIMASI LOTTIE
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        return None
    return None

# Memuat animasi Lottie
lottie_home = load_lottieurl("https://lottie.host/947d937e-1b76-43a0-b786-d255c0ee1e74/stE5uwmVhW.json") 
lottie_form = load_lottieurl("https://lottie.host/409d6f6a-ce07-4286-9a25-9b24765ff0f5/H6q8S0vXzH.json") 
lottie_about = load_lottieurl("https://lottie.host/51e3db3d-ef04-45fb-bc76-efdbb0cae5eb/tqNUnVjY02.json") 

# 3. DATABASE DAN REKOMENDASI WADAH OTOMATIS
B3_DATABASE = {
    "Sludge IPAL / Elektroplating": {
        "simbol": "☣️ Beracun (Toxic)", 
        "masa_simpan": 90,
        "wadah_rekomendasi": "Drum Plastik (HDPE Drum) atau Jumbo Bag dengan pelapis dalam (inner liner) untuk mencegah kebocoran material basah."
    },
    "Oli Bekas / Solvent": {
        "simbol": "🔥 Mudah Menyala (Flammable)", 
        "masa_simpan": 180,
        "wadah_rekomendasi": "Drum Baja (Steel Drum) yang dilengkapi dengan seal penutup rapat untuk menahan tekanan uap cair."
    },
    "Aki Bekas / Asam-Asaman": {
        "simbol": "🧪 Korosif (Corrosive)", 
        "masa_simpan": 365,
        "wadah_rekomendasi": "Box Container Plastic / Palet Plastik HDPE khusus yang tahan terhadap korosi asam dan zat kimia tajam."
    },
    "Kain Majun Terkontaminasi": {
        "simbol": "⚠️ Bahaya Terhadap Kesehatan", 
        "masa_simpan": 180,
        "wadah_rekomendasi": "Drum Baja (Steel Drum) atau Container Tertutup untuk meminimalisir risiko penyebaran kontaminan ke udara."
    },
    "Fly Ash / Bottom Ash": {
        "simbol": "☣️ Beracun (Toxic)", 
        "masa_simpan": 365,
        "wadah_rekomendasi": "Jumbo Bag tipe tertutup rapat (Woven PP dengan liner) untuk menghindari emisi debu halus ke lingkungan sekitar."
    }
}

# 4. INITIALIZATION SESSION STATE
if "b3_db" not in st.session_state:
    st.session_state.b3_db = pd.DataFrame(columns=[
        "ID Limbah", "Jenis Limbah", "Karakteristik / Simbol", 
        "Rekomendasi Wadah", "Berat (Kg)", "Tanggal Masuk", "Batas Hari", "Sisa Hari", "Status"
    ])

# ==================== SIDEBAR (NAVIGASI SAMPING) ====================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>☣️ Storify Waste</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 14px;'>Sistem Kepatuhan TPS Digital</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    menu_pilihan = st.radio(
        "Pilih Menu Navigasi:",
        ["🏠 Beranda Utama", "📥 Input & Hasil Data", "ℹ️ Tentang & Regulasi"]
    )
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("⚡ Dibangun untuk Kepatuhan Lingkungan & K3")
    st.caption("Aplikasi Pemantauan Digital v1.2")

# ==================== LOGIKA HALAMAN UTAMA ====================

# 📑 MENU 1: BERANDA UTAMA
if menu_pilihan == "🏠 Beranda Utama":
    
    # Grid layout untuk Header & Animasi agar seimbang
    col_header1, col_header2 = st.columns([2, 1])
    
    with col_header1:
        st.markdown("""
            <div style="padding: 20px 0;">
                <h1 style="color: #0f172a; font-size: 38px; font-weight: 800; margin-bottom: 10px;">
                    Sistem Pemantauan & Kepatuhan <span style="color: #10b981;">Limbah B3</span>
                </h1>
                <p style="color: #475569; font-size: 18px; line-height: 1.6;">
                    Solusi cerdas integratif untuk pencatatan logbook, standarisasi pengemasan, 
                    dan pelacakan masa simpan real-time di Tempat Penyimpanan Sementara (TPS).
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_header2:
        if lottie_home:
            st_lottie(lottie_home, speed=1, quality="high", height=220, key="home_lottie")
            
    st.markdown("---")
