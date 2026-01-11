import streamlit as st

st.set_page_config(
    page_title="Smart Livestock Management",
    page_icon="🐄",
    layout="wide"
)

# ================= SESSION STATE =================
if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"  # login | signup | app

if "user_email" not in st.session_state:
    st.session_state.user_email = None


# ================= LANGUAGE DATA =================
LANGUAGES = {
    "English": {
        "title": "Livestock Care App",
        "subtitle": "Smart monitoring for modern farmers",
        "welcome": "Welcome 👋",
        "desc": "Track livestock health, monitor activity, and connect with veterinarians — all from a single smart app designed for farmers.",
        "animals": "Animals",
        "health": "Health Monitoring",
        "portal": "Farmer / Vet Portal",
        "dark": "Dark Mode",
        "controls": "App Controls",
        "settings": "App Settings",
        "profile": "Profile"
    },
    "Hindi": {
        "title": "पशुधन देखभाल ऐप",
        "subtitle": "आधुनिक किसानों के लिए स्मार्ट निगरानी",
        "welcome": "स्वागत है 👋",
        "desc": "पशुओं के स्वास्थ्य की निगरानी करें और पशु चिकित्सकों से जुड़ें।",
        "animals": "पशु",
        "health": "स्वास्थ्य निगरानी",
        "portal": "किसान / पशु चिकित्सक पोर्टल",
        "dark": "डार्क मोड",
        "controls": "ऐप नियंत्रण",
        "settings": "ऐप सेटिंग्स",
        "profile": "प्रोफ़ाइल"
    }
}


# ================= AUTH STYLES =================
def auth_styles():
    st.markdown("""
    <style>
    .auth-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 90vh;
        background-color: #f9faf7;
    }

    .auth-card {
        width: 420px;
        background: #ffffff;
        padding: 35px;
        border-radius: 18px;
        box-shadow: 0px 15px 40px rgba(0,0,0,0.12);
    }

    .auth-header {
        background: #2e7d32;
        color: white;
        text-align: center;
        padding: 18px;
        border-radius: 14px;
        margin-bottom: 25px;
        font-size: 18px;
        font-weight: 600;
    }

    .auth-title {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 5px;
        color: #1f2937;
    }

    .auth-subtitle {
        color: #6b7280;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)


# ================= LOGIN PAGE =================
def login_page():
    auth_styles()

    st.markdown("""
    <div class="auth-wrapper">
        <div class="auth-card">
            <div class="auth-header">Smart Livestock Management</div>
            <div class="auth-title">Welcome Back</div>
            <div class="auth-subtitle">Sign in to access your farm dashboard</div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign In")

    if submit:
        if email and password:
            st.session_state.user_email = email
            st.session_state.auth_page = "app"
            st.rerun()
        else:
            st.error("Please enter email and password")

    if st.button("Don't have an account? Sign up"):
        st.session_state.auth_page = "signup"
        st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)


# ================= SIGN UP PAGE =================
def signup_page():
    auth_styles()

    st.markdown("""
    <div class="auth-wrapper">
        <div class="auth-card">
            <div class="auth-header">Smart Livestock Management</div>
            <div class="auth-title">Create Account</div>
            <div class="auth-subtitle">Sign up to start managing your livestock</div>
    """, unsafe_allow_html=True)

    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up")

    if submit:
        if email and password and password == confirm:
            st.session_state.user_email = email
            st.session_state.auth_page = "app"
            st.rerun()
        else:
            st.error("Please check your inputs")

    if st.button("Already have an account? Sign In"):
        st.session_state.auth_page = "login"
        st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)


# ================= MAIN APP =================
def main_app():

    # ---------- TOP CONTROLS ----------
    st.markdown("### ⚙️ App Controls")
    col1, col2, col3 = st.columns([6, 2, 2])

    with col3:
        selected_language = st.selectbox("🌐 Language", list(LANGUAGES.keys()))

    lang = LANGUAGES[selected_language]

    with col2:
        dark_mode = st.toggle(f"🌙 {lang['dark']}", value=False)

    with col1:
        with st.expander(f"⚙️ {lang['settings']}"):
            st.write(f"Logged in as: **{st.session_state.user_email}**")
            if st.button("Logout"):
                st.session_state.auth_page = "login"
                st.session_state.user_email = None
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
if st.session_state.auth_page == "login":
    login_page()
elif st.session_state.auth_page == "signup":
    signup_page()
else:
    main_app()
