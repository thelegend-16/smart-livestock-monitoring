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
    st.session_state.user = {
        "name": "User", 
        "email": "", 
        "role": "Farmer", 
        "phone": "+91 00000 00000",
        "location": "Farm Location",
        "details": {}
    }

if "attendance_logs" not in st.session_state:
    st.session_state.attendance_logs = []

if "sub_page" not in st.session_state:
    st.session_state.sub_page = "home"

if "herd_data" not in st.session_state:
    st.session_state.herd_data = pd.DataFrame(columns=[
        "Name", "Tag Number", "Species", "Gender", "Breed", "DOB", "Weight", "Status"
    ])

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
    /* Original Login/Auth Styles */
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

# ================= AUTH PAGES (KEPT SAME) =================
def login_page():
    apply_custom_styles("#2e7d32", "#0e1117", "#1c2128", "#ffffff")
    _, c, _ = st.columns([1, 1.5, 1])
    with c:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('<div class="title-box">LIVESTOCK CARE APP</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-subtext">WELCOME TO LIVESTOCK CARE APP</div>', unsafe_allow_html=True)
        st.subheader("Sign In")
        st.write("Please enter your details to continue.")
        with st.form("login"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Access Dashboard"):
                if email:
                    st.session_state.user["email"] = email
                    st.session_state.user["name"] = email.split("@")[0].title()
                    st.session_state.page = "app"; st.rerun()
        if st.button("Create an Account"):
            st.session_state.page = "signup"; st.rerun()

def signup_page():
    apply_custom_styles("#2e7d32", "#0e1117", "#1c2128", "#ffffff")
    _, c, _ = st.columns([1, 1.5, 1])
    with c:
        st.markdown('<div class="auth-container"><div class="title-box">CREATE ACCOUNT</div>', unsafe_allow_html=True)
        role = st.radio("I am a:", ["Farmer", "Veterinarian"], horizontal=True)
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            # Extra fields if Vet
            vet_details = {}
            if role == "Veterinarian":
                vet_details['spec'] = st.selectbox("Specialty", ["General Surgeon", "Large Animal Specialist"])
                vet_details['loc'] = st.text_input("Location")
                vet_details['phone'] = st.text_input("Phone")
            
            if st.form_submit_button("Sign Up"):
                st.session_state.user.update({"name": name, "email": email, "role": role, "details": vet_details})
                st.session_state.page = "app"; st.rerun()
        if st.button("Back to Login"):
            st.session_state.page = "login"; st.rerun()

# ================= ENHANCED PROFILE =================
def profile_page():
    apply_custom_styles("#4caf50", "#0e1117", "#1c2128", "#ffffff")
    st.markdown('<div class="header"><h1>👤 User Profile</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.info(f"**Role:** {st.session_state.user['role']}")
        if st.button("Logout", type="primary", use_container_width=True):
            st.session_state.page = "login"; st.rerun()
        if st.button("⬅ Back to Home", use_container_width=True):
            st.session_state.page = "app"; st.rerun()

    with col2:
        with st.form("edit_profile"):
            st.subheader("Edit Profile Details")
            u_name = st.text_input("Name", st.session_state.user["name"])
            u_phone = st.text_input("Phone", st.session_state.user["phone"])
            u_loc = st.text_input("Location", st.session_state.user["location"])
            
            if st.form_submit_button("Update Profile"):
                st.session_state.user.update({"name": u_name, "phone": u_phone, "location": u_loc})
                st.success("Changes saved!")
                st.rerun()

# ================= MY ANIMALS (NEW IMAGE INTERFACE) =================
def render_animals_page():
    st.header("🐄 My Animals")
    
    col_l, col_r = st.columns([4, 1])
    with col_r:
        if st.button("➕ Add New Animal", type="primary", use_container_width=True):
            st.session_state.adding_animal = True

    if st.session_state.get("adding_animal", False):
        # UI matching your 'Add New Animal' reference image
        with st.form("new_animal_form"):
            st.subheader("Add New Animal")
            c1, c2 = st.columns(2)
            name = c1.text_input("Name *", placeholder="e.g., Bella")
            tag = c2.text_input("Tag Number *", placeholder="e.g., TAG-001")
            
            c3, c4 = st.columns(2)
            species = c3.selectbox("Species *", ["Cattle", "Buffalo", "Goat", "Sheep"])
            gender = c4.selectbox("Gender *", ["Female", "Male"])
            
            breed = st.text_input("Breed", placeholder="e.g., Angus, Holstein")
            
            c5, c6 = st.columns(2)
            dob = c5.date_input("Date of Birth")
            weight = c6.text_input("Weight (kg)", placeholder="e.g., 450")
            
            status = st.selectbox("Health Status", ["Healthy ✅", "Sick ⚠️", "Treated 💊"])
            notes = st.text_area("Notes", placeholder="Any additional notes...")
            
            b1, b2 = st.columns([1, 5])
            if b1.form_submit_button("Add"):
                new_data = [name, tag, species, gender, breed, dob, weight, status]
                st.session_state.herd_data.loc[len(st.session_state.herd_data)] = new_data
                st.session_state.adding_animal = False
                st.rerun()
            if b2.form_submit_button("Cancel"):
                st.session_state.adding_animal = False
                st.rerun()

    st.divider()
    st.dataframe(st.session_state.herd_data, use_container_width=True)

# ================= APP ROUTING =================
def main_app():
    cl, ct, cp = st.columns([5, 2, 2])
    dark_mode = ct.toggle("🌙 Dark Mode", value=True)
    if cp.button("👤 Profile"): st.session_state.page = "profile"; st.rerun()

    primary, bg, card, text = ("#4caf50", "#0e1117", "#1c2128", "#ffffff") if dark_mode else ("#2e7d32", "#f8fafc", "#ffffff", "#1e293b")
    apply_custom_styles(primary, bg, card, text)

    if st.session_state.user["role"] == "Veterinarian":
        st.markdown('<div class="header"><h1>👨‍⚕️ Vet Portal</h1></div>', unsafe_allow_html=True)
        st.write(f"Welcome Dr. {st.session_state.user['name']}")
    else:
        if st.session_state.sub_page == "home":
            st.markdown('<div class="header"><h1>🐄 Farmer Dashboard</h1></div>', unsafe_allow_html=True)
            _, mid, _ = st.columns([1,2,1])
            with mid:
                st.markdown('<div class="box-icon">📸</div>', unsafe_allow_html=True)
                if st.button("Camera & Upload", use_container_width=True):
                    st.session_state.sub_page = "camera"; st.rerun()
            c1, c2 = st.columns(2); c3, c4 = st.columns(2)
            with c1:
                st.markdown('<div class="box-icon">🐄</div>', unsafe_allow_html=True)
                if st.button("My Animals", use_container_width=True): st.session_state.sub_page = "animals"; st.rerun()
            with c2:
                st.markdown('<div class="box-icon">❤️</div>', unsafe_allow_html=True)
                if st.button("Health Monitoring", use_container_width=True): st.session_state.sub_page = "health"; st.rerun()
            with c3:
                st.markdown('<div class="box-icon">👨‍🌾</div>', unsafe_allow_html=True)
                if st.button("Find Vets", use_container_width=True): st.session_state.sub_page = "portal"; st.rerun()
            with c4:
                st.markdown('<div class="box-icon">📅</div>', unsafe_allow_html=True)
                if st.button("Attendance", use_container_width=True): st.session_state.sub_page = "attendance"; st.rerun()
        else:
            if st.button("⬅ Back"): st.session_state.sub_page = "home"; st.rerun()
            if st.session_state.sub_page == "animals": render_animals_page()
            elif st.session_state.sub_page == "camera": st.camera_input("Capture")
            elif st.session_state.sub_page == "health": st.metric("Herd Avg", "Healthy")
            elif st.session_state.sub_page == "portal": st.write("Searching Vets...")
            elif st.session_state.sub_page == "attendance": st.write("Attendance Marked")

if st.session_state.page == "login": login_page()
elif st.session_state.page == "signup": signup_page()
elif st.session_state.page == "profile": profile_page()
else: main_app()
