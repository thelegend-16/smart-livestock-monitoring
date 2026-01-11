import streamlit as st

st.set_page_config(
    page_title="Smart Livestock Management",
    page_icon="🐄",
    layout="wide"
)

# ================= SESSION STATE =================
if "page" not in st.session_state:
    st.session_state.page = "login"

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
        "welcome": "Welcome back,",
        "desc": "Track livestock health, monitor activity, and connect with veterinarians — all from one smart app.",
        "animals": "My Animals",
        "health": "Health Monitoring",
        "portal": "Farmer / Vet Portal",
        "dark": "Dark Mode",
        "profile": "Profile"
    },
    "Hindi": {
        "title": "पशुधन देखभाल ऐप",
        "subtitle": "आधुनिक किसानों के लिए स्मार्ट निगरानी",
        "welcome": "स्वागत है,",
        "desc": "पशुओं के स्वास्थ्य की निगरानी करें और पशु चिकित्सकों से जुड़ें।",
        "animals": "मेरे पशु",
        "health": "स्वास्थ्य निगरानी",
        "portal": "किसान / पशु चिकित्सक पोर्टल",
        "dark": "डार्क मोड",
        "profile": "प्रोफ़ाइल"
    }
}

# ================= AUTH STYLES (FIXED VISIBILITY) =================
def auth_styles():
    # Detect if user is likely in dark mode to set initial visibility
    st.markdown("""
    <style>
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    /* FIX: Using forced white for dark background and dynamic for light */
    .welcome-header {
        color: #4caf50;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-size: 14px;
        margin-bottom: 10px;
    }
    .main-title {
        font-size: 32px;
        font-weight: 800;
        color: white !important; /* Forced white for login visibility */
        margin-bottom: 5px;
    }
    .sub-title {
        color: #cbd5e1 !important; /* Light grey for visibility */
        margin-bottom: 30px;
        font-size: 16px;
    }
    div[data-testid="stFormSubmitButton"] > button {
        width: 100%;
        border-radius: 12px !important;
        height: 3.5em !important;
        background: linear-gradient(90deg, #2e7d32, #4caf50) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ================= LOGIN PAGE =================
def login_page():
    auth_styles()
    # Centering the login card
    _, col2, _ = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="welcome-header">Welcome to Livestock Care App</div>', unsafe_allow_html=True)
        st.markdown('<div class="main-title">Sign In</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-title">Please enter your details to continue.</div>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Email Address", placeholder="e.g., farmer@domain.com")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Access Dashboard")

        if submit:
            if email and password:
                st.session_state.user["email"] = email
                st.session_state.user["name"] = email.split("@")[0].title()
                st.session_state.page = "app"
                st.rerun()
            else:
                st.error("Missing credentials")

        if st.button("New User? Create Account"):
            st.session_state.page = "signup"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ================= SIGN UP PAGE =================
def signup_page():
    auth_styles()
    _, col2, _ = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="main-title">Join Us</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-title">Start your smart farming journey today.</div>', unsafe_allow_html=True)
        
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            role = st.selectbox("I am a...", ["Farmer", "Veterinarian"])
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Create Account")

        if submit:
            if name and email and password:
                st.session_state.user = {"name": name, "email": email, "role": role}
                st.session_state.page = "app"
                st.rerun()
            else:
                st.error("Please fill all fields")

        if st.button("Already a member? Login"):
            st.session_state.page = "login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ================= MAIN APP =================
def main_app():
    # Theme configuration
    lang_col, theme_col, prof_col = st.columns([6, 2, 2])
    with lang_col:
        language = st.selectbox("🌐", list(LANGUAGES.keys()), label_visibility="collapsed")
    lang = LANGUAGES[language]
    with theme_col:
        dark_mode = st.toggle(f"🌙 {lang['dark']}", value=False)
    with prof_col:
        if st.button(f"👤 {lang['profile']}"):
            st.session_state.page = "profile"
            st.rerun()

    # Dynamic Theme Colors (FIXED FOR VISIBILITY)
    if dark_mode:
        bg, card, text, primary = "#0e1117", "#1c2128", "#FFFFFF", "#4caf50"
    else:
        bg, card, text, primary = "#F8FAFC", "#FFFFFF", "#1E293B", "#2e7d32"

    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {text} !important; }}
    
    /* Header styling */
    .app-header {{
        background: linear-gradient(135deg, {primary}, #81c784);
        padding: 40px; border-radius: 24px;
        color: white !important; text-align: center;
        margin-bottom: 30px;
    }}
    .app-header h1, .app-header p {{ color: white !important; }}

    /* Content Card */
    .content-card {{
        background: {card}; padding: 25px; border-radius: 20px;
        margin-bottom: 25px; border: 1px solid {primary}33;
    }}
    .content-card h3, .content-card p {{ color: {text} !important; }}

    /* Nav Buttons */
    .nav-btn {{
        background: {card}; border: 2px solid {primary};
        color: {text} !important; padding: 20px;
        border-radius: 15px; text-align: center;
        font-weight: 700; font-size: 18px;
        margin-bottom: 15px; cursor: pointer;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="app-header">
      <h1>🐄 {lang['title']}</h1>
      <p>{lang['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="content-card">
      <h3>{lang['welcome']} {st.session_state.user['name']} 👋</h3>
      <p>{lang['desc']}</p>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)
    with col_a: st.markdown(f'<div class="nav-btn">🐄<br>{lang["animals"]}</div>', unsafe_allow_html=True)
    with col_b: st.markdown(f'<div class="nav-btn">❤️<br>{lang["health"]}</div>', unsafe_allow_html=True)
    with col_c: st.markdown(f'<div class="nav-btn">👨‍🌾<br>{lang["portal"]}</div>', unsafe_allow_html=True)

# ================= PROFILE PAGE =================
def profile_page():
    st.markdown("### 👤 Account Settings")
    with st.form("edit_profile"):
        name = st.text_input("Name", st.session_state.user["name"])
        email = st.text_input("Email", st.session_state.user["email"])
        role = st.selectbox("Role", ["Farmer", "Veterinarian"], index=0)
        if st.form_submit_button("Save Updates"):
            st.session_state.user.update({"name": name, "email": email, "role": role})
            st.success("Profile saved!")

    if st.button("⬅ Dashboard"):
        st.session_state.page = "app"
        st.rerun()
    if st.button("🚪 Sign Out", type="primary"):
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
