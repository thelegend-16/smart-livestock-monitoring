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
        st.markdown('<div class="welcome-subtext">Welcome</div>', unsafe_allow_html=True)

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

# ================= MAIN APP LAYOUT =================
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
    .box-icon {{
        text-align:center; padding:15px;
        border:2px solid {primary};
        border-bottom: none;
        border-radius:20px 20px 0 0;
        background:{card};
        font-size: 30px;
    }}
    /* Custom button styling to snap to the icon box */
    div.stButton > button {{
        border-radius: 0 0 20px 20px !important;
        border: 2px solid {primary} !important;
        border-top: none !important;
        background-color: {card} !important;
        color: {text} !important;
        height: 50px;
        font-weight: bold;
    }}
    div.stButton > button:hover {{
        background-color: {primary} !important;
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    if st.session_state.sub_page != "home":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.sub_page = "home"
            st.rerun()

    # Routing
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

# ================= HOME PAGE =================
def render_home(lang):
    st.markdown(f'<div class="header"><h1>🐄 {lang["title"]}</h1><p>{lang["subtitle"]}</p></div>', unsafe_allow_html=True)
    st.markdown(f"### {lang['welcome']} {st.session_state.user['name']} 👋")

    # Camera at top center
    _, mid, _ = st.columns([1,2,1])
    with mid:
        st.markdown('<div class="box-icon">📸</div>', unsafe_allow_html=True)
        if st.button(lang["camera"], use_container_width=True):
            st.session_state.sub_page = "camera"; st.rerun()

    st.write("") 

    # Grid for other 4 features
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.markdown('<div class="box-icon">🐄</div>', unsafe_allow_html=True)
        if st.button(lang["animals"], use_container_width=True):
            st.session_state.sub_page = "animals"; st.rerun()
    with r1c2:
        st.markdown('<div class="box-icon">❤️</div>', unsafe_allow_html=True)
        if st.button(lang["health"], use_container_width=True):
            st.session_state.sub_page = "health"; st.rerun()

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.markdown('<div class="box-icon">👨‍🌾</div>', unsafe_allow_html=True)
        if st.button(lang["portal"], use_container_width=True):
            st.session_state.sub_page = "portal"; st.rerun()
    with r2c2:
        st.markdown('<div class="box-icon">📅</div>', unsafe_allow_html=True)
        if st.button(lang["attendance"], use_container_width=True):
            st.session_state.sub_page = "attendance"; st.rerun()

# ================= FEATURE PAGES =================
def render_camera(lang):
    st.header(f"📸 {lang['camera']}")
    tab1, tab2 = st.tabs(["📷 Take Photo", "📁 Upload Image"])
    with tab1:
        img = st.camera_input("Capture Animal")
        if img: st.image(img, use_container_width=True)
    with tab2:
        file = st.file_uploader("Upload", type=["jpg","png","jpeg"])
        if file: st.image(Image.open(file), use_container_width=True)

def render_attendance(lang):
    st.header(f"📅 {lang['attendance']}")
    if st.button("✅ Mark Attendance"):
        st.session_state.attendance_logs.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        st.success("Success!")
    if st.session_state.attendance_logs:
        st.table(pd.DataFrame(st.session_state.attendance_logs, columns=["Timestamp"]))

def render_animals(lang):
    st.header(f"🐄 {lang['animals']}")
    with st.form("add_animal"):
        aid = st.text_input("Tag ID")
        atype = st.selectbox("Type", ["Cow","Buffalo","Goat","Sheep"])
        age = st.number_input("Age", 0)
        if st.form_submit_button("Add"):
            st.session_state.herd_data.loc[len(st.session_state.herd_data)] = [aid, atype, age, "Healthy"]
    st.dataframe(st.session_state.herd_data, use_container_width=True)

def render_health(lang):
    st.header(f"❤️ {lang['health']}")
    st.metric("Avg Temp", "38.5 °C")
    st.metric("Activity", "High")

def render_vet_portal(lang):
    st.header(f"👨‍⚕️ {lang['portal']}")
    vets = ["Dr. Sharma (2km)", "Dr. Verma (5km)"]
    for v in vets:
        with st.container(border=True):
            st.write(f"**{v}**")
            if st.button(f"Call {v.split()[1]}"): st.info("Dialing...")

# ================= NAVIGATION =================
def signup_page():
    auth_styles()
    _, c, _ = st.columns([1, 1.5, 1])
    with c:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('<div class="title-box">CREATE ACCOUNT</div>', unsafe_allow_html=True)
        with st.form("signup"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            if st.form_submit_button("Sign Up"):
                st.session_state.user = {"name": name, "email": email, "role": "Farmer"}
                st.session_state.page = "app"; st.rerun()
        if st.button("Back"): st.session_state.page = "login"; st.rerun()

def profile_page():
    st.header("👤 Profile")
    st.write(f"Logged in as: {st.session_state.user['name']}")
    if st.button("Logout"):
        st.session_state.page = "login"
        st.session_state.user = {"name":"","email":""}
        st.rerun()
    if st.button("Back"): st.session_state.page = "app"; st.rerun()

if st.session_state.page == "login": login_page()
elif st.session_state.page == "signup": signup_page()
elif st.session_state.page == "profile": profile_page()
else: main_app()
