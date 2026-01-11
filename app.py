import streamlit as st
from datetime import datetime
import pandas as pd

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

# Sub-routing for the dashboard
if "sub_page" not in st.session_state:
    st.session_state.sub_page = "home"

if "herd_data" not in st.session_state:
    st.session_state.herd_data = pd.DataFrame(columns=["ID", "Type", "Age", "Health Status"])

# ================= LANGUAGE DATA =================
LANGUAGES = {
    "English": {
        "title": "Livestock Care App",
        "subtitle": "Smart monitoring for modern farmers",
        "welcome": "Welcome,",
        "desc": "Track livestock health and manage your farm operations.",
        "animals": "My Animals",
        "health": "Health Monitoring",
        "portal": "Farmer / Vet Portal",
        "dark": "Dark Mode",
        "profile": "Profile",
        "attendance": "Attendance"
    },
    "Hindi": {
        "title": "पशुधन देखभाल ऐप",
        "subtitle": "आधुनिक किसानों के लिए स्मार्ट निगरानी",
        "welcome": "स्वागत है,",
        "desc": "पशुओं के स्वास्थ्य की निगरानी करें और अपने फार्म का प्रबंधन करें।",
        "animals": "मेरे पशु",
        "health": "स्वास्थ्य निगरानी",
        "portal": "किसान / पशु चिकित्सक पोर्टल",
        "dark": "डार्क मोड",
        "profile": "प्रोफ़ाइल",
        "attendance": "उपस्थिति"
    }
}

# ================= AUTH STYLES =================
def auth_styles():
    st.markdown("""
    <style>
    .auth-container { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px; }
    .title-box {
        background-color: #2e7d32; color: white; padding: 20px 40px;
        border-radius: 15px; font-size: 28px; font-weight: bold;
        text-align: center; margin-bottom: 10px; width: 100%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .welcome-subtext { color: #4caf50; font-size: 18px; font-weight: 600; text-transform: uppercase; margin-bottom: 30px; }
    .login-label { color: white !important; font-size: 24px; font-weight: bold; margin-bottom: 20px; }
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.05); padding: 20px;
        border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# ================= PAGES =================

def login_page():
    auth_styles()
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('<div class="title-box">LIVESTOCK CARE APP</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-subtext">Welcome</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-label">Sign In</div>', unsafe_allow_html=True)
        with st.form("login_form"):
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Access Dashboard")
        if submit and email and password:
            st.session_state.user["email"] = email
            st.session_state.user["name"] = email.split("@")[0].title()
            st.session_state.page = "app"; st.rerun()
        if st.button("Create an Account"):
            st.session_state.page = "signup"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def main_app():
    # Header logic
    col_l, col_t, col_p = st.columns([5, 2, 2])
    with col_l: language = st.selectbox("🌐 Language", list(LANGUAGES.keys()))
    lang = LANGUAGES[language]
    with col_t: dark_mode = st.toggle(f"🌙 {lang['dark']}", value=True)
    with col_p: 
        if st.button(f"👤 {lang['profile']}"): st.session_state.page = "profile"; st.rerun()

    bg, card, text, primary = ("#0e1117", "#1c2128", "#FFFFFF", "#4caf50") if dark_mode else ("#F8FAFC", "#FFFFFF", "#1E293B", "#2e7d32")

    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {text} !important; }}
    .main-header {{ background: linear-gradient(135deg, {primary}, #81c784); padding: 30px; border-radius: 20px; color: white; text-align: center; margin-bottom: 25px; }}
    h1, h2, h3, p {{ color: {text} !important; }}
    .main-header h1, .main-header p {{ color: white !important; }}
    </style>
    """, unsafe_allow_html=True)

    # Sidebar Navigation or Home Button
    if st.session_state.sub_page != "home":
        if st.button("⬅ Back to Dashboard"): 
            st.session_state.sub_page = "home"; st.rerun()

    # --- SUB-PAGE ROUTING ---
    if st.session_state.sub_page == "home":
        render_home(lang, primary, card)
    elif st.session_state.sub_page == "animals":
        render_animals(lang)
    elif st.session_state.sub_page == "health":
        render_health(lang)
    elif st.session_state.sub_page == "portal":
        render_vet_portal(lang)

def render_home(lang, primary, card):
    st.markdown(f'<div class="main-header"><h1>🐄 {lang["title"]}</h1><p>{lang["subtitle"]}</p></div>', unsafe_allow_html=True)
    
    # Attendance
    st.subheader(f"📅 {lang['attendance']}")
    c1, c2 = st.columns([1, 2])
    with c1:
        if st.button("✅ Mark Attendance", use_container_width=True):
            st.session_state.attendance_logs.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            st.success("Attendance Marked!")
    with c2:
        with st.expander("View History"):
            for log in st.session_state.attendance_logs[:5]: st.write(f"📍 Present: {log}")

    st.divider()
    
    # Feature Buttons (Making them work)
    fa, fb, fc = st.columns(3)
    with fa:
        st.markdown(f'<div style="text-align:center; padding:20px; border:2px solid {primary}; border-radius:15px;">🐄<br><b>{lang["animals"]}</b></div>', unsafe_allow_html=True)
        if st.button("Manage Herd", use_container_width=True): 
            st.session_state.sub_page = "animals"; st.rerun()
    with fb:
        st.markdown(f'<div style="text-align:center; padding:20px; border:2px solid {primary}; border-radius:15px;">❤️<br><b>{lang["health"]}</b></div>', unsafe_allow_html=True)
        if st.button("Check Vitals", use_container_width=True): 
            st.session_state.sub_page = "health"; st.rerun()
    with fc:
        st.markdown(f'<div style="text-align:center; padding:20px; border:2px solid {primary}; border-radius:15px;">👨‍🌾<br><b>{lang["portal"]}</b></div>', unsafe_allow_html=True)
        if st.button("Find Vets", use_container_width=True): 
            st.session_state.sub_page = "portal"; st.rerun()

def render_animals(lang):
    st.header(f"🐄 {lang['animals']}")
    with st.expander("➕ Add New Animal"):
        with st.form("animal_form"):
            a_id = st.text_input("Tag ID")
            a_type = st.selectbox("Type", ["Cow", "Buffalo", "Goat", "Sheep"])
            a_age = st.number_input("Age (Years)", min_value=0)
            if st.form_submit_button("Register Animal"):
                new_data = pd.DataFrame([{"ID": a_id, "Type": a_type, "Age": a_age, "Health Status": "Healthy"}])
                st.session_state.herd_data = pd.concat([st.session_state.herd_data, new_data], ignore_index=True)
                st.success("Animal Registered!")
    st.dataframe(st.session_state.herd_data, use_container_width=True)

def render_health(lang):
    st.header(f"❤️ {lang['health']}")
    st.info("Live Monitoring coming soon with IoT sensors.")
    st.metric("Average Herd Temp", "38.5 °C", "Stable")
    st.metric("Activity Level", "High", "+5%")

def render_vet_portal(lang):
    st.header(f"👨‍⚕️ {lang['portal']}")
    st.subheader("Nearby Veterinarians")
    
    # Mock Data for nearby vets
    vets = [
        {"Name": "Dr. Sharma", "Specialty": "Large Animals", "Distance": "2.5 km", "Contact": "+91 98765 43210"},
        {"Name": "Dr. Verma", "Specialty": "Vaccinations", "Distance": "4.1 km", "Contact": "+91 87654 32109"},
        {"Name": "Dr. Singh", "Specialty": "General Physician", "Distance": "5.8 km", "Contact": "+91 76543 21098"}
    ]
    
    for v in vets:
        with st.container(border=True):
            v_col1, v_col2 = st.columns([3, 1])
            with v_col1:
                st.markdown(f"**{v['Name']}** ({v['Specialty']})")
                st.caption(f"📍 {v['Distance']} away")
            with v_col2:
                if st.button(f"📞 Call", key=v['Name']):
                    st.success(f"Connecting to {v['Contact']}...")

# ================= SIGNUP & PROFILE =================
def signup_page():
    auth_styles()
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="auth-container"><div class="title-box">CREATE ACCOUNT</div>', unsafe_allow_html=True)
        with st.form("signup"):
            name = st.text_input("Full Name"); email = st.text_input("Email"); password = st.text_input("Password", type="password")
            if st.form_submit_button("Sign Up"):
                st.session_state.user = {"name": name, "email": email, "role": "Farmer"}; st.session_state.page = "app"; st.rerun()
        if st.button("Back"): st.session_state.page = "login"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def profile_page():
    st.header("👤 Profile Settings")
    st.write(f"**User:** {st.session_state.user['name']}")
    if st.button("Logout"): st.session_state.page = "login"; st.session_state.user = {"name":"","email":""}; st.rerun()
    if st.button("Back"): st.session_state.page = "app"; st.rerun()

# ================= ROUTER =================
if st.session_state.page == "login": login_page()
elif st.session_state.page == "signup": signup_page()
elif st.session_state.page == "profile": profile_page()
else: main_app()
