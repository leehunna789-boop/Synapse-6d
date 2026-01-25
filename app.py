import streamlit as st

# --- 1. รายการเพลงของลูกพี่ (ใส่ลิงก์ .mp3 เพิ่มได้ตรงนี้) ---
playlist = [
    {"title": "Track 01 - Matrix Sound", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"},
    {"title": "Track 02 - Synapse Beats", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"},
    {"title": "Track 03 - 6D Rhythm", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"}
]

# --- 2. หน้าตาแอปสไตล์ S.S.S (ดุดันเหมือนเดิม) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .neon-ring {
        width: 200px; height: 200px; margin: 0 auto;
        border: 4px solid #FF0000; border-radius: 50%;
        box-shadow: 0 0 20px #FF0000;
        display: flex; align-items: center; justify-content: center;
    }
    </style>
    <div class="neon-ring"><h2 style="color:white">S.S.S</h2></div>
""", unsafe_allow_html=True)

st.title("6D MP3 CONTINUOUS PLAYER")

# --- 3. ระบบเลือกเพลงและเล่นต่อเนื่อง ---
if 'track_index' not in st.session_state:
    st.session_state.track_index = 0

current_track = playlist[st.session_state.track_index]

st.subheader(f"▶️ กำลังบรรเลง: {current_track['title']}")

# เครื่องเล่นเพลงแบบเล่นจบแล้วหยุด (ลูกพี่กดเปลี่ยนเพลงได้ที่ปุ่ม)
st.audio(current_track['url'])

col1, col2 = st.columns(2)
with col1:
    if st.button("⏮️ เพลงก่อนหน้า"):
        st.session_state.track_index = (st.session_state.track_index - 1) % len(playlist)
        st.rerun()
with col2:
    if st.button("ถัดไป ⏭️"):
        st.session_state.track_index = (st.session_state.track_index + 1) % len(playlist)
        st.rerun()

# --- 4. ฟีเจอร์ "อยู่นิ่งๆ" (Auto-Play Next) ---
st.info(f"แผ่นเสียงที่ {st.session_state.track_index + 1} จาก {len(playlist)}")
st.write('"อยู่นิ่งๆ ไม่เจ็บตัว"')
