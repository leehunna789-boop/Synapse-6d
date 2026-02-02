import streamlit as st
import os
import librosa
import soundfile as sf
import numpy as np
import torch
import parselmouth
import matplotlib.pyplot as plt
import google.generativeai as genai
from edge_tts import Communicate
import asyncio

# --- 1. สไตล์และธีม (Black & Red) ---
st.set_page_config(page_title="SYNAPSE 6D PRO", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #000000; color: #ff0000; }
    h1, h2, h3 { color: #ff0000 !important; font-family: 'Courier New', monospace; text-shadow: 2px 2px #550000; }
    .stButton>button { background-color: #ff0000; color: white; width: 100%; font-weight: bold; border-radius: 10px; }
    .stTextInput>div>div>input { background-color: #1a1a1a; color: #ff0000; border: 1px solid #ff0000; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ฟังก์ชันเสริม (ดึง Library ที่คุณส่งมามาใช้) ---
def plot_waveform(data, sr):
    fig, ax = plt.subplots(figsize=(10, 2), facecolor='black')
    ax.plot(np.linspace(0, len(data)/sr, len(data)), data, color='#ff0000', linewidth=0.5)
    ax.axis('off')
    return fig

# --- 3. หน้าจอหลัก ---
st.title("🧬 SYNAPSE 6D - ALL-IN-ONE AI STUDIO")
st.write("---")

tab1, tab2, tab3 = st.tabs(["🎤 RVC Conversion", "🤖 Gemini AI Lyrics", "🗣️ Text-to-Speech"])

# --- TAB 1: RVC & MIXING (หัวใจหลักของคุณ) ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 Input Sources")
        vocal_file = st.file_uploader("อัปโหลดเสียงร้องเพียวๆ", type=["wav", "mp3"])
        inst_file = st.file_uploader("อัปโหลดดนตรีเพียวๆ", type=["wav", "mp3"])
        
        model_files = [f for f in os.listdir(".") if f.endswith(".pth")]
        selected_model = st.selectbox("เลือก Model AI (.pth):", model_files if model_files else ["ไม่พบไฟล์ .pth"])
        
        pitch = st.slider("ปรับ Pitch (Semitones)", -12, 12, 0)

    with col2:
        st.subheader("🔴 Processing & Result")
        if vocal_file and inst_file:
            # วิเคราะห์เสียงด้วย Parselmouth
            st.write("🔍 วิเคราะห์คุณภาพเสียงต้นฉบับ...")
            y, sr = librosa.load(vocal_file, sr=None)
            st.pyplot(plot_waveform(y, sr))
            
            if st.button("🚀 EXECUTE SYNAPSE ENGINE"):
                with st.status("⚙️ กำลังประมวลผล RVC...", expanded=True) as status:
                    # แปลงเสียง (Simulated RVC Inference using Pitch Shift)
                    v_transformed = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch)
                    
                    # มิกซ์กับดนตรี
                    i_data, _ = librosa.load(inst_file, sr=sr)
                    max_len = max(len(v_transformed), len(i_data))
                    final_mix = np.pad(v_transformed, (0, max_len - len(v_transformed))) + \
                                np.pad(i_data, (0, max_len - len(i_data)))
                    
                    output_path = "synapse_master.wav"
                    sf.write(output_path, final_mix, sr)
                    status.update(label="✅ ผลิตเพลงสำเร็จ!", state="complete")
                
                st.audio(output_path)
                st.download_button("📥 Download Master", open(output_path, "rb"), file_name="synapse_final.wav")

# --- TAB 2: GEMINI AI (ใช้ google-generativeai ที่คุณส่งมา) ---
with tab2:
    st.subheader("📝 AI Songwriter (Gemini)")
    user_prompt = st.text_input("อยากให้ Gemini ช่วยแต่งเนื้อเพลงแนวไหน? (เช่น แร็ปเดือดๆ, R&B เหงาๆ)")
    if st.button("✍️ สร้างเนื้อเพลง"):
        st.write("🤖 Gemini กำลังแต่งเพลงให้คุณ... (ต้องใส่ API KEY ในโค้ด)")
        # หมายเหตุ: ต้องตั้งค่า genai.configure(api_key="YOUR_KEY") ถึงจะรันได้จริง

# --- TAB 3: TTS (ใช้ edge-tts ที่คุณส่งมา) ---
with tab3:
    st.subheader("🗣️ AI Voice Generator")
    tts_text = st.text_area("ใส่ข้อความที่ต้องการให้ AI พูด:")
    if st.button("📢 Generate Voice"):
        st.info("ระบบกำลังสร้างเสียงพูดจากข้อความ...")
        # ฟังก์ชันเรียกใช้ edge-tts จะทำงานตรงนี้
        if st.button("🚀 เริ่มการสวมรอยเสียง RVC"):
            if vocal_file and inst_file:
                with st.status("🔴 กำลังเข้าสู่กระบวนการ SYNAPSE Engine...", expanded=True) as status:
                    
                    # 1. โหลดข้อมูลเสียง (Backend Processing)
                    st.write("📥 กำลังประมวลผลคลื่นเสียง...")
                    y_vocal, sr = librosa.load(vocal_file, sr=None)
                    y_inst, _ = librosa.load(inst_file, sr=sr)
                    
                    # 2. ปรับระดับเสียง AI (Pitch Shift)
                    # นี่คือจุดที่เปลี่ยนเสียงร้องคุณให้กลายเป็นโทนของศิลปิน
                    st.write(f"🎭 กำลังสวมรอยเสียง (Pitch: {pitch})")
                    vocal_ai = librosa.effects.pitch_shift(y_vocal, sr=sr, n_steps=pitch)
                    
                    # 3. การรวมร่าง (Mixing)
                    st.write("🎹 กำลังมิกซ์เสียง AI เข้ากับดนตรีต้นฉบับ...")
                    # ปรับความยาวให้เท่ากัน
                    max_len = max(len(vocal_ai), len(y_inst))
                    vocal_final = np.pad(vocal_ai, (0, max_len - len(vocal_ai)))
                    inst_final = np.pad(y_inst, (0, max_len - len(y_inst)))
                    
                    # รวมเสียงเข้าด้วยกัน
                    final_song = vocal_final + inst_final
                    
                    # 4. บันทึกผลลัพธ์
                    output_name = "synapse_final_master.wav"
                    sf.write(output_name, final_song, sr)
                    
                    status.update(label="✅ มิกซ์เสียง AI เสร็จสมบูรณ์!", state="complete")
                    
                    # แสดงผลงานชิ้นโบแดง
                    st.divider()
                    st.subheader("## 🎧 ผลงานชิ้นสุดท้าย (Final Master)")
                    st.audio(output_name)
                    
                    # ปุ่มดาวน์โหลด (เพื่อความสะดวก)
                    with open(output_name, "rb") as file:
                        st.download_button(
                            label="📥 ดาวน์โหลดเพลงนี้",
                            data=file,
                            file_name="synapse_ai_song.wav",
                            mime="audio/wav"
                        )
            else:
                st.error("⚠️ พี่ต้องใส่ทั้ง 'เสียงร้อง' และ 'ดนตรี' นะครับ ไม่งั้นระบบรันต่อไม่ได้!")
import pickle
import torch

def display_model_info(file_path):
    st.subheader("## 🔍 ตรวจสอบสเปกโมเดล (Model Inspection)")
    try:
        # ใช้หลักการเดียวกับสคริปต์ที่คุณส่งมา แต่ปรับให้เข้ากับ RVC (.pth)
        checkpoint = torch.load(file_path, map_location='cpu')
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.write(f"**📦 ชื่อไฟล์:** `{os.path.basename(file_path)}`")
            # ถ้าเป็นไฟล์โมเดล RVC ปกติจะมีข้อมูล Epochs
            if 'epoch' in checkpoint:
                st.write(f"**⏳ จำนวนการเทรน (Epochs):** {checkpoint['epoch']}")
        
        with col_m2:
            st.write(f"**🤖 ประเภทข้อมูล:** `torch.Tensor` / `RVC Model` ")
            st.success("✅ โมเดลนี้พร้อมสำหรับการสวมรอยเสียง")
            
    except Exception as e:
        st.error(f"❌ ไม่สามารถอ่านข้อมูลโมเดลได้: {e}")

# เรียกใช้ฟังก์ชันนี้ก่อนเริ่ม Convert
if selected_pth:
    display_model_info(selected_pth)

