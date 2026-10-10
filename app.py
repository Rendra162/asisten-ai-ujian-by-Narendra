import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="M Solver - Ultimate VIP Edition",
    page_icon="⚡",
    layout="centered"
)

# 2. Desain CSS Kustom (Futuristic VIP Dark Mode & Floating UI)
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    
    /* Tombol Utama Estetik */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: bold;
        color: white;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        border: none;
        padding: 12px;
        box-shadow: 0px 4px 15px rgba(99, 102, 241, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
        box-shadow: 0px 6px 20px rgba(99, 102, 241, 0.6);
    }

    /* Panel Kontrol Mengambang (Floating Style Box) */
    .floating-panel {
        background: #111827;
        border: 2px solid #374151;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.7);
        margin-bottom: 20px;
    }
    
    .panel-header {
        color: #38bdf8;
        font-size: 18px;
        font-weight: bold;
        font-family: monospace;
        text-align: center;
        letter-spacing: 1.5px;
        margin-bottom: 5px;
    }

    /* Kotak Hasil Jawaban */
    .result-box {
        background: #1f2937;
        border-left: 6px solid #38bdf8;
        padding: 18px;
        border-radius: 8px;
        margin-top: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
    }
    
    .badge {
        background-color: #374151;
        color: #38bdf8;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
        font-family: monospace;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Konfigurasi Gemini AI
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API Key Gemini belum dikonfigurasi di Streamlit Secrets!")

# Inisialisasi Riwayat Sesi (Session State) di memori aplikasi
if "history" not in st.session_state:
    st.session_state.history = []

# 4. Header / Floating Control Panel
st.markdown("""
    <div class="floating-panel">
        <div class="panel-header">⚡ M SOLVER ULTIMATE VIP ⚡</div>
        <div style="text-align: center; color: #9ca3af; font-size: 12px;">
            AI Smart Exam Engine • Auto-Subject Detect • Instant Solver
        </div>
    </div>
""", unsafe_allow_html=True)

# 5. Pengaturan Mode Jawab Cerdas
with st.expander("⚙️ Konfigurasi Tampilan Jawaban AI"):
    mode_output = st.radio(
        "Pilih format keluaran jawaban:",
        ["🎯 Target Utama: Jawaban Singkat & Jelas (A/B/C/D/E)", "📖 Pembahasan Lengkap + Analisis Rumus & Tingkat Kesulitan"]
    )

st.markdown("---")

# 6. Fitur Utama: Tangkap Layar / Kamera Langsung
st.markdown("### 📸 Tangkap Soal Secara Instan")
st.info("💡 **Tips:** Arahkan kamera HP ke layar soal, ambil foto, dan biarkan M Solver membongkar jawabannya.")

foto_soal = st.camera_input("Ambil foto soal ujian:")

if foto_soal is not None:
    with st.spinner("🤖 M Solver sedang menganalisis tingkat kesulitan & mencari jawaban..."):
        try:
            img_bytes = foto_soal.getvalue()
            img_parts = [{"mime_type": "image/jpeg", "data": img_bytes}]
            
            if "Target Utama" in mode_output:
                prompt_instruction = "Berikan jawaban akhir atau pilihan ganda yang benar (A/B/C/D/E) secara sangat jelas di baris pertama."
            else:
                prompt_instruction = """Berikan format terstruktur berikut:
                1. **Mata Pelajaran Terdeteksi:** (Matematika/Fisika/Inggris/dll)
                2. **Tingkat Kesulitan:** (Mudah / Sedang / Sulit / HOTS)
                3. **Jawaban Benar / Opsi:** (A/B/C/D/E atau hasil akhir)
                4. **Pembahasan & Rumus Cepat:** (Langkah pengerjaan ringkas)"""
            
            prompt = f"""Kamu adalah M Solver, asisten ujian AI elit. Analisis gambar soal ini dengan cermat. 
            {prompt_instruction}"""
            
            response = model.generate_content([prompt, img_parts[0]])
            hasil_ai = response.text
            
            # Simpan ke riwayat sesi
            st.session_state.history.insert(0, {"tipe": "Foto", "isi": hasil_ai})
            
            # Tampilkan Hasil
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### 🎯 Hasil Analisis M Solver:")
            st.write(hasil_ai)
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Gagal memproses gambar: {e}")

st.markdown("---")

# 7. Fitur AI Chat Assistant (Ruang Tanya Jawab Bebas)
st.markdown("### 💬 AI Chat Assistant")
st.write("Ada materi atau rumus tambahan yang ingin ditanyakan? Diskusikan langsung di sini.")

user_query = st.text_input("Tulis pertanyaan atau materi:", placeholder="Contoh: Bagaimana cara cepat menghitung hukum Ohm?")

if st.button("🚀 Kirim Pertanyaan"):
    if user_query:
        with st.spinner("M Solver sedang merumuskan jawaban..."):
            chat_res = model.generate_content(user_query)
            jawaban_chat = chat_res.text
            
            # Simpan ke riwayat sesi
            st.session_state.history.insert(0, {"tipe": "Chat", "isi": jawaban_chat})
            
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### 🤖 Jawaban Asisten:")
            st.write(jawaban_chat)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Silakan ketik pertanyaan terlebih dahulu!")

# 8. Fitur Riwayat Sesi (Session History)
if len(st.session_state.history) > 0:
    with st.expander(f"📜 Riwayat Soal & Sesi Aktif ({len(st.session_state.history)})"):
        if st.button("🗑️ Hapus Riwayat"):
            st.session_state.history = []
            st.rerun()
            
        for i, item in enumerate(st.session_state.history[:5]): # Tampilkan 5 riwayat terakhir
            st.markdown(f"**[{item['tipe']}] Riwayat #{i+1}:**")
            st.info(item['isi'][:150] + "...") # Pratinjau teks

# Footer VIP Elit
st.markdown("---")
st.markdown("<p style='text-align: center; color: #4b5563; font-size: 11px;'>M Solver Ultimate VIP • Powered by Google Gemini AI</p>", unsafe_allow_html=True)
