import streamlit as st

st.set_page_config(
    page_title="Smart Livestock Management",
    page_icon="🐄",
    layout="wide"
)

# ================= SESSION STATE =================
if "page" not in st.session_state:
    st.session_state.page = "login"   # login | signup | app | profile

if "user" not in st.session_state:
    st.session_state.user = {
        "name": "",
        "email": "",
        "role": "Farmer"
    }

# ================= LANGUAGE DATA =================
LANGUAGES = {
    "English": {
        "title": "Livestock Care App",
        "subtitle": "Smart monitoring for modern farmers",
        "welcome": "Welcome 👋",
        "desc": "Track livestock health, monitor activity, and connect with veterinarians — all from one smart app.",
        "animals": "Animals",
        "health": "Health Monitoring",
        "portal": "Farmer / Vet Portal",
        "dark": "Dark Mode",
        "profile": "Profile"
    }
}

# ================= LOGIN / SIGNUP STYLES =================
def auth_styles():
    st.markdown("""
    <style>
    .auth-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
    }

    .auth-card {
        width: 440px;
        background: white;
        padding: 36px;
        border-radius: 22px;
        box-shadow: 0px 25px 60px rgba(0,0,0,0.18);
    }

    .auth-brand {
        text-align: center;
        margin-bottom: 22px;
    }

    .auth-brand h1 {
        font-size: 26px;
        margin-bottom: 4px;
        color: #1b5e20;
    }

    .auth-brand p {
        color: #6b7280;
        font-size: 14px;
    }

    .auth-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 6px;
        color: #111827;
    }

    .auth-subtitle {
        color: #6b7280;
        margin-bottom: 24px;
    }

    .auth-footer {
        text-align: center;
        margin-top: 18px;
        font-size: 14px;
    }

    .auth-footer button {
        background: none;
        border: none;
        color: #2e7d32;
        font-weight: 600;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

# ================= LOGIN PAGE =================
def login_page():
    auth_styles()

    st.markdown("""
    <div class="auth-wrapper">
      <div class="auth-card">

        <div class="auth-brand">
            <h1>🐄 Livestock Care App</h1>
            <p>Smart Livestock Management Platform</p>
        </div>

        <div class="auth-title">Welcome Back</div>
        <div class="auth-subtitle">
            Welcome to Livestock Care App. Please sign in to continue.
        </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign In")

    if submit:
        if email and password:
            st.session_state.user["email"] = email
            st.session_state.user["name"] = email.split("@")[0].title()
            st.session_state.page = "app"
            st.rerun()
        else:
            st.error("Please enter email and password")

    st.markdown("""
        <div class="auth-footer">
            Don’t have an account?
        </div>
    """, unsafe_allow_html=True)

    if st.button("Create Account"):
        st.session_state.page = "signup"
        st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)

# ================= SIGN UP PAGE (UNCHANGED) =================
def signup_page():
    auth_styles()

    st.markdown("""
    <div class="auth-wrapper">
      <div class="auth-card">

        <div class="auth-brand">
            <h1>🐄 Livestock Care App</h1>
            <p>Create your account</p>
        </div>

        <div class="auth-title">Create Account</div>
        <div class="auth-subtitle">
            Start managing your livestock smarter
        </div>
    """, unsafe_allow_html=True)

    with st.form("signup_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        role = st.selectbox("Role", ["Farmer", "Veterinarian"])
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign Up")

    if submit:
        if name and email and password:
            st.session_state.user = {
                "name": name,
                "email": email,
                "role": role
            }
            st.session_state.page = "app"
            st.rerun()
        else:
            st.error("Fill all details")

    if st.button("Already have an account? Login"):
        st.session_state.page = "login"
        st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)

# ================= MAIN APP (UNCHANGED) =================
def main_app():
    col1, col2, col3 = st.columns([6, 2, 2])

    with col3:
        language = st.selectbox("🌐 Language", list(LANGUAGES.keys()))

    lang = LANGUAGES[language]

    with col2:
        dark_mode = st.toggle(f"🌙 {lang['dark']}", value=False)

    with col1:
        if st.button("👤 Profile"):
            st.session_state.page = "profile"
            st.rerun()

    if dark_mode:
        bg = "#0e1117"; card = "#161b22"; text = "#ffffff"; primary = "#2ea043"
    else:
        bg = "#f4f6f8"; card = "#ffffff"; text = "#000000"; primary = "#2e7d32"

    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {text}; }}
    .header {{
        background: linear-gradient(90deg, {primary}, #4caf50);
        padding: 26px;
        border-radius: 18px;
        color: white;
        text-align: center;
        margin-bottom: 28px;
    }}
    .card {{
        background: {card};
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.15);
        margin-bottom: 18px;
    }}
    .btn {{
        background: linear-gradient(90deg, {primary}, #4caf50);
        color: white;
        padding: 16px;
        border-radius: 14px;
        text-align: center;
        font-size: 17px;
        font-weight: 600;
        margin-bottom: 14px;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="header">
      <h1>🐄 {lang['title']}</h1>
      <p>{lang['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
      <h3>{lang['welcome']} {st.session_state.user['name']}</h3>
      <p>{lang['desc']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="btn">🐄 {lang['animals']}</div>
    <div class="btn">❤️ {lang['health']}</div>
    <div class="btn">👨‍🌾 {lang['portal']}</div>
    """, unsafe_allow_html=True)

# ================= PROFILE PAGE (UNCHANGED) =================
def profile_page():
    st.subheader("👤 User Profile")

    with st.form("edit_profile"):
        name = st.text_input("Name", st.session_state.user["name"])
        email = st.text_input("Email", st.session_state.user["email"])
        role = st.selectbox("Role", ["Farmer", "Veterinarian"])
        save = st.form_submit_button("Save Changes")

    if save:
        st.session_state.user.update({
            "name": name,
            "email": email,
            "role": role
        })
        st.success("Profile updated")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            st.session_state.page = "app"
            st.rerun()
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.page = "login"
            st.session_state.user = {"name": "", "email": "", "role": "Farmer"}
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
