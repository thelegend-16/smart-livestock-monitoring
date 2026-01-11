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
        "profile": "प्रोफ़ाइल"
    }
}

# ================= COMMON AUTH STYLES =================
def auth_styles():
    st.markdown("""
    <style>
    /* Global Background */
    .stApp {
        background: #f8fafc;
    }

    /* Modern Card Styling */
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .login-box {
        background: white;
        padding: 40px;
        border-radius: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        width: 100%;
    }

    .welcome-text {
        color: #2e7d32;
        font-weight: 700;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 13px;
    }

    .main-title {
        font-size: 32px;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 8px;
    }

    .sub-title {
        color: #64748b;
        margin-bottom: 25px;
        font-size: 15px;
    }

    /* Styling the Form Submit Button */
    div[data-testid="stFormSubmitButton"] > button {
        width: 100%;
        border-radius: 10px !important;
        height: 3.5em !important;
        background: linear-gradient(90deg, #2e7d32, #4caf50) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.2);
    }
    
    /* "Create account" link button styling */
    div.stButton > button {
        background-color: transparent;
        color: #2e7d32;
        border: 1px solid #2e7d32;
        width: 100%;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ================= LOGIN PAGE =================
def login_page():
    auth_styles()

    # Center the login box
    _, col2, _ = st.columns([1, 1.5, 1])

    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Header text outside the form for better styling
        st.markdown("""
            <div class="welcome-text">Welcome to Livestock Care App</div>
            <div class="main-title">Sign In</div>
            <div class="sub-title">Enter your credentials to access your dashboard.</div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("Email Address", placeholder="farmer@example.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            st.checkbox("Remember me", value=True)
            submit = st.form_submit_button("Access Dashboard")

        if submit:
            if email and password:
                st.session_state.user["email"] = email
                st.session_state.user["name"] = email.split("@")[0].title()
                st.session_state.page = "app"
                st.rerun()
            else:
                st.error("Please enter email and password")

        st.markdown("<div style='margin-top: 20px; text-align: center; width: 100%;'>", unsafe_allow_html=True)
        if st.button("New here? Create an account"):
            st.session_state.page = "signup"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ================= SIGN UP PAGE =================
def signup_page():
    auth_styles()

    _, col2, _ = st.columns([1, 1.5, 1])

    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("""
            <div class="welcome-text">Join us today</div>
            <div class="main-title">Create Account</div>
            <div class="sub-title">Start managing your livestock smarter.</div>
        """, unsafe_allow_html=True)

        with st.form("signup_form"):
            name = st.text_input("Full Name", placeholder="John Doe")
            email = st.text_input("Email", placeholder="john@example.com")
            role = st.selectbox("Role", ["Farmer", "Veterinarian"])
            password = st.text_input("Password", type="password", placeholder="••••••••")
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
                st.error("Please fill all details")

        if st.button("Already have an account? Login"):
            st.session_state.page = "login"
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# ================= MAIN APP =================
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
        padding: 26px; border-radius: 18px;
        color: white; text-align: center; margin-bottom: 28px;
    }}
    .card {{
        background: {card}; padding: 22px; border-radius: 16px;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.15);
        margin-bottom: 18px;
    }}
    .btn-custom {{
        background: linear-gradient(90deg, {primary}, #4caf50);
        color: white; padding: 16px;
        border-radius: 14px; text-align: center;
        font-size: 17px; font-weight: 600;
        margin-bottom: 14px;
        cursor: pointer;
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
      <h3 style="color: {primary if not dark_mode else '#4caf50'};">{lang['welcome']} {st.session_state.user['name']}</h3>
      <p>{lang['desc']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="btn-custom">🐄 {lang['animals']}</div>
    <div class="btn-custom">❤️ {lang['health']}</div>
    <div class="btn-custom">👨‍🌾 {lang['portal']}</div>
    """, unsafe_allow_html=True)

# ================= PROFILE PAGE =================
def profile_page():
    st.subheader("👤 User Profile")

    with st.form("edit_profile"):
        name = st.text_input("Name", st.session_state.user["name"])
        email = st.text_input("Email", st.session_state.user["email"])
        role = st.selectbox("Role", ["Farmer", "Veterinarian"], index=0)
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
