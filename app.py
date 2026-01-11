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

# Shared list to store all appointments
if "appointments" not in st.session_state:
    st.session_state.appointments = []

if "all_users" not in st.session_state:
    st.session_state.all_users = [
        {"name": "Dr. Sharma", "role": "Veterinarian", "location": "Mumbai", "phone": "98765-12345", "spec": "Surgery"},
        {"name": "Dr. Khan", "role": "Veterinarian", "location": "Delhi", "phone": "91234-56789", "spec": "General"}
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

# ================= AUTH PAGES =================
def login_page():
    apply_custom_styles("#2e7d32", "#0e1117", "#1c2128", "#ffffff")
    _, c, _ = st.columns([1, 1.5, 1])
    with c:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('<div class="title-box">LIVESTOCK CARE APP</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-subtext">WELCOME TO LIVESTOCK CARE APP</div>', unsafe_allow_html=True)
        st.subheader("Sign In")
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

# ================= FARMER VET FINDER =================
def render_find_vets():
    st.header("👨‍⚕️ Find Local Veterinarians")
    search_loc = st.text_input("Enter your location:", placeholder="e.g., Mumbai")
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
                        # Save appointment to shared list
                        st.session_state.appointments.append({
                            "vet_name": st.session_state.booking_vet,
                            "farmer_name": st.session_state.user["name"],
                            "farmer_phone": st.session_state.user["phone"],
                            "date": str(d),
                            "time": str(t)
                        })
                        st.success("Appointment booked successfully!")
                        del st.session_state.booking_vet
        else:
            st.warning("No Vets found in this location.")

# ================= VET APPOINTMENT CHECKER =================
def render_vet_appointments():
    st.header("📅 Appointment Requests")
    my_name = st.session_state.user["name"]
    # Filter appointments for this specific vet
    my_appointments = [a for a in st.session_state.appointments if a['vet_name'].lower() in my_name.lower() or my_name.lower() in a['vet_name'].lower()]
    
    if my_appointments:
        for appt in my_appointments:
            with st.container(border=True):
                st.write(f"👤 **Farmer Name:** {appt['farmer_name']}")
                st.write(f"📞 **Phone:** {appt['farmer_phone']}")
                st.write(f"⏰ **Time:** {appt['date']} at {appt['time']}")
                st.button("✅ Accept", key=f"acc_{appt['time']}")
    else:
        st.info("No appointments booked yet.")

# ================= MAIN APP =================
def main_app():
    cl, ct, cp = st.columns([5, 2, 2])
    dark_mode = ct.toggle("🌙 Dark Mode", value=True)
    if cp.button("👤 Profile"): st.session_state.page = "profile"; st.rerun()
    primary, bg, card, text = ("#4caf50", "#0e1117", "#1c2128", "#ffffff") if dark_mode else ("#2e7d32", "#f8fafc", "#ffffff", "#1e293b")
    apply_custom_styles(primary, bg, card, text)

    if st.session_state.page == "profile":
        st.header("👤 Profile")
        st.write(st.session_state.user)
        if st.button("Logout"): st.session_state.page = "login"; st.rerun()
        if st.button("⬅ Back"): st.session_state.page = "app"; st.rerun()
    
    elif st.session_state.user["role"] == "Veterinarian":
        st.markdown(f'<div class="header"><h1>👨‍⚕️ Vet Portal</h1></div>', unsafe_allow_html=True)
        st.write(f"### Welcome Dr. {st.session_state.user['name']}")
        _, mid, _ = st.columns([1,2,1])
        with mid:
            st.markdown('<div class="box-icon">📅</div>', unsafe_allow_html=True)
            if st.button("Check Appointments", use_container_width=True):
                st.session_state.sub_page = "vet_appt"; st.rerun()
        
        if st.session_state.sub_page == "vet_appt":
            if st.button("⬅ Back"): st.session_state.sub_page = "home"; st.rerun()
            render_vet_appointments()

    else: # Farmer Portal
        if st.session_state.sub_page == "home":
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
            if st.button("⬅ Back"): st.session_state.sub_page = "home"; st.rerun()
            if st.session_state.sub_page == "portal": render_find_vets()
            elif st.session_state.sub_page == "animals": 
                # Same form logic you had
                st.header("🐄 My Animals")
                if st.button("➕ Add New Animal"): st.session_state.adding = True
                if st.session_state.get("adding"):
                    with st.form("a"):
                        n = st.text_input("Name")
                        if st.form_submit_button("Save"):
                             st.session_state.herd_data.loc[len(st.session_state.herd_data)] = [n, "0", "Cow", "F", "B", "2024", "0", "H"]
                             st.session_state.adding = False; st.rerun()
                st.dataframe(st.session_state.herd_data)
            elif st.session_state.sub_page == "camera":
                st.header("📸 Camera")
                tab1, tab2 = st.tabs(["Capture", "Upload"])
                with tab1: st.camera_input("Take Photo")
                with tab2: st.file_uploader("Upload")

# ================= RUN =================
if st.session_state.page == "login": login_page()
elif st.session_state.page == "signup": signup_page()
else: main_app()
