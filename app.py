import streamlit as st
import librosa
import soundfile as sf
import os

# --- SETUP UI SYNAPSE 6D (RED & BLACK STYLE) ---
st.set_page_config(page_title="SYNAPSE 6D", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #ff0000; }
    h1, h2, h3 { color: #ff0000 !important; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { 
        background-color: #ff0000; 
        color: white; 
        border-radius: 5px; 
        border: 2px solid #8B0000;
        font-weight: bold;
    }
    .stSlider > div > div > div > div { background-color: #ff0000; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧬 SYNAPSE 6D - AI VOCAL ENGINE")

col1, col2 = st.columns(2)

with col1:
    st.subheader("## วางไฟล์ที่นี่ (Drop files)")
    uploaded_file = st.file_uploader("อัปโหลดเสียงร้องของคุณ (MP3/WAV)", type=["mp3", "wav"])
    
    # Slider ปรับระดับเสียง
    pitch_val = st.slider("ปรับระดับเสียง (Pitch Shift)", -12, 12, 0)
    st.write(f"ระดับเสียงปัจจุบัน: {pitch_val} Semitones")

with col2:
    st.subheader("## ข้อมูลเอาต์พุต (Output Information)")
    if uploaded_file:
        st.write("🎵 เสียงต้นฉบับ:")
        st.audio(uploaded_file)
        
        if st.button("🚀 เริ่มการแปลงเสียง (Convert)"):
            with st.status("🔴 กำลังรัน Engine แดง...", expanded=True) as status:
                st.write("📥 กำลังโหลดข้อมูลคลื่นเสียง...")
                # โหลดไฟล์และประมวลผลจริง
                y, sr = librosa.load(uploaded_file, sr=None)
                
                st.write("📊 กำลังใช้ Pitch Shifting Algorithm...")
                y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch_val)
                
                output_file = "synapse_output.wav"
                sf.write(output_file, y_shifted, sr)
                
                status.update(label="🔴 แปลงเสียงสำเร็จ!", state="complete")
                
                st.write("🎤 ผลลัพธ์เสียงที่ผ่านการประมวลผล:")
                st.audio(output_file)
    else:
        st.info("รอรับไฟล์เสียงเข้าสู่ระบบ...")
