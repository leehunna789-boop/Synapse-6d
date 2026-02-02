import streamlit as st
import librosa
import soundfile as sf
import numpy as np

# ... (โค้ดส่วนบนของคุณเหมือนเดิม) ...

if st.button("🚀 เริ่มการแปลงเสียง (Convert)"):
    if uploaded_file:
        with st.status("🤖 SYNAPSE Engine กำลังประมวลผล...", expanded=True) as status:
            # 1. โหลดไฟล์เสียงเข้ามาในระบบจริง ๆ
            st.write("📥 กำลังโหลดไฟล์เสียง...")
            y, sr = librosa.load(uploaded_file, sr=None)
            
            # 2. สกัดความถี่ (Pitch Extraction) และปรับระดับตามที่เลือกใน Slider
            st.write("📊 กำลังปรับระดับเสียง (Pitch Shifting)...")
            # pitch จาก Slider ที่คุณตั้งไว้
            y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch)
            
            # 3. บันทึกเป็นไฟล์ผลลัพธ์ชั่วคราว
            output_path = "output_voice.wav"
            sf.write(output_path, y_shifted, sr)
            
            status.update(label="✅ แปลงเสียงนักร้องสำเร็จ!", state="complete")
            
            st.write("🎤 ผลลัพธ์เสียงที่ผ่าน SYNAPSE Engine:")
            st.audio(output_path)
    else:
        st.error("กรุณาอัปโหลดไฟล์ก่อนครับ!")
