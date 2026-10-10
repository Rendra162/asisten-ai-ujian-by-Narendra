import streamlit as st
import requests
from bs4 import BeautifulSoup
from google import genai

# Konfigurasi Halaman Web
st.set_page_config(page_title="Asisten AI Ujian Otomatis", page_icon="🤖", layout="centered")

# Judul Aplikasi
st.title("🤖 Asisten AI Ujian (Otomatis Baca Link)")
st.write("Masukkan link soal atau ketik pertanyaan, lalu biarkan AI membaca dan mengerjakannya!")

# --- SIDEBAR UNTUK API KEY & DATA UJIAN ---
st.sidebar.header("🔑 Pengaturan & Data Ujian")
api_key_input = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")

st.sidebar.subheader("Data Siswa")
nama_siswa = st.sidebar.text_input("Nama Kamu", "Aditya")
kelas = st.sidebar.text_input("Kelas", "X11")
token_ujian = st.sidebar.text_input("Token Ujian", "Horee")

# Fungsi untuk mengambil teks dari sebuah URL/Link
def ambil_teks_dari_link(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()
            teks = soup.get_text(separator=' ', strip=True)
            return teks
        else:
            return f"Gagal mengakses link. Status code: {response.status_code}"
    except Exception as e:
        return f"Terjadi kesalahan saat membaca link: {e}"

# --- AREA UTAMA ---
if not api_key_input:
    st.warning("⚠️ Silakan masukkan **Gemini API Key** Anda di panel sebelah kiri terlebih dahulu.")
else:
    client = genai.Client(api_key=api_key_input)

    link_input = st.text_input("🔗 Masukkan Link Ujian / Web Soal:", placeholder="https://contoh-link-soal.com")
    catatan_tambahan = st.text_area("Atau ketik pertanyaan/instruksi tambahan (opsional):", placeholder="Contoh: Pilihkan jawaban yang benar untuk soal-soal di link tersebut.")

    if st.button("Proses Soal dengan AI 🚀", type="primary"):
        if not link_input and not catatan_tambahan:
            st.error("Silakan masukkan minimal Link Ujian atau ketik pertanyaan!")
        else:
            with st.spinner("Sedang membaca link dan memproses soal dengan AI..."):
                try:
                    konten_dari_web = ""
                    if link_input:
                        st.info(f"Mengambil data dari link: {link_input}...")
                        konten_dari_web = ambil_teks_dari_link(link_input)
                    
                    prompt_lengkap = f"""
                    Anda adalah asisten AI yang cerdas untuk membantu siswa bernama {nama_siswa} dari kelas {kelas}.
                    Berikut adalah isi teks yang diambil dari link ujian yang diberikan:
                    
                    --- ISI LINK UJIAN ---
                    {konten_dari_web}
                    ----------------------
                    
                    Instruksi / Pertanyaan Tambahan dari Siswa:
                    {catatan_tambahan}
                    
                    Tolong analisis teks ujian di atas, berikan jawaban atau solusi yang akurat dan jelas untuk setiap soal yang ada di dalamnya.
                    """

                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=prompt_lengkap,
                    )
                    
                    st.success("Berhasil diselesaikan oleh AI!")
                    st.markdown("### 💡 Hasil / Kunci Jawaban:")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

    st.markdown("---")
    st.caption(f"Sesi aktif: **{nama_siswa}** | Kelas: **{kelas}** | Token: **{token_ujian}**")