import streamlit as st

# --- 1. ตั้งค่าหน้าตาเว็บ (UI Config) ---
st.set_page_config(page_title="SYNAPSE 6D", page_icon="🧬", layout="wide")

# ปรับสีให้เป็น ดำ-แดง ตามสไตล์ SYNAPSE
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    h1, h2, h3 { color: #ff4b4b !important; }
    .stButton>button { background-color: #ff4b4b; color: white; border-radius: 8px; border: none; }
    .stButton>button:hover { background-color: #ff3333; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ส่วนหัวข้อ (Header) ---
st.title("🧬 SYNAPSE 6D - AI Voice Engine")
st.write("เครื่องมือแปลงเสียงคุณภาพสูง (High-quality voice conversion tool)")

# --- 3. ส่วนการทำงาน (Main Interface) ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("## วางไฟล์ที่นี่ (Drop files)")
    uploaded_file = st.file_uploader("อัปโหลดเสียงร้อง (R&B/Rap/Hiphop)", type=["wav", "mp3"])
    
    # ดึงค่าจาก JSON ที่คุณส่งมา
    pitch = st.slider("ปรับระดับเสียง (Pitch Shift)", -12, 12, 0, help="Adjust input audio pitch")
    f0_method = st.selectbox("อัลกอริธึมสกัดระดับเสียง", ["rmvpe", "fcpe", "pm"])
    
    index_rate = st.slider("อัตราส่วนการผสม (Blend Ratio)", 0.0, 1.0, 0.75)

with col2:
    st.subheader("## ข้อมูลเอาต์พุต (Output Information)")
    if uploaded_file:
        st.audio(uploaded_file, format='audio/wav')
        
        if st.button("🚀 เริ่มการแปลงเสียง (Convert)"):
            with st.spinner('กำลังประมวลผล...'):
                # ส่วนนี้คือจุดที่จะเชื่อมกับ RVC จริงในขั้นตอนถัดไป
                st.info("ระบบกำลังจำลองการทำงาน (Mockup Mode)...")
                st.success("✅ การอนุมาน (Inference) สำเร็จ!")
                st.audio(uploaded_file) # ตอนนี้ให้ลองฟังไฟล์เดิมไปก่อน
    else:
        st.warning("กรุณาอัปโหลดไฟล์เสียงเพื่อเริ่มต้น")

# --- 4. ส่วนท้าย (Footer) ---
st.divider()
st.markdown("### [สนับสนุน](https://discord.gg/urxFjYmYYh) — [GitHub](https://github.com/IAHispano/Applio)")
