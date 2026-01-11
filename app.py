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
        "name": "Guest User", 
        "email": "user@farm.com", 
        "role": "Farmer", 
        "phone": "+91 98765 43210",
        "location": "Default Farm Site",
        "details": {}
    }

if "attendance_logs" not in st.session_state:
    st.session_state.attendance_logs = []

if "sub_page" not in st.session_state:
    st.session_state.sub_page = "home"

if "herd_data" not in st.session_state:
    # Matching the columns to your new interface
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
    /* Form specific styling to match the image */
    .stForm {{
        background-color: #fcfdfa !important;
        border-radius: 15px !important;
        padding: 20px !important;
    }}
    .auth-container {{ text-align:center; padding:40px; }}
    .title-box {{
        background:#2e7d32; color:white; padding:20px;
        border-radius:16px; font-size:28px; font-weight:bold;
        margin-bottom:10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# ================= LOGIN & SIGNUP (SAME AS BEFORE) =================
def login_page():
    apply_custom_styles("#2e7d32", "#0e1117", "#1c2128", "#ffffff")
    _, c, _ = st.columns([1, 1.5, 1])
    with c:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('<div class="title-box">LIVESTOCK CARE APP</div>', unsafe_allow_html=True)
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
        role = st.radio("Select Role:", ["Farmer", "Veterinarian"], horizontal=True)
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            if st.form_submit_button("Sign Up"):
                st.session_state.user.update({"name": name, "email": email, "role": role})
                st.session_state.page = "app"; st.rerun()
        if st.button("Back to Login"):
            st.session_state.page = "login"; st.rerun()

# ================= ENHANCED PROFILE SECTION =================
def profile_page():
    apply_custom_styles("#4caf50", "#0e1117", "#1c2128", "#ffffff")
    st.markdown('<div class="header"><h1>👤 Profile Settings</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150)
        st.subheader(st.session_state.user["name"])
        st.caption(st.session_state.user["role"])

    with col2:
        with st.expander("✏️ Edit Account Details", expanded=True):
            with st.form("profile_edit"):
                new_name = st.text_input("Display Name", st.session_state.user["name"])
                new_phone = st.text_input("Phone Number", st.session_state.user["phone"])
                new_loc = st.text_input("Farm Location", st.session_state.user["location"])
                
                if st.form_submit_button("Save Changes"):
                    st.session_state.user.update({
                        "name": new_name,
                        "phone": new_phone,
                        "location": new_loc
                    })
                    st.success("Profile updated successfully!")
                    st.rerun()
        
        if st.button("Logout", type="secondary"):
            st.session_state.page = "login"; st.rerun()
        if st.button("⬅ Back to App"):
            st.session_state.page = "app"; st.rerun()

# ================= MY ANIMALS (NEW INTERFACE) =================
def render_animals_page():
    st.header("🐄 My Animals")
    
    # Top Action Bar
    col_a, col_b = st.columns([5, 1])
    with col_b:
        add_btn = st.button("➕ Add New Animal", type="primary", use_container_width=True)
        if add_btn:
            st.session_state.adding_animal = True

    # Floating form implementation matching your image
    if st.session_state.get("adding_animal", False):
        with st.form("add_new_animal_form"):
            st.subheader("Add New Animal")
            
            c1, c2 = st.columns(2)
            name = c1.text_input("Name *", placeholder="e.g., Bella")
            tag = c2.text_input("Tag Number *", placeholder="e.g., TAG-001")
            
            c3, c4 = st.columns(2)
            species = c3.selectbox("Species *", ["Cattle 🐄", "Buffalo 🐃", "Goat 🐐", "Sheep 🐑"])
            gender = c4.selectbox("Gender *", ["Female", "Male"])
            
            breed = st.text_input("Breed", placeholder="e.g., Angus, Holstein")
            
            c5, c6 = st.columns(2)
            dob = c5.date_input("Date of Birth", value=None)
            weight = c6.text_input("Weight (kg)", placeholder="e.g., 450")
            
            status = st.selectbox("Health Status", ["Healthy ✅", "Under Treatment 💊", "Sick ⚠️"])
            notes = st.text_area("Notes", placeholder="Any additional notes about this animal...")
            
            cb1, cb2 = st.columns([1, 5])
            if cb1.form_submit_button("Add"):
                new_row = [name, tag, species, gender, breed, dob, weight, status]
                st.session_state.herd_data.loc[len(st.session_state.herd_data)] = new_row
                st.session_state.adding_animal = False
                st.success(f"{name} added to herd!")
                st.rerun()
            if cb2.form_submit_button("Cancel"):
                st.session_state.adding_animal = False
                st.rerun()

    st.divider()
    if len(st.session_state.herd_data) > 0:
        st.dataframe(st.session_state.herd_data, use_container_width=True)
    else:
        st.info("No animals registered yet. Click the button above to start.")

# ================= REMAINING APP LOGIC =================
def render_farmer_portal():
    if st.session_state.sub_page == "home":
        st.markdown('<div class="header"><h1>🐄 Farmer Dashboard</h1></div>', unsafe_allow_html=True)
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
    else:
        if st.button("⬅ Back to Dashboard"):
            st.session_state.sub_page = "home"; st.rerun()
        
        if st.session_state.sub_page == "animals": render_animals_page()
        elif st.session_state.sub_page == "camera": st.camera_input("Capture")
        elif st.session_state.sub_page == "health": st.metric("Herd Health", "Good")
        elif st.session_state.sub_page == "portal": st.write("Searching Vets...")
        elif st.session_state.sub_page == "attendance": st.write("Marking Attendance...")

def main_app():
    cl, ct, cp = st.columns([5, 2, 2])
    dark_mode = ct.toggle("🌙 Dark Mode", value=True)
    if cp.button("👤 Profile"): st.session_state.page = "profile"; st.rerun()

    primary, bg, card, text = ("#4caf50", "#0e1117", "#1c2128", "#ffffff") if dark_mode else ("#2e7d32", "#f8fafc", "#ffffff", "#1e293b")
    apply_custom_styles(primary, bg, card, text)

    if st.session_state.user["role"] == "Veterinarian":
        st.title("Vet Portal Under Construction")
    else:
        render_farmer_portal()

if st.session_state.page == "login": login_page()
elif st.session_state.page == "signup": signup_page()
elif st.session_state.page == "profile": profile_page()
else: main_app()
