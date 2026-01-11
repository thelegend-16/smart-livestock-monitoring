import streamlit as st
from datetime import datetime
import pandas as pd
from PIL import Image

st.set_page_config(
    page_title="Smart Livestock Management",
    page_icon="🐄",
    layout="wide"
)

# ================= SESSION STATE =================
if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = {"name": "", "email": "", "role": "Farmer"}

if "attendance_logs" not in st.session_state:
    st.session_state.attendance_logs = []

if "sub_page" not in st.session_state:
    st.session_state.sub_page = "home"

if "herd_data" not in st.session_state:
    st.session_state.herd_data = pd.DataFrame(
        columns=["ID", "Type", "Age", "Health Status"]
    )

# ================= LANGUAGE DATA =================
LANGUAGES = {
    "English": {
        "title": "Livestock Care App",
        "subtitle": "Smart monitoring for modern farmers",
        "welcome": "Welcome back,",
        "animals": "My Animals",
        "health": "Health Monitoring",
        "portal": "Farmer / Vet Portal",
        "attendance": "Attendance",
        "camera": "Camera & Upload",
        "dark": "Dark Mode",
        "profile": "Profile"
    },
    "Hindi": {
        "title": "पशुधन देखभाल ऐप",
        "subtitle": "आधुनिक किसानों के लिए स्मार्ट निगरानी",
        "welcome": "स्वागत है,",
        "animals": "मेरे पशु",
        "health": "स्वास्थ्य निगरानी",
        "portal": "किसान / पशु चिकित्सक पोर्टल",
        "attendance": "उपस्थिति",
        "camera": "कैमरा और अपलोड",
        "dark": "डार्क मोड",
        "profile": "प्रोफ़ाइल"
    }
}

# ================= AUTH STYLES =================
def auth_styles():
    st.markdown("""
    <style>
    .auth-container { text-align:center; padding:40px; }
    .title-box {
        background:#2e7d32; color:white; padding:20px;
        border-radius:16px; font-size:28px; font-weight:bold;
        margin-bottom:10px;
    }
    .welcome-subtext {
        color:#4caf50; font-size:18px; font-weight:600;
        margin-bottom:25px;
    }
    </style>
    """, unsafe_allow_html=True)

# ================= LOGIN =================
def login_page():
    auth_styles()
    _, c, _ = st.columns([1, 1.5, 1])
    with c:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('<div class="title-box">LIVESTOCK CARE APP</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-subtext">Welcome to Livestock Care App</div>', unsafe_allow_html=True)

        with st.form("login"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Access Dashboard"):
                if email and password:
                    st.session_state.user["email"] = email
                    st.session_state.user["name"] = email.split("@")[0].title()
                    st.session_state.page = "app"
                    st.rerun()

        if st.button("Create an Account"):
            st.session_state.page = "signup"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ================= SIGNUP =================
def signup_page():
    auth_styles()
    _, c, _ = st.columns([1, 1.5, 1])
    with c:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('<div class="title-box">CREATE ACCOUNT</div>', unsafe_allow_html=True)
        with st.form("signup"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Sign Up"):
                st.session_state.user = {"name": name, "email": email, "role": "Farmer"}
                st.session_state.page = "app"
                st.rerun()
        if st.button("Back to Login"):
            st.session_state.page = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ================= MAIN APP =================
def main_app():
    cl, ct, cp = st.columns([5, 2, 2])
    with cl:
        language = st.selectbox("🌐 Language", list(LANGUAGES.keys()))
    lang = LANGUAGES[language]
    with ct:
        dark_mode = st.toggle(f"🌙 {lang['dark']}", value=True)
    with cp:
        if st.button(f"👤 {lang['profile']}"):
            st.session_state.page = "profile"
            st.rerun()

    bg, card, text, primary = (
        ("#0e1117", "#1c2128", "#ffffff", "#4caf50")
        if dark_mode else
        ("#f8fafc", "#ffffff", "#1e293b", "#2e7d32")
    )

    st.markdown(f"""
    <style>
    .stApp {{ background:{bg}; color:{text}; }}
    .header {{
        background:linear-gradient(135deg,{primary},#81c784);
        padding:30px; border-radius:20px;
        color:white; text-align:center; margin-bottom:25px;
    }}
    .box {{
        text-align:center; padding:25px;
        border:2px solid {primary};
        border-radius:20px;
        background:{card};
    }}
    </style>
    """, unsafe_allow_html=True)

    if st.session_state.sub_page != "home":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.sub_page = "home"
            st.rerun()

    if st.session_state.sub_page == "home":
        render_home(lang)
    elif st.session_state.sub_page == "animals":
        render_animals(lang)
    elif st.session_state.sub_page == "health":
        render_health(lang)
    elif st.session_state.sub_page == "portal":
        render_vet_portal(lang)
    elif st.session_state.sub_page == "attendance":
        render_attendance(lang)
    elif st.session_state.sub_page == "camera":
        render_camera(lang)

# ================= HOME =================
def render_home(lang):
    st.markdown(f'<div class="header"><h1>🐄 {lang["title"]}</h1><p>{lang["subtitle"]}</p></div>', unsafe_allow_html=True)
    st.markdown(f"### {lang['welcome']} {st.session_state.user['name']} 👋")

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.markdown(f'<div class="box">🐄<br><b>{lang["animals"]}</b></div>', unsafe_allow_html=True)
        if st.button("Manage Herd", use_container_width=True):
            st.session_state.sub_page = "animals"; st.rerun()

    with r1c2:
        st.markdown(f'<div class="box">❤️<br><b>{lang["health"]}</b></div>', unsafe_allow_html=True)
        if st.button("Check Vitals", use_container_width=True):
            st.session_state.sub_page = "health"; st.rerun()

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.markdown(f'<div class="box">👨‍🌾<br><b>{lang["portal"]}</b></div>', unsafe_allow_html=True)
        if st.button("Find Vets", use_container_width=True):
            st.session_state.sub_page = "portal"; st.rerun()

    with r2c2:
        st.markdown(f'<div class="box">📅<br><b>{lang["attendance"]}</b></div>', unsafe_allow_html=True)
        if st.button("Attendance", use_container_width=True):
            st.session_state.sub_page = "attendance"; st.rerun()

    _, mid, _ = st.columns([1,2,1])
    with mid:
        st.markdown(f'<div class="box">📸<br><b>{lang["camera"]}</b></div>', unsafe_allow_html=True)
        if st.button("Open Camera / Upload", use_container_width=True):
            st.session_state.sub_page = "camera"; st.rerun()

# ================= CAMERA =================
def render_camera(lang):
    st.header(f"📸 {lang['camera']}")
    tab1, tab2 = st.tabs(["📷 Take Photo", "📁 Upload Image"])
    with tab1:
        img = st.camera_input("Capture Image")
        if img:
            st.image(img, use_container_width=True)
    with tab2:
        file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])
        if file:
            st.image(Image.open(file), use_container_width=True)

# ================= ATTENDANCE =================
def render_attendance(lang):
    st.header(f"📅 {lang['attendance']}")
    if st.button("Mark Present"):
        st.session_state.attendance_logs.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    if st.session_state.attendance_logs:
        st.table(pd.DataFrame(st.session_state.attendance_logs, columns=["Timestamp"]))

# ================= ANIMALS =================
def render_animals(lang):
    st.header(f"🐄 {lang['animals']}")
    with st.form("animal"):
        aid = st.text_input("Tag ID")
        atype = st.selectbox("Type", ["Cow","Buffalo","Goat","Sheep"])
        age = st.number_input("Age", 0)
        if st.form_submit_button("Add"):
            st.session_state.herd_data.loc[len(st.session_state.herd_data)] = [aid, atype, age, "Healthy"]
    st.dataframe(st.session_state.herd_data, use_container_width=True)

# ================= HEALTH =================
def render_health(lang):
    st.header(f"❤️ {lang['health']}")
    st.metric("Avg Temperature", "38.5 °C")
    st.metric("Activity Level", "High")

# ================= VET PORTAL =================
def render_vet_portal(lang):
    st.header(f"👨‍⚕️ {lang['portal']}")
    for v in ["Dr Sharma","Dr Verma"]:
        st.write(v)
        if st.button(f"Call {v}"): st.success("Calling...")

# ================= PROFILE =================
def profile_page():
    st.header("👤 Profile")
    st.write(st.session_state.user)
    if st.button("Logout"):
        st.session_state.page = "login"
        st.session_state.user = {"name":"","email":"","role":"Farmer"}
        st.rerun()
    if st.button("Back"):
        st.session_state.page = "app"
        st.rerun()

# ================= ROUTER =================
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "profile":
    profile_page()
else:
    main_app()
