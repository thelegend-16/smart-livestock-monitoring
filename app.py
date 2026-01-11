import streamlit as st

st.set_page_config(
    page_title="Livestock App",
    page_icon="🐄",
    layout="wide"
)

# ---------- APP STYLE ----------
st.markdown("""
<style>
body {
    background-color: #f4f6f8;
}

/* Header */
.app-header {
    background: linear-gradient(90deg, #2e7d32, #66bb6a);
    padding: 22px;
    border-radius: 16px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
}

/* Card */
.card {
    background-color: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

/* Button */
.app-btn {
    background-color: #2e7d32;
    color: white;
    padding: 14px;
    border-radius: 12px;
    text-align: center;
    font-size: 16px;
    margin-bottom: 12px;
}

/* Bottom Nav */
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: white;
    border-top: 1px solid #ddd;
    display: flex;
    justify-content: space-around;
    padding: 10px 0;
}

.nav-item {
    font-size: 14px;
    color: #444;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div class="app-header">
    <h1>🐄 Livestock Care App</h1>
    <p>Smart monitoring for modern farmers</p>
</div>
""", unsafe_allow_html=True)

# ---------- HOME ACTIONS ----------
st.markdown("""
<div class="card">
    <h3>Welcome 👋</h3>
    <p>Monitor livestock health, track animals, and connect with veterinarians using one app.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="app-btn">🐄 View Animals</div>
<div class="app-btn">❤️ Health Status</div>
<div class="app-btn">👨‍🌾 Farmer / Vet Portal</div>
""", unsafe_allow_html=True)

# ---------- BOTTOM NAV ----------
st.markdown("""
<div class="bottom-nav">
    <div class="nav-item">🏠 Home</div>
    <div class="nav-item">🐄 Animals</div>
    <div class="nav-item">❤️ Health</div>
    <div class="nav-item">👤 Profile</div>
</div>
""", unsafe_allow_html=True)
