import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้าเว็บให้กว้างและสวยงาม
st.set_page_config(page_title="Media Hub Pro", layout="wide")

# --- ส่วนของ CSS สำหรับตัวหนังสือวิ่ง (Scrolling Text) ---
st.markdown("""
    <style>
    .scroll-container {
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        padding: 10px 0;
        margin-bottom: 20px;
    }
    .scroll-text {
        display: inline-block;
        font-size: 20px;
        font-weight: bold;
        color: white;
        animation: scroll 20s linear infinite;
    }
    @keyframes scroll {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    .bg-yt { background: linear-gradient(90deg, #FF0000, #CC0000); }
    .bg-fb { background: linear-gradient(90deg, #1877F2, #0D47A1); }
    .bg-tk { background: linear-gradient(90deg, #000000, #25F4EE); }
    </style>
""", unsafe_allow_html=True)

def scrolling_banner(text, color_class):
    st.markdown(f"""
        <div class="scroll-container {color_class}">
            <div class="scroll-text">{text} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {text} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {text}</div>
        </div>
    """, unsafe_allow_html=True)

# --- ส่วนเนื้อหาหลัก ---
st.title("📺 ระบบรวมสื่อ Media & Scrolling Text")

# ลิงก์ที่คุณให้มา
links = {
    "Facebook": "https://www.facebook.com",
    "YouTube": "https://youtube.com",
    "TikTok": "https://www.tiktok.com"
}

# 1. แถบ YouTube
scrolling_banner("● LIVE FROM YOUTUBE CHANNEL ● แหล่งรวมวิดีโอคุณภาพ ●", "bg-yt")
with st.container(border=True):
    st.subheader("YouTube Channel")
    st.info(f"🔗 [คลิกที่นี่เพื่อเปิดหน้า YouTube ของคุณ]({links['YouTube']})")
    # ฝังวิดีโอตัวอย่าง (ถ้ามีลิงก์วิดีโอตรงๆ จะดีมาก)
    st.video("https://www.youtube.com") # ตัวอย่างวิดีโอ

# 2. แถบ Facebook
scrolling_banner("● FACEBOOK UPDATES ● ติดตามข่าวสารได้ที่นี่ ●", "bg-fb")
with st.container(border=True):
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Facebook Profile")
        st.write("ดูความเคลื่อนไหวล่าสุดจาก Facebook")
        st.link_button("ไปที่ Facebook", links["Facebook"])
    with col2:
        # ฝัง Page Plugin แบบง่าย
        fb_html = f'<iframe src="https://www.facebook.com{links["Facebook"]}&tabs=timeline&width=340&height=331&small_header=false&adapt_container_width=true&hide_cover=false&show_facepile=true" width="340" height="331" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowfullscreen="true" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"></iframe>'
        components.html(fb_html, height=350)

# 3. แถบ TikTok
scrolling_banner("● TIKTOK TRENDS ● วิดีโอสั้นสุดฮิต ●", "bg-tk")
with st.container(border=True):
    st.subheader("TikTok Creator")
    tk_html = f'''
    <blockquote class="tiktok-embed" data-unique-id="user1010970801941" data-embed-type="creator" style="max-width: 780px; min-width: 288px;" >
        <section> <a target="_blank" href="{links['TikTok']}">@user1010970801941</a> </section>
    </blockquote>
    <script async src="https://www.tiktok.com"></script>
    '''
    components.html(tk_html, height=500, scrolling=True)

st.success("แอปทำงานปกติบน Streamlit Cloud แล้วครับ! 🎉")
