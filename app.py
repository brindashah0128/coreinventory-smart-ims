import streamlit as st
import database
import auth

from dashboard import show_dashboard
from products import product_page
from inventory import inventory_page
from analytics import show_analytics
from ai_insights import show_ai_insights


# Page configuration
st.set_page_config(
    page_title="CoreInventory Smart IMS",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

.main {
background-color: #f5f7fb;
}

h1, h2, h3 {
color: #1f4e79;
}

.stButton>button {
background-color: #4CAF50;
color: white;
border-radius: 8px;
height: 40px;
}

.stMetric {
background-color: #ffffff;
padding: 15px;
border-radius: 10px;
box-shadow: 0px 3px 6px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_signup_page():

    st.markdown('<p class="main-title">    📦CoreInventory Smart IMS   </p>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # LOGIN
    with tab1:

        st.subheader("Login to your account")

        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):

            user = auth.login_user(username, password)

            if user:
                st.session_state.logged_in = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")

    # SIGNUP
    with tab2:

        st.subheader("Create new account")

        new_user = st.text_input("Username", key="signup_user")
        new_pass = st.text_input("Password", type="password", key="signup_pass")

        if st.button("Sign Up"):

            auth.register_user(new_user, new_pass)

            st.success("Account created! You can now login.")


# Stop app if not logged in
if not st.session_state.logged_in:
    login_signup_page()
    st.stop()

st.markdown('<p class="main-title">📦 CoreInventory Smart IMS</p>', unsafe_allow_html=True)

# Sidebar navigation
menu = st.sidebar.radio(
    "📌 Navigation",
    [
        "📊 Dashboard",
        "📦 Product Management",
        "🚚 Inventory Operations",
        "📈 Analytics",
        "🤖 AI Insights"
    ]
)

# Page Routing
if menu == "📊 Dashboard":
    show_dashboard()

elif menu == "📦 Product Management":
    product_page()

elif menu == "🚚 Inventory Operations":
    inventory_page()

elif menu == "📈 Analytics":
    show_analytics()

elif menu == "🤖 AI Insights":
    show_ai_insights()

# Logout button
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()