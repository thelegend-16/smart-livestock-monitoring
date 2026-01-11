import streamlit as st

st.set_page_config(
    page_title="Livestock Care App",
    page_icon="🐄",
    layout="wide"
)

# ================= LANGUAGE DATA =================
LANGUAGES = {
    "English": {
        "title": "Livestock Care App",
        "subtitle": "Smart monitoring for modern farmers",
        "welcome": "Welcome 👋",
        "desc": "Track livestock health, monitor activity, and connect with veterinarians — all from a single smart app designed for farmers.",
        "animals": "Animals",
        "health": "Health Monitoring",
        "portal": "Farmer / Vet Portal",
        "controls": "App Controls",
        "settings": "App Settings",
        "dark": "Dark Mode"
    },
    "Hindi": {
        "title": "पशुधन देखभाल ऐप",
        "subtitle": "आधुनिक किसानों के लिए स्मार्ट निगरानी",
        "welcome": "स्वागत है 👋",
        "desc": "पशुओं के स्वास्थ्य की निगरानी करें, गतिविधि ट्रैक करें और पशु चिकित्सकों से जुड़ें।",
        "animals": "पशु",
        "health": "स्वास्थ्य निगरानी",
        "portal": "किसान / पशु चिकित्सक पोर्टल",
        "controls": "ऐप नियंत्रण",
        "settings": "ऐप सेटिंग्स",
        "dark": "डार्क मोड"
    },
    "Tamil": {
        "title": "மிருக பராமரிப்பு செயலி",
        "subtitle": "நவீன விவசாயிகளுக்கான புத்திசாலி கண்காணிப்பு",
        "welcome": "வரவேற்கிறோம் 👋",
        "desc": "மிருக ஆரோக்கியத்தை கண்காணிக்கவும், செயல்பாட்டை கண்காணிக்கவும் மற்றும் விலங்கு மருத்துவருடன் இணைக்கவும்.",
        "animals": "மிருகங்கள்",
        "health": "ஆரோக்கிய கண்காணிப்பு",
        "portal": "விவசாயி / மருத்துவர் போர்டல்",
        "controls": "அப் கட்டுப்பாடுகள்",
        "settings": "அப் அமைப்புகள்",
        "dark": "இருண்ட முறை"
    }
}

# ================= TOP CONTROLS =================
st.markdown(f"### ⚙️ {LANGUAGES['English']['controls']}")

col1, col2, col3 = st.columns([6, 2, 2])

with col3:
    selected_language = st.selectbox("🌐 Language", list(LANGUAGES.keys()))

lang = LANGUAGES[selected_language]

with col2:
    dark_mode = st.toggle(f"🌙 {lang['dark']}", value=False)

with col1:
    with st.expander(f"⚙️ {lang['settings']}"):
        st.write("• Notifications (coming soon)")
        st.write("• Language preferences")
        st.write("• Profile settings")

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

[data-testid="stToggle"] label div {{
    color: {text} !important;
}}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown(f"""
<div class="app-header">
    <h1>🐄 {lang['title']}</h1>
    <p>{lang['subtitle']}</p>
</div>
""", unsafe_allow_html=True)

# ================= HOME CONTENT =================
st.markdown(f"""
<div class="card">
    <h3>{lang['welcome']}</h3>
    <p>{lang['desc']}</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="app-btn">🐄 {lang['animals']}</div>
<div class="app-btn">❤️ {lang['health']}</div>
<div class="app-btn">👨‍🌾 {lang['portal']}</div>
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
