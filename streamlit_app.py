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
    .stApp {
        background-color: #fdfdfd;
    }
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
    }
    section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label {
        color: #f8fafc !important;
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
# Animasi tambahan untuk menu K3/Kedaruratan
lottie_safety = load_lottieurl("https://lottie.host/bc796e94-3cb1-447a-b5e1-db3496c81bf4/cM6wWbyf3T.json")

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
    
    # Menambahkan opsi menu ke-3: Cara Penanganan & SOP
    menu_pilihan = st.radio(
        "Pilih Menu Navigasi:",
        ["🏠 Beranda Utama", "📥 Input & Hasil Data", "📋 Prosedur Kedaruratan & SOP", "ℹ️ Tentang & Regulasi"]
    )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("⚡ Dibangun untuk Kepatuhan Lingkungan & K3")
    st.caption("Aplikasi Pemantauan Digital v1.3")

# ==================== LOGIKA HALAMAN UTAMA ====================

# 📑 MENU 1: BERANDA UTAMA
if menu_pilihan == "🏠 Beranda Utama":
    col_header1, col_header2 = st.columns([2, 1])
    with col_header1:
        st.markdown("""
            <div style="padding: 20px 0;">
                <h1 style="color: #0f172a; font-size: 38px; font-weight: 800; margin-bottom: 10px;">
                    Sistem Pemantauan & Kepatuhan <span style="color: #10b981;">Limbah B3</span>
                </h1>
                <p style="color: #475569; font-size: 18px; line-height: 1.6;">
                    Solusi cerdas integratif untuk pencatatan logbook, standarisasi pengemasan, 
                    pelacakan masa simpan real-time, serta penanggulangan tanggap darurat di TPS.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col_header2:
        if lottie_home:
            st_lottie(lottie_home, speed=1, quality="high", height=220, key="home_lottie")
            
    st.markdown("---")
    st.markdown("<h3 style='text-align: center; color: #1e293b; margin-bottom: 25px;'>Mengapa Storify Waste Diperlukan?</h3>", unsafe_allow_html=True)
    
    pilar1, pilar2, pilar3 = st.columns(3)
    with pilar1:
        st.markdown("""
            <div style="background-color: #ffffff; padding: 25px; border-radius: 12px; border-top: 5px solid #ef4444; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); height: 250px;">
                <h4 style="color: #0f172a; margin-top: 0;">🛡️ Kepatuhan Hukum & K3</h4>
                <p style="color: #475569; font-size: 14px; line-height: 1.5;">
                    Sistem otomatis memberikan peringatan dini (early warning) sebelum batas waktu legal penyimpanan limbah berakhir sesuai regulasi pemerintah.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with pilar2:
        st.markdown("""
            <div style="background-color: #ffffff; padding: 25px; border-radius: 12px; border-top: 5px solid #f59e0b; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); height: 250px;">
                <h4 style="color: #0f172a; margin-top: 0;">📦 Standardisasi Kemasan</h4>
                <p style="color: #475569; font-size: 14px; line-height: 1.5;">
                    Mencegah kecelakaan kerja dengan rekomendasi otomatis jenis kontainer atau wadah yang kompatibel dengan sifat kimia limbah berbahaya.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with pilar3:
        st.markdown("""
            <div style="background-color: #ffffff; padding: 25px; border-radius: 12px; border-top: 5px solid #10b981; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); height: 250px;">
                <h4 style="color: #0f172a; margin-top: 0;">📊 Transparansi Audit</h4>
                <p style="color: #475569; font-size: 14px; line-height: 1.5;">
                    Menghasilkan format logbook digital yang terstruktur, rapi, dan siap diekspor kapan saja untuk mempermudah audit lingkungan internal maupun KLHK.
                </p>
            </div>
        """, unsafe_allow_html=True)

# 📥 MENU 2: INPUT & HASIL DATA
elif menu_pilihan == "📥 Input & Hasil Data":
    col_title, col_anim = st.columns([3, 1])
    with col_title:
        st.markdown("""
            <div style="padding-top: 15px;">
                <h1 style="color: #0f172a; margin-bottom: 0;">📥 Manajemen Logbook & Inventaris TPS</h1>
                <p style="color: #64748b;">Silakan masukkan data manifes limbah masuk di panel kiri untuk memperbarui tabel pantauan.</p>
            </div>
        """, unsafe_allow_html=True)
    with col_anim:
        if lottie_form:
            st_lottie(lottie_form, speed=1, quality="high", height=100, key="form_menu_top")
            
    st.markdown("---")
    col_f1, col_f2 = st.columns([1, 2.2])
    
    with col_f1:
        st.markdown("""
            <div style="background-color: #f8fafc; padding: 15px; border-radius: 8px; border-left: 4px solid #3b82f6; margin-bottom: 15px;">
                <b style="color: #1e3a8a;">📝 Formulir Entri Limbah</b>
            </div>
        """, unsafe_allow_html=True)
            
        with st.form(key="form_b3", clear_on_submit=True):
            jenis_limbah = st.selectbox("Pilih Jenis Limbah B3", list(B3_DATABASE.keys()))
            simbol_oto = B3_DATABASE[jenis_limbah]["simbol"]
            wadah_oto = B3_DATABASE[jenis_limbah]["wadah_rekomendasi"]
            
            st.markdown(f"""
                <div style="background-color: #ffffff; border: 1px solid #e2e8f0; padding: 12px; border-radius: 8px; margin-bottom: 15px;">
                    <span style="font-size: 13px; color: #64748b;">Karakteristik Bahaya:</span><br>
                    <b style="color: #ef4444;">{simbol_oto}</b><br><br>
                    <span style="font-size: 13px; color: #64748b;">Rekomendasi Wadah Teknis:</span><br>
                    <span style="font-size: 14px; color: #334155; font-weight: 500;">{wadah_oto}</span>
                </div>
            """, unsafe_allow_html=True)
            
            berat = st.number_input("Berat Limbah Masuk (Kg)", min_value=1.0, step=10.0)
            tgl_masuk = st.date_input("Tanggal Masuk TPS", date.today())
            submit_btn = st.form_submit_button(label="Simpan Data Masuk 💾", use_container_width=True)
            
        if submit_btn:
            id_limbah = f"B3-{datetime.now().strftime('%M%S')}"
            batas_hari = B3_
