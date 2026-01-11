import streamlit as st

st.set_page_config(
    page_title="Livestock Care App",
    page_icon="🐄",
    layout="wide"
)

# ================= TOP SETTINGS STRIP =================
st.markdown("### ⚙️ App Controls")

col1, col2 = st.columns([8, 2])

with col2:
    dark_mode = st.toggle("🌙 Dark Mode", value=False)

with col1:
    with st.expander("⚙️ App Settings"):
        st.write("• Notifications (coming soon)")
        st.write("• Language (coming soon)")
        st.write("• Profile settings (coming soon)")

# ================= THEME COLORS =================
if dark_mode:
    bg = "#0e1117"
    card = "#161b22"
    text = "#ffffff"
    subtext = "#c9d1d9"
    primary = "#2ea043"
else:
    bg = "#f4f6f8"
    card = "#ffffff"
    text = "#000000"
    subtext = "#555555"
    primary = "#2e7d32"

# ================= STYLES =================
st.markdown(f"""
<style>
.stApp {{
    background-color: {bg};
    color: {text};
}}

.block-container {{
    padding-top: 1rem;
    padding-bottom: 6rem;
}}

.app-header {{
    background: linear-gradient(90deg, {primary}, #4caf50);
    padding: 26px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 28px;
}}

.card {{
    background-color: {card};
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.15);
    margin-bottom: 18px;
}}

.card p {{
    color: {subtext};
    font-size: 16px;
}}

.app-btn {{
    background: linear-gradient(90deg, {primary}, #4caf50);
    color: white;
    padding: 16px;
    border-radius: 14px;
    text-align: center;
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 14px;
}}

.bottom-nav {{
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: {card};
    border-top: 1px solid #ddd;
    display: flex;
    justify-content: space-around;
    padding: 12px 0;
}}

.nav-item {{
    font-size: 14px;
    color: {subtext};
}}

/* 🔹 FIX: Toggle label color based on mode */
.stToggle label span {{
    color: {text} !important;
}}
</style>
""", unsafe_allow_html=True)

# ================= APP HEADER =================
st.markdown("""
<div class="app-header">
    <h1>🐄 Livestock Care App</h1>
    <p>Smart monitoring for modern farmers</p>
</div>
""", unsafe_allow_html=True)

# ================= HOME CONTENT =================
st.markdown("""
<div class="card">
    <h3>Welcome 👋</h3>
    <p>
        Track livestock health, monitor activity, and connect with veterinarians —
        all from a single smart app designed for farmers.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="app-btn">🐄 Animals</div>
<div class="app-btn">❤️ Health Monitoring</div>
<div class="app-btn">👨‍🌾 Farmer / Vet Portal</div>
""", unsafe_allow_html=True)

# ================= BOTTOM NAV =================
st.markdown("""
<div class="bottom-nav">
    <div class="nav-item">🏠 Home</div>
    <div class="nav-item">🐄 Animals</div>
    <div class="nav-item">❤️ Health</div>
    <div class="nav-item">👤 Profile</div>
</div>
""", unsafe_allow_html=True)
