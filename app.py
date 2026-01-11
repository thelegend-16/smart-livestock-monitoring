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
    /* Login Interface Styles (Kept Exactly Same) */
    .auth-container {{ text-align:center; padding:40px; }}
    .title-box {{
        background:#2e7d32; color:white; padding:20px;
        border-radius:16px; font-size:28px; font-weight:bold;
        margin-bottom:10px;
    }}
    .welcome-subtext {{
        color:#4caf50; font-size:18px; font-weight:600;
        margin-bottom:25px;
    }}
    </style>
    """, unsafe_allow_html=True)

# ================= LOGIN PAGE (SAME AS BEFORE) =================
def login_page():
    # Use default green for auth pages
    apply_custom_styles("#2e7d32", "#0e1117", "#1c2128", "#ffffff")
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

# ================= SIGNUP PAGE (UPDATED WITH ROLE SELECTION) =================
def signup_page():
    apply_custom_styles("#2e7d32", "#0e1117", "#1c2128", "#ffffff")
    _, c, _ = st.columns([1, 1.5, 1])
    with c:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('<div class="title-box">CREATE ACCOUNT</div>', unsafe_allow_html=True)
        
        # Role selection before the form
        role = st.radio("Select Role:", ["Farmer", "Veterinarian"], horizontal=True)
        
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            vet_details = {}
            if role == "Veterinarian":
                st.write("---")
                st.subheader("Vet Professional Details")
                vet_details['spec'] = st.selectbox("Specialization", ["General Surgeon", "Large Animal Specialist", "Vaccination Expert"])
                vet_details['loc'] = st.text_input("Your Location")
                vet_details['phone'] = st.text_input("Phone Number")
            
            if st.form_submit_button("Sign Up"):
                if name and email:
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
        st.markdown("</div>", unsafe_allow_html=True)

# ================= MAIN APP ROUTER =================
def main_app():
    cl, ct, cp = st.columns([5, 2, 2])
    dark_mode = ct.toggle("🌙 Dark Mode", value=True)
    if cp.button("👤 Profile"): st.session_state.page = "profile"; st.rerun()

    primary, bg, card, text = ("#4caf50", "#0e1117", "#1c2128", "#ffffff") if dark_mode else ("#2e7d32", "#f8fafc", "#ffffff", "#1e293b")
    apply_custom_styles(primary, bg, card, text)

    # Role-Based Rendering
    if st.session_state.user["role"] == "Veterinarian":
        render_vet_portal()
    else:
        render_farmer_portal()

# ================= FARMER PORTAL =================
def render_farmer_portal():
    if st.session_state.sub_page != "home":
        if st.button("⬅ Back to Dashboard"): 
            st.session_state.sub_page = "home"; st.rerun()

    if st.session_state.sub_page == "home":
        st.markdown('<div class="header"><h1>🐄 Farmer Dashboard</h1><p>Smart Livestock Management</p></div>', unsafe_allow_html=True)
        st.markdown(f"### Welcome back, {st.session_state.user['name']} 👋")
        
        # Camera top center
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

    elif st.session_state.sub_page == "camera":
        st.header("📸 Camera & Upload")
        img = st.camera_input("Capture Animal")
        if img: st.image(img)
    elif st.session_state.sub_page == "animals":
        st.header("🐄 My Animals")
        st.dataframe(st.session_state.herd_data)
    elif st.session_state.sub_page == "portal":
        st.header("👨‍⚕️ Search Nearby Vets")
        st.info("Looking for professional help in your location...")
    elif st.session_state.sub_page == "attendance":
        st.header("📅 Attendance Log")
        if st.button("Mark Present"):
             st.session_state.attendance_logs.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        st.table(st.session_state.attendance_logs)

# ================= VET PORTAL =================
def render_vet_portal():
    st.markdown('<div class="header"><h1>👨‍⚕️ Veterinarian Portal</h1><p>Professional Dashboard</p></div>', unsafe_allow_html=True)
    st.write(f"### Welcome, Dr. {st.session_state.user['name']}")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("Your Profile Card")
            st.write(f"**Specialization:** {st.session_state.user['details'].get('spec')}")
            st.write(f"**Location:** {st.session_state.user['details'].get('loc')}")
            st.write(f"**Emergency Phone:** {st.session_state.user['details'].get('phone')}")
            st.button("Edit Profile")
    
    with col2:
        with st.container(border=True):
            st.subheader("Upcoming Appointments")
            st.info("No bookings yet. Farmers will contact you via your location.")

    st.divider()
    st.subheader("Recent Patient Consultations")
    st.write("You haven't treated any animals yet.")

# ================= PROFILE PAGE =================
def profile_page():
    st.header("👤 Account Profile")
    st.write(st.session_state.user)
    if st.button("Logout", type="primary"):
        st.session_state.page = "login"
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
