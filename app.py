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
        "location": "Default City"
    }

if "all_users" not in st.session_state:
    # Initial mock data for vets to test the matching system
    st.session_state.all_users = [
        {"name": "Dr. Sharma", "role": "Veterinarian", "location": "Mumbai", "phone": "98765-12345", "spec": "Surgery"},
        {"name": "Dr. Khan", "role": "Veterinarian", "location": "Delhi", "phone": "91234-56789", "spec": "General"},
        {"name": "Dr. Reddy", "role": "Veterinarian", "location": "Mumbai", "phone": "99887-77665", "spec": "Vaccination"}
    ]

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
    div.stButton > button:hover {{
        background-color: {primary} !important;
        color: white !important;
    }}
    /* Login Interface Styles */
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
            loc = st.text_input("Location (City)")
            phone = st.text_input("Phone Number")
            if st.form_submit_button("Sign Up"):
                new_user = {"name": name, "email": email, "role": role, "location": loc, "phone": phone}
                st.session_state.all_users.append(new_user)
                st.session_state.user = new_user
                st.session_state.page = "app"; st.rerun()
        if st.button("Back to Login"):
            st.session_state.page = "login"; st.rerun()

# ================= FEATURE MODULES =================
def render_animals_page():
    st.header("🐄 My Animals")
    if st.button("➕ Add New Animal", type="primary"):
        st.session_state.adding_animal = True

    if st.session_state.get("adding_animal", False):
        with st.form("animal_form"):
            st.subheader("Add New Animal")
            c1, c2 = st.columns(2)
            name = c1.text_input("Name *", placeholder="e.g., Bella")
            tag = c2.text_input("Tag Number *", placeholder="e.g., TAG-001")
            c3, c4 = st.columns(2)
            species = c3.selectbox("Species *", ["Cattle", "Buffalo", "Goat", "Sheep"])
            gender = c4.selectbox("Gender *", ["Female", "Male"])
            breed = st.text_input("Breed", placeholder="e.g., Angus")
            c5, c6 = st.columns(2)
            dob = c5.date_input("Date of Birth")
            weight = c6.text_input("Weight (kg)")
            status = st.selectbox("Health Status", ["Healthy", "Sick", "Under Treatment"])
            if st.form_submit_button("Save"):
                st.session_state.herd_data.loc[len(st.session_state.herd_data)] = [name, tag, species, gender, breed, dob, weight, status]
                st.session_state.adding_animal = False
                st.rerun()
            if st.form_submit_button("Cancel"):
                st.session_state.adding_animal = False
                st.rerun()
    st.dataframe(st.session_state.herd_data, use_container_width=True)

def render_camera_page():
    st.header("📸 Camera & Upload")
    tab1, tab2 = st.tabs(["📷 Take Photo", "📁 Upload Image"])
    with tab1:
        img = st.camera_input("Capture")
        if img: st.image(img)
    with tab2:
        up = st.file_uploader("Upload", type=["jpg", "png"])
        if up: st.image(Image.open(up))

def render_find_vets():
    st.header("👨‍⚕️ Find Local Veterinarians")
    search_loc = st.text_input("Enter your location to match with Vets:", placeholder="e.g., Mumbai")
    if search_loc:
        matches = [v for v in st.session_state.all_users if v['role'] == "Veterinarian" and v['location'].lower() == search_loc.lower()]
        if matches:
            for vet in matches:
                with st.container(border=True):
                    st.subheader(vet['name'])
                    st.write(f"📞 Contact: {vet['phone']} | 📍 Location: {vet['location']}")
                    if st.button(f"Book Appointment with {vet['name']}"):
                        st.session_state.booking_vet = vet['name']
            
            if "booking_vet" in st.session_state:
                with st.form("book_vet"):
                    st.write(f"### Scheduling with {st.session_state.booking_vet}")
                    d = st.date_input("Select Date")
                    t = st.time_input("Select Time")
                    if st.form_submit_button("Confirm"):
                        st.success("Appointment booked successfully!")
                        del st.session_state.booking_vet
        else:
            st.warning("No Vets found in this location.")

# ================= MAIN APP LAYOUT =================
def main_app():
    cl, ct, cp = st.columns([5, 2, 2])
    dark_mode = ct.toggle("🌙 Dark Mode", value=True)
    if cp.button("👤 Profile"): st.session_state.page = "profile"; st.rerun()
    primary, bg, card, text = ("#4caf50", "#0e1117", "#1c2128", "#ffffff") if dark_mode else ("#2e7d32", "#f8fafc", "#ffffff", "#1e293b")
    apply_custom_styles(primary, bg, card, text)

    if st.session_state.page == "profile":
        st.header("👤 Profile Settings")
        with st.form("edit_profile"):
            u_name = st.text_input("Name", st.session_state.user["name"])
            u_loc = st.text_input("Location", st.session_state.user["location"])
            u_phone = st.text_input("Phone", st.session_state.user["phone"])
            if st.form_submit_button("Save"):
                st.session_state.user.update({"name": u_name, "location": u_loc, "phone": u_phone})
                st.success("Updated!")
        if st.button("Logout"): st.session_state.page = "login"; st.rerun()
        if st.button("⬅ Back"): st.session_state.page = "app"; st.rerun()
    
    elif st.session_state.sub_page == "home":
        st.markdown('<div class="header"><h1>🐄 Dashboard</h1></div>', unsafe_allow_html=True)
        _, mid, _ = st.columns([1,2,1])
        with mid:
            st.markdown('<div class="box-icon">📸</div>', unsafe_allow_html=True)
            if st.button("Camera & Upload", use_container_width=True): st.session_state.sub_page = "camera"; st.rerun()
        c1, c2 = st.columns(2); c3, c4 = st.columns(2)
        with c1:
            st.markdown('<div class="box-icon">🐄</div>', unsafe_allow_html=True)
            if st.button("My Animals", use_container_width=True): st.session_state.sub_page = "animals"; st.rerun()
        with c2:
            st.markdown('<div class="box-icon">❤️</div>', unsafe_allow_html=True)
            if st.button("Health Monitoring", use_container_width=True): st.session_state.sub_page = "health"; st.rerun()
        with c3:
            st.markdown('<div class="box-icon">👨‍⚕️</div>', unsafe_allow_html=True)
            if st.button("Find Vets", use_container_width=True): st.session_state.sub_page = "portal"; st.rerun()
        with c4:
            st.markdown('<div class="box-icon">📅</div>', unsafe_allow_html=True)
            if st.button("Attendance", use_container_width=True): st.session_state.sub_page = "attendance"; st.rerun()
    else:
        if st.button("⬅ Back to Dashboard"): st.session_state.sub_page = "home"; st.rerun()
        if st.session_state.sub_page == "animals": render_animals_page()
        elif st.session_state.sub_page == "camera": render_camera_page()
        elif st.session_state.sub_page == "portal": render_find_vets()
        elif st.session_state.sub_page == "health": st.metric("Herd Status", "Healthy")
        elif st.session_state.sub_page == "attendance": st.write("Attendance Logs...")

# ================= RUN =================
if st.session_state.page == "login": login_page()
elif st.session_state.page == "signup": signup_page()
else: main_app()
