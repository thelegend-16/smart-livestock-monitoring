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
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 85vh;
    }

    .login-card {
        width: 380px;
        background: #161b22;
        padding: 30px;
        border-radius: 18px;
        box-shadow: 0px 15px 40px rgba(0,0,0,0.5);
        color: white;
    }

    .login-card h2 {
        text-align: center;
        margin-bottom: 5px;
    }

    .login-card p {
        text-align: center;
        color: #9ba3af;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-wrapper">
        <div class="login-card">
            <h2>🐄 Livestock Care App</h2>
            <p>Login to continue</p>
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
            st.rerun()
        else:
            st.error("Please enter username and password")

    st.markdown("</div></div>", unsafe_allow_html=True)


# ================= MAIN APP =================
def main_app():

    LANGUAGES = {
        "English": {
            "title": "Livestock Care App",
            "subtitle": "Smart monitoring for modern farmers",
            "welcome": "Welcome 👋",
            "desc": "Track livestock health, monitor activity, and connect with veterinarians — all from a single smart app designed for farmers.",
            "animals": "Animals",
            "health": "Health Monitoring",
            "portal": "Farmer / Vet Portal",
            "dark": "Dark Mode"
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
        with st.expander("⚙️ App Settings"):
            st.write(f"Logged in as: **{st.session_state.user_role}**")
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.rerun()

    # ---------- THEME ----------
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


# ================= ROUTER =================
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
