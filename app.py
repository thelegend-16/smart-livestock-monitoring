import streamlit as st

st.set_page_config(
    page_title="Livestock Care App",
    page_icon="🐄",
    layout="wide"
)

# ================= SESSION STATE =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None

# ================= LOGIN PAGE =================
def login_page():
    st.markdown("""
    <style>
    .login-box {
        max-width: 400px;
        margin: auto;
        background: white;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.2);
        margin-top: 100px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-box">
        <h2 style="text-align:center;">🐄 Livestock Care App</h2>
        <p style="text-align:center;">Login to continue</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        role = st.selectbox("Login as", ["Farmer", "Veterinarian", "Admin"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if username and password:
            st.session_state.logged_in = True
            st.session_state.user_role = role
            st.experimental_rerun()
        else:
            st.error("Please enter username and password")

# ================= MAIN APP =================
def main_app():

    # ---------- LANGUAGE DATA ----------
    LANGUAGES = {
        "English": {
            "title": "Livestock Care App",
            "subtitle": "Smart monitoring for modern farmers",
            "welcome": "Welcome 👋",
            "desc": "Track livestock health, monitor activity, and connect with veterinarians — all from a single smart app designed for farmers.",
            "animals": "Animals",
            "health": "Health Monitoring",
            "portal": "Farmer / Vet Portal",
            "controls": "App Controls",
            "settings": "App Settings",
            "dark": "Dark Mode"
        },
        "Hindi": {
            "title": "पशुधन देखभाल ऐप",
            "subtitle": "आधुनिक किसानों के लिए स्मार्ट निगरानी",
            "welcome": "स्वागत है 👋",
            "desc": "पशुओं के स्वास्थ्य की निगरानी करें और पशु चिकित्सकों से जुड़ें।",
            "animals": "पशु",
            "health": "स्वास्थ्य निगरानी",
            "portal": "किसान / पशु चिकित्सक पोर्टल",
            "controls": "ऐप नियंत्रण",
            "settings": "ऐप सेटिंग्स",
            "dark": "डार्क मोड"
        }
    }

    # ---------- TOP CONTROLS ----------
    st.markdown("### ⚙️ App Controls")

    col1, col2, col3 = st.columns([6, 2, 2])

    with col3:
        language = st.selectbox("🌐 Language", list(LANGUAGES.keys()))

    lang = LANGUAGES[language]

    with col2:
        dark_mode = st.toggle(f"🌙 {lang['dark']}", value=False)

    with col1:
        with st.expander(f"⚙️ {lang['settings']}"):
            st.write(f"Logged in as: **{st.session_state.user_role}**")
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.experimental_rerun()

    # ---------- THEME COLORS ----------
    if dark_mode:
        bg = "#0e1117"
        card = "#161b22"
        text = "#ffffff"
        subtext = "#c9d1d9"
        primary = "#2ea043"
    else:
        bg = "#f4f6f8"
        card = "#ffffff"
        text = "#000000"
        subtext = "#555555"
        primary = "#2e7d32"

    # ---------- STYLES ----------
    st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg};
        color: {text};
    }}

    .app-header {{
        background: linear-gradient(90deg, {primary}, #4caf50);
        padding: 26px;
        border-radius: 18px;
        color: white;
        text-align: center;
        margin-bottom: 28px;
    }}

    .card {{
        background-color: {card};
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.15);
        margin-bottom: 18px;
    }}

    .app-btn {{
        background: linear-gradient(90deg, {primary}, #4caf50);
        color: white;
        padding: 16px;
        border-radius: 14px;
        text-align: center;
        font-size: 17px;
        font-weight: 600;
        margin-bottom: 14px;
    }}

    [data-testid="stToggle"] label div {{
        color: {text} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # ---------- HEADER ----------
    st.markdown(f"""
    <div class="app-header">
        <h1>🐄 {lang['title']}</h1>
        <p>{lang['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------- HOME ----------
    st.markdown(f"""
    <div class="card">
        <h3>{lang['welcome']}</h3>
        <p>{lang['desc']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="app-btn">🐄 {lang['animals']}</div>
    <div class="app-btn">❤️ {lang['health']}</div>
    <div class="app-btn">👨‍🌾 {lang['portal']}</div>
    """, unsafe_allow_html=True)


# ================= APP ROUTER =================
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
