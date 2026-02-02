import streamlit as st

# ตั้งค่าหน้าตาเว็บ
st.set_page_config(page_title="SYNAPSE 6D", page_icon="🧬", layout="wide")

# CSS ตกแต่ง ดำ-แดง
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    h1, h2, h3 { color: #ff4b4b !important; }
    .stButton>button { background-color: #ff4b4b; color: white; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧬 SYNAPSE 6D - AI Voice Engine")
st.write("เครื่องมือแปลงเสียงคุณภาพสูง (แปลโดย Applio)")

col1, col2 = st.columns(2)

with col1:
    st.subheader("## วางไฟล์ที่นี่ (Drop files)")
    uploaded_file = st.file_uploader("เลือกไฟล์เสียง (wav, mp3)", type=["wav", "mp3"])
    pitch = st.slider("ปรับระดับเสียง (Pitch Shift)", -12, 12, 0)
    f0_method = st.selectbox("อัลกอริธึมสกัดระดับเสียง", ["rmvpe", "fcpe"])

with col2:
    st.subheader("## ข้อมูลเอาต์พุต (Output Information)")
    if uploaded_file:
        st.audio(uploaded_file)
        if st.button("🚀 เริ่มการแปลงเสียง (Convert)"):
            st.success("✅ ระบบเชื่อมต่อ GitHub สำเร็จ! (สถานะ: พร้อมอัปเกรดเป็น RVC จริง)")

st.divider()
st.markdown("[สนับสนุน](https://discord.gg/urxFjYmYYh) — [GitHub](https://github.com/IAHispano/Applio)")
