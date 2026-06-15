import streamlit as st
import pandas as pd
from datetime import datetime, date
import requests
import os
from streamlit_lottie import st_lottie

# 1. PENGATURAN HALAMAN & CUSTOM CSS GLOBAL (HIJAU TUA DEEP FOREST)
st.set_page_config(
    page_title="Storify Waste",
    page_icon="☣️",
    layout="wide"
)

# Custom CSS Global dengan Sidebar Hijau Tua Pekat/Gelap
st.markdown("""
    <style>
    .stApp {
        background-color: #fdfdfd;
    }
    
    /* SIDEBAR HIJAU TUA AGAL GELAP (DEEP FOREST GREEN) */
    section[data-testid="stSidebar"] {
        background-color: #0f4c3a !important; /* Warna hijau botol tua pekat */
    }
    
    /* Memastikan teks di sidebar berwarna putih bersih agar kontras dengan background gelap */
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    
    /* WARNA IKON TANDA TANYA (HELP) BIAR PUTIH TERANG NYALA */
    section[data-testid="stSidebar"] button[data-testid="stTooltipHoverTarget"] svg {
        fill: #ffffff !important;
        color: #ffffff !important;
        filter: drop-shadow(0 0 4px rgba(255, 255, 255, 0.6));
    }
    
    /* Desain Tombol Utama (Button) */
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
    
    /* AGAR FOTO TIDAK ZOOM */
    .stApp img {
        max-width: 65% !important;
        height: auto !important;    
        display: block;
        margin-left: auto;
        margin-right: auto;
        border-radius: 15px;       
    }
    /* Khusus untuk logo kecil di dalam sidebar agar tidak melar */
    section[data-testid="stSidebar"] img, div[style*="align-items: center"] img, div[style*="box-shadow"] img {
        max-width: 100% !important;
        height: auto !important;
        display: inline-block;
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

lottie_home = load_lottieurl("https://lottie.host/947d937e-1b76-43a0-b786-d255c0ee1e74/stE5uwmVhW.json") 
lottie_form = load_lottieurl("https://lottie.host/409d6f6a-ce07-4286-9a25-9b24765ff0f5/H6q8S0vXzH.json") 
lottie_about = load_lottieurl("https://lottie.host/51e3db3d-ef04-45fb-bc76-efdbb0cae5eb/tqNUnVjY02.json") 
lottie_safety = load_lottieurl("https://lottie.host/bc796e94-3cb1-447a-b5e1-db3496c81bf4/cM6wWbyf3T.json")

# 3. DATABASE DENGAN LOGO B3 RESMI & DATA PENANGANAN LENGKAP
B3_DATABASE = {
    "Sludge IPAL / Elektroplating": {
        "karakteristik": "Beracun (Toxic)",
        "logo_url": "https://images.tokopedia.net/img/cache/500-square/VqbcmM/2022/9/29/7ff5bec4-cf0a-426d-9059-a8d6ce31f491.png",
        "masa_simpan": 90,
        "wadah_rekomendasi": "Drum Plastik (HDPE Drum) atau Jumbo Bag dengan pelapis dalam (inner liner) untuk mencegah kebocoran material basah.",
        "sop_kebocoran": [
            "<b>Isolasi Area:</b> Pasang barikade pembatas (safety cone) di sekitar area ceceran lumpur IPAL.",
            "<b>Lokalisasi Limbah:</b> Gunakan sekop non-pemicu percikan untuk mengumpulkan material lumpur yang tumpah.",
            "<b>Pembersihan Teknis:</b> Masukkan kembali lumpur ke dalam drum plastik cadangan penampung darurat.",
            "<b>Dekontaminasi Lantai:</b> Bersihkan sisa lantai menggunakan absorban lembab atau serbuk gergaji. Bilas bekasnya ke saluran IPAL internal."
        ],
        "first_aid": [
            "<b>Kontak Kulit:</b> Segera basuh kulit menggunakan sabun antiseptik dan air mengalir deras.",
            "<b>Kontak Mata:</b> Alirkan air bersih dari eye wash station minimal 15 menit and segera hubungi tim medis."
        ],
        "apd": ["Masker Katrid Gas / N95", "Kacamata Goggle pelindung", "Sarung Tangan Nitrile / Rubber tebal", "Sepatu Safety Boots karet"]
    },
    "Oli Bekas / Solvent": {
        "karakteristik": "Mudah Menyala (Flammable)",
        "logo_url": "https://i1.wp.com/hsepedia.com/wp-content/uploads/2018/03/sign-2.png?ssl=1",
        "masa_simpan": 180,
        "wadah_rekomendasi": "Drum Baja (Steel Drum) yang dilengkapi dengan seal penutup rapat untuk menahan tekanan uap cair.",
        "sop_kebocoran": [
            "<b>Eliminasi Api:</b> Matikan semua mesin elektrikal dan larang keras merokok di radius tumpahan.",
            "<b>Pengurungan (Containment):</b> Pasang <i>Oil Spill Boom</i> atau taburkan pasir kering di sekeliling genangan oli agar tidak meluas.",
            "<b>Penyedotan:</b> Sedot cairan minyak menggunakan pompa tangan manual penampung darurat.",
            "<b>Pembersihan Akhir:</b> Lap sisa lapisan minyak tipis dengan kain majun absorber khusus cairan hidrokarbon."
        ],
        "first_aid": [
            "<b>Kontak Kulit:</b> Cuci bersih dengan sabun pelarut minyak dan air mengalir. Ganti baju petugas jika terkena cipratan.",
            "<b>Risiko Kebakaran:</b> Siapkan APAR jenis Busa (Foam) atau CO2 di titik tumpahan. Jangan siram pakai air biasa karena oli akan meluas."
        ],
        "apd": ["Kacamata Safety Goggles", "Sarung Tangan Neoprene tahan minyak", "Apron PVC Pelindung Dada", "Sepatu Safety sol anti-slip"]
    },
    "Aki Bekas / Asam-Asaman": {
        "karakteristik": "Korosif (Corrosive)",
        "logo_url": "https://images.tokopedia.net/img/cache/700/VqbcmM/2022/9/29/d0df9bbf-a230-4ee6-9625-360467df8362.png",
        "masa_simpan": 365,
        "wadah_rekomendasi": "Box Container Plastic / Palet Plastik HDPE khusus yang tahan terhadap korosi asam dan zat kimia tajam.",
        "sop_kebocoran": [
            "<b>Proses Netralisasi:</b> Taburkan bubuk soda kue (Sodium Bikarbonat) secara perlahan di atas tumpahan air asam aki untuk menaikkan pH menjadi netral (pH 6-8).",
            "<b>Penyerapan:</b> Serap hasil netralisasi menggunakan pad kain dari <i>Chemical Spill Kit</i> atau pasir.",
            "<b>Pengepakan Evakuasi:</b> Pindahkan sel aki rusak ke dalam wadah box kontainer HDPE tertutup rapat."
        ],
        "first_aid": [
            "<b>Luka Bakar Asam:</b> Bilas secepat mungkin bagian tubuh/kulit yang terkena cairan asam dengan air mengalir kontinu selama 20 menit tanpa henti.",
            "<b>Gas Berbahaya:</b> Nyalakan blower ventilasi ruangan karena retakan aki berisiko memicu akumulasi gas hidrogen."
        ],
        "apd": ["Pelindung Wajah Penuh (Face Shield)", "Sarung Tangan Karet Panjang Tahan Asam", "Apron Karet Tebal", "Safety Boots khusus zat asam"]
    },
    "Kain Majun Terkontaminasi": {
        "karakteristik": "Bahaya Terhadap Kesehatan",
        "logo_url": "https://images.tokopedia.net/img/cache/500-square/VqbcmM/2022/9/29/d3a77198-9c4d-488a-83a1-80fb1cd17f32.png",
        "masa_simpan": 180,
        "wadah_rekomendasi": "Drum Baja (Steel Drum) atau Container Tertutup untuk meminimalisir risiko penyebaran kontaminan ke udara.",
        "sop_kebocoran": [
            "<b>Pencegahan Tercecer:</b> Pastikan kain majun kotor tidak diletakkan di lantai terbuka luar bangunan.",
            "<b>Wadah Tertutup:</b> Gunakan capit panjang untuk mengumpulkan kain majun berserakan lalu masukkan ke drum klem baja.",
            "<b>Kontrol Suhu:</b> Jaga drum majun dari paparan panas matahari berlebih guna menghindari penguapan gas sisa solvent."
        ],
        "first_aid": [
            "<b>Paparan Bau Terhirup:</b> Jika petugas pusing akibat menghirup uap kain majun solvent, bawa segera ke ruangan terbuka ber-AC atau berudara bersih."
        ],
        "apd": ["Sarung Tangan Kain berlapis Nitrile", "Masker Karbon Aktif (penyaring bau gas)", "Kacamata Safety Standar"]
    },
    "Fly Ash / Bottom Ash": {
        "karakteristik": "Beracun (Toxic)",
        "logo_url": "https://images.tokopedia.net/img/cache/500-square/VqbcmM/2022/9/29/7ff5bec4-cf0a-426d-9059-a8d6ce31f491.png",
        "masa_simpan": 365,
        "wadah_rekomendasi": "Jumbo Bag tipe tertutup rapat (Woven PP dengan liner) untuk menghindari emisi debu halus ke lingkungan sekitar.",
        "sop_kebocoran": [
            "<b>Metode Pembasahan:</b> Semprotkan spray air halus (*water mist*) ke area ceceran abu halus agar debu tidak terbang terbawa angin.",
            "<b>Pembersihan Serbuk:</b> Sekop abu secara perlahan ke dalam Jumbo Bag baru atau wadah tertutup rapat.",
            "<b>Pencegahan Saluran:</b> Tutup lubang selokan sekitar agar serbuk abu tidak hanyut masuk ke ekosistem air warga."
        ],
        "first_aid": [
            "<b>Mata Kemasukan Abu:</b> Basuh mata dengan cairan steril pembersih mata secara berulang. Jangan digosok karena partikel silika abu bisa menggores kornea."
        ],
        "apd": ["Masker Respirator Partikulat N95/N100", "Kacamata Goggle anti-debu", "Sarung Tangan Heavy Duty", "Safety Boots & Wearpack Full"]
    }
}

# 4. INITIALIZATION DATABASE PERMANEN & SIDEBAR MULTI-USER (UI PREMIUM REVISED)
with st.sidebar:
    # Logo bagian atas Sidebar
    st.markdown("""
        <div style="text-align: center; margin-top: -10px; margin-bottom: 15px;">
            <img src="https://i.pinimg.com/1200x/bc/06/49/bc064971cc50c810bab582f3c2a3b3da.jpg" 
                 style="width: 100px; height: 100px; object-fit: cover; border-radius: 50%; border: 3px solid #10b981; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" 
                 alt="Logo Sidebar">
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>Storify Waste</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1; font-size: 14px;'>Sistem Kepatuhan TPS Digital</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- FITUR UTAMA: RUANG PENYIMPANAN TERPISAH (VERSI FIX VISUAL) ---
    st.markdown("<h3 style='color: #f59e0b; font-size: 19px; font-weight: 700; margin-bottom: 5px; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);'>🔑 Akses Ruang TPS</h3>", unsafe_allow_html=True)
    
    id_tps_user = st.text_input(
        "Masukkan ID / Nama Perusahaan:", 
        value="", 
        placeholder="Contoh: PT Surya Abadi",
        help="Ketik nama pabrik/perusahaan Anda. Sistem akan otomatis membuatkan atau memuat folder database khusus untuk Anda agar tidak bercampur dengan pengguna lain."
    ).strip()
    
    if not id_tps_user:
        nama_file_aktif = "ruang_publik"
        nama_tampilan = "Ruang Publik (Belum Masuk)"
    else:
        nama_file_aktif = id_tps_user.replace(" ", "_")
        nama_tampilan = id_tps_user.replace("_", " ")
    
    NAMA_FILE_DB = f"database_tps_{nama_file_aktif}.csv"
    KOLOM_DATABASE = ["ID Limbah", "Jenis Limbah", "Karakteristik / Simbol", "Rekomendasi Wadah", "Berat (Kg)", "Tanggal Masuk", "Batas Hari", "Sisa Hari", "Status"]

    if "current_tps_id" not in st.session_state or st.session_state.current_tps_id != nama_file_aktif:
        st.session_state.current_tps_id = nama_file_aktif
        if os.path.exists(NAMA_FILE_DB):
            try:
                st.session_state.b3_db = pd.read_csv(NAMA_FILE_DB)
                if not st.session_state.b3_db.empty:
                    st.session_state.b3_db["Tanggal Masuk"] = pd.to_datetime(st.session_state.b3_db["Tanggal Masuk"]).dt.date
            except:
                st.session_state.b3_db = pd.DataFrame(columns=KOLOM_DATABASE)
        else:
            st.session_state.b3_db = pd.DataFrame(columns=KOLOM_DATABASE)
            st.session_state.b3_db.to_csv(NAMA_FILE_DB, index=False)
            
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #059669 0%, #10b981 100%); 
                    padding: 14px; 
                    border-radius: 12px; 
                    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25); 
                    text-align: center; 
                    margin-top: 12px; 
                    border: 1px solid #34d399;">
            <span style="font-size: 12px; color: #d1fae5; font-weight: 500; display: block; margin-bottom: 3px; letter-spacing: 0.5px;">📍 RUANG DATA AKTIF</span>
            <b style="color: #ffffff; font-size: 15px; font-weight: 700; display: block; word-wrap: break-word;">{nama_tampilan}</b>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

# --- KODE BARU (SUDAH DIRAPIKAN INDENTASINYA) ---

st.markdown("---")

# # Pastikan tidak ada spasi sisa di awal baris jika ini di tingkat utama (global scope)
menu_pilihan = st.radio(
    "Pilih Menu Navigasi:",
    ["🏠 Beranda Utama", "📊 Input & Hasil Data", "📋 Prosedur Kedaruratan & SOP", "ℹ️ Tentang & Regulasi"]
)

st.markdown("---")

# --- KOTAK NAMA ANGGOTA KELOMPOK BARU ---
st.markdown("""
<div style="background-color: rgba(255, 255, 255, 0.08); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2);">
    <b style="color: #f59e0b; font-size: 14px; display: block; margin-bottom: 6px; letter-spacing: 0.5px;">👥 KELOMPOK 4:</b>
    <ul style="color: #ffffff; font-size: 13px; padding-left: 16px; margin: 0; line-height: 1.4;">
        <li>Ajeng Ayu Dyah Putri</li>
        <li>Fathiyya Rizkyana</li>
        <li>Nadine Nareshwari Radisti</li>
        <li>Namina Ratu Chessa Juniar</li>
        <li>Naura Khairunnisa Istiadi</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Storify Waste v1.0")
# ==================== LOGIKA HALAMAN UTAMA ====================

# 📑 MENU 1: BERANDA UTAMA
if menu_pilihan == "🏠 Beranda Utama":
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="https://i.pinimg.com/736x/8f/13/c1/8f13c1dca7ce0e85ac51c0fba3a92f9a.jpg" style="width: 100%; max-height: 350px; object-fit: cover; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.08);" alt="Landscape Beranda">
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="max-width: 800px; margin: 0 auto; text-align: center; padding: 10px 0;">
            <h1 style="color: #059669; font-size: 38px; font-weight: 800; margin-bottom: 15px; line-height: 1.3;">
                Sistem Pemantauan & Kepatuhan <br><span style="color: #059669;">Limbah B3</span>
            </h1>
            <p style="color: #475569; font-size: 18px; line-height: 1.6; margin-bottom: 20px;">
                Solusi cerdas integratif untuk pencatatan logbook, standarisasi pengemasan, <br>
                pelacakan masa simpan real-time, serta penanggulangan tanggap darurat di TPS.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if lottie_home:
        col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
        with col_l2:
            st_lottie(lottie_home, speed=1, quality="high", height=150, key="home_lottie")
            
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
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="https://i.pinimg.com/736x/32/2d/e3/322de3bd660e7f097e4a3f06f801b564.jpg" style="width: 100%; max-height: 350px; object-fit: cover; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.08);" alt="Landscape Input Data">
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="max-width: 800px; margin: 0 auto; text-align: center; padding: 10px 0;">
            <h1 style="color: #14532d; font-size: 34px; font-weight: 800; margin-bottom: 12px;">
                Manajemen Logbook & Inventaris TPS
            </h1>
            <p style="color: #64748b; font-size: 16px; line-height: 1.5; margin-bottom: 15px;">
                Silakan masukkan data manifes limbah masuk di panel kiri. Data otomatis aman tersimpan secara lokal.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if lottie_form:
        col_lf1, col_lf2, col_lf3 = st.columns([1, 1, 1])
        with col_lf2:
            st_lottie(lottie_form, speed=1, quality="high", height=90, key="form_menu_top")
            
    st.markdown("---")
    col_f1, col_f2 = st.columns([1.1, 2.1])
    
    with col_f1:
        st.markdown("""
            <div style="background-color: #f8fafc; padding: 15px; border-radius: 8px; border-left: 4px solid #3b82f6; margin-bottom: 15px;">
                <b style="color: #1e3a8a;">📝 Formulir Entri Limbah</b>
            </div>
        """, unsafe_allow_html=True)
            
        with st.form(key="form_b3", clear_on_submit=True):
            jenis_limbah = st.selectbox("Pilih Jenis Limbah B3", list(B3_DATABASE.keys()))
            char_name = B3_DATABASE[jenis_limbah]["karakteristik"]
            logo_img = B3_DATABASE[jenis_limbah]["logo_url"]
            wadah_oto = B3_DATABASE[jenis_limbah]["wadah_rekomendasi"]
            
            st.markdown(f"""
                <div style="background-color: #ffffff; border: 1px solid #e2e8f0; padding: 15px; border-radius: 10px; margin-bottom: 15px; display: flex; align-items: center; gap: 15px;">
                    <img src="{logo_img}" width="65" style="object-fit: contain;" alt="Logo B3">
                    <div>
                        <span style="font-size: 12px; color: #64748b; display:block;">Simbol Regulasi Resmi:</span>
                        <b style="color: #dc2626; font-size: 15px;">{char_name}</b>
                    </div>
                </div>
                <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 12px; border-radius: 8px; margin-bottom: 15px;">
                    <span style="font-size: 13px; color: #64748b;">Rekomendasi Wadah Teknis:</span><br>
                    <span style="font-size: 14px; color: #334155; font-weight: 500; display:block; margin-top:4px;">{wadah_oto}</span>
                </div>
            """, unsafe_allow_html=True)
            
            berat = st.number_input("Berat Limbah Masuk (Kg)", min_value=1.0, step=10.0)
            tgl_masuk = st.date_input("Tanggal Masuk TPS", date.today())
            submit_btn = st.form_submit_button(label="Simpan Data Masuk 💾", use_container_width=True)
            
        if submit_btn:
            id_limbah = f"B3-{datetime.now().strftime('%M%S')}"
            batas_hari = B3_DATABASE[jenis_limbah]["masa_simpan"]
            sisa_hari = batas_hari - (date.today() - tgl_masuk).days
            
            status = "Aman"
            if sisa_hari <= 14:
                status = "KRITIS 🔴"
            elif sisa_hari <= 30:
                status = "Peringatan 🟡"

            new_data = pd.DataFrame([{
                "ID Limbah": id_limbah,
                "Jenis Limbah": jenis_limbah,
                "Karakteristik / Simbol": char_name,
                "Rekomendasi Wadah": wadah_oto,
                "Berat (Kg)": int(berat),
                "Tanggal Masuk": tgl_masuk,
                "Batas Hari": f"{batas_hari} Hari",
                "Sisa Hari": sisa_hari,
                "Status": status
            }])
            
            st.session_state.b3_db = pd.concat([st.session_state.b3_db, new_data], ignore_index=True)
            st.session_state.b3_db.to_csv(NAMA_FILE_DB, index=False)
            st.success("Sukses! Data telah tercatat dan tersimpan.")
            st.html("<script>window.location.reload();</script>")

    with col_f2:
        total_tonase = st.session_state.b3_db["Berat (Kg)"].sum() if not st.session_state.b3_db.empty else 0.0
        jml_kritis = len(st.session_state.b3_db[st.session_state.b3_db['Status'] == "KRITIS 🔴"]) if not st.session_state.b3_db.empty else 0
        jml_warning = len(st.session_state.b3_db[st.session_state.b3_db['Status'] == "Peringatan 🟡"]) if not st.session_state.b3_db.empty else 0
        
        m_col1, m_col2, m_col3 = st.columns(3)

        m_col1, m_col2, m_col3 = st.columns(3)

    with m_col1:
        val_berat = int(st.session_state.b3_db['Berat (Kg)'].sum()) if not st.session_state.b3_db.empty else 0
        st.markdown(f"""
        <div style="background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: left;">
            <span style="font-size: 13px; color: #64748b; font-weight: 600; display: block; margin-bottom: 5px;">TOTAL BERAT DATA</span>
            <span style="font-size: 24px; font-weight: 700; color: #10b981; display: block;">{val_berat} Kg</span>
        </div>
        """, unsafe_allow_html=True)

    with m_col2:
        val_warning = len(st.session_state.b3_db[st.session_state.b3_db['Status'].astype(str).str.contains('Peringatan', case=False, na=False)]) if not st.session_state.b3_db.empty else 0
        st.markdown(f"""
        <div style="background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: left;">
            <span style="font-size: 13px; color: #64748b; font-weight: 600; display: block; margin-bottom: 5px;">JUMLAH WARNING</span>
            <span style="font-size: 24px; font-weight: 700; color: #f59e0b; display: block;">{val_warning} Data</span>
        </div>
        """, unsafe_allow_html=True)
