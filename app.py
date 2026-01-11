import streamlit as st

st.set_page_config(
    page_title="Smart Livestock Management",
    page_icon="🐄",
    layout="wide"
)

# ================= SESSION STATE =================
if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"  # login | signup | app
if "user_email" not in st.session_state:
    st.session_state.user_email = None


# ================= COMMON STYLES =================
def auth_styles():
    st.markdown("""
    <style>
    .auth-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 90vh;
        background-color: #f9faf7;
    }

    .auth-card {
        width: 420px;
        background: #ffffff;
        padding: 35px;
        border-radius: 18px;
        box-shadow: 0px 15px 40px rgba(0,0,0,0.12);
    }

    .auth-header {
        background: #2e7d32;
        color: white;
        text-align: center;
        padding: 18px;
        border-radius: 14px;
        margin-bottom: 25px;
        font-size: 18px;
        font-weight: 600;
    }

    .auth-title {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 5px;
        color: #1f2937;
    }

    .auth-subtitle {
        color: #6b7280;
        margin-bottom: 25px;
    }

    .auth-btn button {
        width: 100%;
        background: linear-gradient(90deg, #2e7d32, #4caf50);
        color: white;
        padding: 12px;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 600;
        border: none;
    }

    .auth-footer {
        text-align: center;
        margin-top: 18px;
        color: #374151;
    }

    .auth-footer span {
        color: #2e7d32;
        cursor: pointer;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)


# ================= LOGIN PAGE =================
def login_page():
    auth_styles()

    st.markdown("""
    <div class="auth-wrapper">
        <div class="auth-card">
            <div class="auth-header">Smart Livestock Management</div>
            <div class="auth-title">Welcome Back</div>
            <div class="auth-subtitle">Sign in to access your farm dashboard</div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign In")

    if submit:
        if email and password:
            st.session_state.user_email = email
            st.session_state.auth_page = "app"
            st.rerun()
        else:
            st.error("Please enter email and password")

    st.markdown("""
            <div class="auth-footer">
                Don't have an account?
                <span onclick="window.location.reload()">Sign up</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Go to Sign Up"):
        st.session_state.auth_page = "signup"
        st.rerun()


# ================= SIGN UP PAGE =================
def signup_page():
    auth_styles()

    st.markdown("""
    <div class="auth-wrapper">
        <div class="auth-card">
            <div class="auth-header">Smart Livestock Management</div>
            <div class="auth-title">Create Account</div>
            <div class="auth-subtitle">Sign up to start managing your livestock</div>
    """, unsafe_allow_html=True)

    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up")

    if submit:
        if email and password and password == confirm:
            st.session_state.user_email = email
            st.session_state.auth_page = "app"
            st.rerun()
        else:
            st.error("Check your inputs")

    if st.button("Already have an account? Sign In"):
        st.session_state.auth_page = "login"
        st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)


# ================= MAIN APP =================
def main_app():
    st.markdown("""
    <style>
    .profile-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.12);
        max-width: 400px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🐄 Livestock Care App")

    st.subheader("👤 Profile")

    st.markdown(f"""
    <div class="profile-card">
        <b>Email:</b> {st.session_state.user_email}<br><br>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Switch Account"):
            st.session_state.auth_page = "login"
            st.rerun()

    with col2:
        if st.button("Logout"):
            st.session_state.user_email = None
            st.session_state.auth_page = "login"
            st.rerun()


# ================= ROUTER =================
if st.session_state.auth_page == "login":
    login_page()
elif st.session_state.auth_page == "signup":
    signup_page()
else:
    main_app()
