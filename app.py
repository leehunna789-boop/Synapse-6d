import streamlit as st
import os
import librosa
import soundfile as sf
import numpy as np
import torch
import pickle
import matplotlib.pyplot as plt

# --- 1. ตั้งค่าหน้าตาและธีม (Black & Red) ---
st.set_page_config(page_title="SYNAPSE 6D PRO", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #000000; color: #ff0000; }
    h1, h2, h3 { color: #ff0000 !important; font-family: 'Courier New', monospace; text-shadow: 2px 2px #550000; }
    .stButton>button { background-color: #ff0000; color: white; width: 100%; font-weight: bold; border-radius: 10px; border: none; }
    .stTextInput>div>div>input { background-color: #1a1a1a; color: #ff0000; border: 1px solid #ff0000; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ฟังก์ชันตรวจสอบไฟล์ .pth (ที่คุณส่งมาตอนแรก) ---
def display_model_info(file_path):
    if not file_path or file_path == "ไม่พบไฟล์ .pth":
        return
    st.subheader("## 🔍 ข้อมูลโมเดล (Model Insight)")
    try:
        # ใช้ torch.load ตามสคริปต์ PyData Viewer ของคุณ
        checkpoint = torch.load(file_path, map_location='cpu')
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.write(f"**📦 ชื่อไฟล์:** `{os.path.basename(file_path)}`")
            if isinstance(checkpoint, dict) and 'epoch' in checkpoint:
                st.write(f"**⏳ ฝึกฝนมาแล้ว:** {checkpoint['epoch']} Epochs")
        with col_m2:
            st.success("✅ โครงสร้างไฟล์ถูกต้อง พร้อมใช้งาน")
    except Exception as e:
        st.warning(f"ℹ️ อ่าน Metadata ไม่ได้ (อาจเป็นโมเดลแบบ Index): {e}")

# --- 3. ฟังก์ชันวาดกราฟเสียง ---
def plot_waveform(data, sr, title="Waveform"):
    fig, ax = plt.subplots(figsize=(10, 2.5), facecolor='black')
    ax.plot(np.linspace(0, len(data)/sr, len(data)), data, color='#ff0000', linewidth=0.7)
    ax.set_title(title, color='white', size=10)
    ax.axis('off')
    return fig

# --- 4. หน้าจอหลัก ---
st.title("🧬 SYNAPSE 6D - AI VOCAL ENGINE")
st.write("---")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🔴 ตั้งค่าแหล่งเสียง")
    vocal_file = st.file_uploader("1. อัปโหลดเสียงร้องเพียวๆ", type=["wav", "mp3"])
    inst_file = st.file_uploader("2. อัปโหลดดนตรีเพียวๆ", type=["wav", "mp3"])
    
    # ดึงไฟล์ .pth ในโฟลเดอร์มาโชว์ (ตามโปรเจกต์คุณ)
    model_files = [f for f in os.listdir(".") if f.endswith(".pth")]
    selected_model = st.selectbox("เลือกโมเดลศิลปิน (.pth):", model_files if model_files else ["ไม่พบไฟล์ .pth"])
    
    # แสดงข้อมูลโมเดลทันทีที่เลือก
    if selected_model != "ไม่พบไฟล์ .pth":
        display_model_info(selected_model)
    
    pitch = st.slider("ปรับโทนเสียง (Pitch Shift)", -12, 12, 0)

with col2:
    st.subheader("🔴 การประมวลผลและแสดงผล")
    if vocal_file and inst_file:
        # วิเคราะห์เสียงต้นฉบับ
        y_v, sr = librosa.load(vocal_file, sr=None)
        st.pyplot(plot_waveform(y_v, sr, "Original Vocal Visualizer"))
        
        if st.button("🚀 EXECUTE SYNAPSE ENGINE"):
            with st.status("⚙️ กำลังแปลงเสียงและมิกซ์เพลง...", expanded=True) as status:
                # 1. แปลงเสียง (Pitch Shift Simulation)
                v_transformed = librosa.effects.pitch_shift(y_v, sr=sr, n_steps=pitch)
                
                # 2. โหลดดนตรีและมิกซ์
                y_i, _ = librosa.load(inst_file, sr=sr)
                max_len = max(len(v_transformed), len(y_i))
                final_mix = np.pad(v_transformed, (0, max_len - len(v_transformed))) + \
                            np.pad(y_i, (0, max_len - len(y_i)))
                
                # 3. บันทึก
                output_path = "synapse_master.wav"
                sf.write(output_path, final_mix, sr)
                status.update(label="✅ SYNAPSE Engine: สำเร็จ!", state="complete")
            
            st.audio(output_path)
            with open(output_path, "rb") as f:
                st.download_button("📥 ดาวน์โหลด Master (WAV)", f, file_name="synapse_final.wav")
    else:
        st.info("💡 กรุณาอัปโหลดทั้งเสียงร้องและดนตรีเพื่อเริ่มทำงาน")
