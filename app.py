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
    st.session_state.user = {"name": "", "email": "", "role": "Farmer", "details": {}}

if "attendance_logs" not in st.session_state:
    st.session_state.attendance_logs = []

if "sub_page" not in st.session_state:
    st.session_state.sub_page = "home"

if "herd_data" not in st.session_state:
    st.session_state.herd_data = pd.DataFrame(columns=["ID", "Type", "Age", "Health Status"])

# ================= STYLES =================
def apply_custom_styles(primary, bg, card, text):
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
    .auth-container {{ text-align:center; padding:20px; }}
    .title-box {{
        background:#2e7d32; color:white; padding:20px;
        border-radius:16px; font-size:28px; font-weight:bold;
        margin-bottom:10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# ================= LOGIN PAGE =================
def login_page():
    _, c, _ = st.columns([1, 1.5, 1])
    with c:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('<div class="title-box">LIVESTOCK CARE APP</div>', unsafe_allow_html=True)
        st.write("### Sign In")
        with st.form("login"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Access Portal"):
                if email:
                    st.session_state.user["email"] = email
                    st.session_state.user["name"] = email.split("@")[0].title()
                    st.session_state.page = "app"
                    st.rerun()
        if st.button("New here? Create an Account"):
            st.session_state.page = "signup"
            st.rerun()

# ================= SIGNUP PAGE =================
def signup_page():
    _, c, _ = st.columns([1, 1.5, 1])
    with c:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('<div class="title-box">JOIN THE NETWORK</div>', unsafe_allow_html=True)
        
        role = st.radio("I am a:", ["Farmer", "Veterinarian"], horizontal=True)
        
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            
            # Vet-specific fields
            vet_details = {}
            if role == "Veterinarian":
                vet_details['spec'] = st.selectbox("Specialization", ["General Surgeon", "Large Animal Specialist", "Vaccination Expert"])
                vet_details['loc'] = st.text_input("Location (City/District)")
                vet_details['phone'] = st.text_input("Phone Number")
            
            if st.form_submit_button("Create Account"):
                st.session_state.user = {
                    "name": name, 
                    "email": email, 
                    "role": role,
                    "details": vet_details
                }
                st.session_state.page = "app"
                st.rerun()
        
        if st.button("Back to Login"):
            st.session_state.page = "login"
            st.rerun()

# ================= FARMER PORTAL =================
def render_farmer_home():
    st.markdown('<div class="header"><h1>🐄 Farmer Dashboard</h1><p>Smart Livestock Management</p></div>', unsafe_allow_html=True)
    
    # Grid Layout
    _, mid, _ = st.columns([1,2,1])
    with mid:
        st.markdown('<div class="box-icon">📸</div>', unsafe_allow_html=True)
        if st.button("Camera & Upload", use_container_width=True):
            st.session_state.sub_page = "camera"; st.rerun()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="box-icon">🐄</div>', unsafe_allow_html=True)
        if st.button("My Animals", use_container_width=True):
            st.session_state.sub_page = "animals"; st.rerun()
    with c2:
        st.markdown('<div class="box-icon">❤️</div>', unsafe_allow_html=True)
        if st.button("Health Monitoring", use_container_width=True):
            st.session_state.sub_page = "health"; st.rerun()

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="box-icon">👨‍🌾</div>', unsafe_allow_html=True)
        if st.button("Find Vets", use_container_width=True):
            st.session_state.sub_page = "portal"; st.rerun()
    with c4:
        st.markdown('<div class="box-icon">📅</div>', unsafe_allow_html=True)
        if st.button("Attendance", use_container_width=True):
            st.session_state.sub_page = "attendance"; st.rerun()

# ================= VET PORTAL =================
def render_vet_home():
    st.markdown('<div class="header"><h1>👨‍⚕️ Veterinarian Portal</h1><p>Professional Health Services</p></div>', unsafe_allow_html=True)
    
    st.write(f"### Welcome, {st.session_state.user['name']}")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("Your Profile")
            st.write(f"**Specialty:** {st.session_state.user['details'].get('spec')}")
            st.write(f"**Location:** {st.session_state.user['details'].get('loc')}")
            st.write(f"**Phone:** {st.session_state.user['details'].get('phone')}")
    
    with col2:
        with st.container(border=True):
            st.subheader("Today's Appointments")
            st.info("No appointments scheduled for today.")

    st.divider()
    st.subheader("Active Cases")
    st.write("When farmers contact you, requests will appear here.")

# ================= MAIN APP ROUTER =================
def main_app():
    # Header Logic
    cl, ct, cp = st.columns([5, 2, 2])
    dark_mode = ct.toggle("🌙 Dark Mode", value=True)
    if cp.button("👤 Profile"): st.session_state.page = "profile"; st.rerun()

    primary, bg, card, text = ("#4caf50", "#0e1117", "#1c2128", "#ffffff") if dark_mode else ("#2e7d32", "#f8fafc", "#ffffff", "#1e293b")
    apply_custom_styles(primary, bg, card, text)

    # Sub-page back button
    if st.session_state.sub_page != "home":
        if st.button("⬅ Back to Dashboard"): 
            st.session_state.sub_page = "home"; st.rerun()

    # Role-Based Routing
    if st.session_state.user["role"] == "Veterinarian":
        render_vet_home()
    else:
        # Farmer Sub-pages
        if st.session_state.sub_page == "home": render_farmer_home()
        elif st.session_state.sub_page == "animals": render_animals_page()
        elif st.session_state.sub_page == "camera": render_camera_page()
        elif st.session_state.sub_page == "attendance": render_attendance_page()
        elif st.session_state.sub_page == "portal": render_vet_portal_page()
        elif st.session_state.sub_page == "health": render_health_page()

# ================= HELPER PAGES =================
def render_camera_page():
    st.header("📸 Camera & Upload")
    img = st.camera_input("Capture Animal")
    if img: st.image(img)

def render_attendance_page():
    st.header("📅 Attendance")
    if st.button("Mark Present Today"):
        st.session_state.attendance_logs.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    st.table(pd.DataFrame(st.session_state.attendance_logs, columns=["Timestamp"]))

def render_animals_page():
    st.header("🐄 My Animals")
    with st.form("add"):
        aid = st.text_input("Tag ID")
        if st.form_submit_button("Add"):
            st.session_state.herd_data.loc[len(st.session_state.herd_data)] = [aid, "Cow", 2, "Healthy"]
    st.dataframe(st.session_state.herd_data)

def render_vet_portal_page():
    st.header("👨‍⚕️ Available Veterinarians")
    st.write("Searching for specialists in your area...")
    st.container(border=True).write("**Dr. Smith** - Large Animal Specialist (Located 2km away)")

def render_health_page():
    st.header("❤️ Health Monitoring")
    st.metric("Avg Herd Heart Rate", "75 BPM")

def profile_page():
    st.header("👤 Profile")
    st.write(st.session_state.user)
    if st.button("Logout"):
        st.session_state.page = "login"
        st.rerun()
    if st.button("Back"):
        st.session_state.page = "app"
        st.rerun()

# ================= ROUTER =================
if st.session_state.page == "login": login_page()
elif st.session_state.page == "signup": signup_page()
elif st.session_state.page == "profile": profile_page()
else: main_app()
