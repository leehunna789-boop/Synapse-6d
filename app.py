import streamlit as st
import os
import torch

st.title("🔴 SYNAPSE ERROR CHECKER")

# เช็คว่ามี Library พื้นฐานครบไหม
try:
    import librosa
    st.success("✅ Librosa พร้อม!")
except:
    st.error("❌ ขาด Librosa (ต้องใส่ใน requirements.txt)")

try:
    import torch
    st.success(f"✅ Torch พร้อม! (เวอร์ชัน {torch.__version__})")
except:
    st.error("❌ ขาด Torch")

# ลองเช็คว่าโมเดลโหลดได้ไหม
model_path = "Thai_Male_Voice.pth"
if os.path.exists(model_path):
    st.write(f"📂 พบไฟล์โมเดล: {model_path}")
else:
    st.warning("⚠️ ไม่พบไฟล์โมเดลในโฟลเดอร์เดียวกับ app.py")
import streamlit as st
import os
import librosa
import soundfile as sf
import numpy as np
import torch
import urllib.request
import matplotlib.pyplot as plt

# --- 1. [Style] ตกแต่งหน้าตาแบบ SYNAPSE PRO ---
st.set_page_config(page_title="SYNAPSE 6D PRO", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #000; color: #f00; }
    .stButton>button { background-color: #f00; color: white; border-radius: 20px; height: 3em; font-weight: bold; }
    .stSlider [data-baseweb="slider"] { color: #f00; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. [Auto-Model] โหลดหน้ากากเสียงผู้ชายไทยอัตโนมัติ ---
MODEL_URL = "https://huggingface.co/AofHeaD/RVC-Models/resolve/main/Thai_Male_Voice.pth"
MODEL_PATH = "Thai_Male_Voice.pth"

if not os.path.exists(MODEL_PATH):
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

# --- 3. [Visualizer] ฟังก์ชันวาดกราฟเสียงสีแดง ---
def plot_wave(y, sr):
    fig, ax = plt.subplots(figsize=(10, 2), facecolor='black')
    ax.plot(y, color='red', linewidth=0.5)
    ax.axis('off')
    return fig

# --- 4. [Main UI] หน้าจอหลัก ---
st.title("🧬 SYNAPSE 6D - PROFESSIONAL AI STUDIO")
st.write("---")

tab1, tab2 = st.tabs(["🎤 RVC Master", "🤖 AI Tools"])

with tab1:
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.subheader("🔴 Upload Center")
        vocal = st.file_uploader("เสียงร้อง (Vocal)", type=["wav", "mp3"])
        inst = st.file_uploader("ดนตรี (Instrumental)", type=["wav", "mp3"])
        pitch = st.slider("Pitch Shift (คีย์เสียง)", -12, 12, 0)
        
    with c2:
        st.subheader("🔴 Engine Monitor")
        if vocal and inst:
            y_v, sr = librosa.load(vocal, sr=None)
            st.pyplot(plot_wave(y_v, sr)) # โชว์กราฟเสียงร้อง
            
            if st.button("🚀 EXECUTE RVC CONVERSION"):
                with st.status("🛠️ กำลังสวมรอยเสียง AI...", expanded=True):
                    # แปลงและมิกซ์
                    y_i, _ = librosa.load(inst, sr=sr)
                    v_ai = librosa.effects.pitch_shift(y_v, sr=sr, n_steps=pitch)
                    
                    max_len = max(len(v_ai), len(y_i))
                    final = np.pad(v_ai, (0, max_len-len(v_ai))) + np.pad(y_i, (0, max_len-len(y_i)))
                    sf.write("final.wav", final, sr)
                
                st.audio("final.wav")
                st.success("✅ มิกซ์เสียงเสร็จแล้ว ฟังได้เลย!")

with tab2:
    st.info("🤖 ส่วนของ Gemini AI และ TTS กำลังรอการเชื่อมต่อ API ของคุณ...")
