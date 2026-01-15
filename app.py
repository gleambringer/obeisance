import streamlit as st
import datetime

st.set_page_config(page_title="Obeisance", layout="wide", initial_sidebar_state="collapsed")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

pwd_secret = st.secrets.get("admin_password", "admin123")

st.markdown("""
<style>
    .stApp {
        background-color: #1a0033;
    }
    [data-testid="stHeader"] {
        background: none;
    }
    section[data-testid="stSidebar"] {
        background-color: #0d001a;
        border-right: 2px solid #39FF14;
    }
    .stTextInput input {
        background-color: #2b0054 !important;
        color: #FFD700 !important;
        border: 1px solid #39FF14 !important;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .msg {
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #FF0000;
        max-width: 70%;
        font-family: sans-serif;
    }
    .right {
        align-self: flex-end;
        background-color: #555555;
        color: #FFD700;
    }
    .left {
        align-self: flex-start;
        background-color: #333333;
        color: #FFD700;
    }
    .admin-box {
        background: linear-gradient(-45deg, #C0C0C0, #FFFFFF, #E5E4E2, #C0C0C0);
        background-size: 400% 400%;
        animation: silver-shine 3s ease infinite;
        color: #0000FF !important;
        border: 2px solid #FFD700 !important;
        font-weight: bold;
    }
    .admin-label {
        color: #FFD700;
        font-weight: 900;
        text-transform: uppercase;
        font-size: 0.8em;
        display: block;
        margin-bottom: 2px;
    }
    @keyframes silver-shine {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    h1 {
        color: #FFD700 !important;
        text-align: center;
        border-bottom: 2px solid #39FF14;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Obeisance Setup")
    u_input = st.text_input("Username", max_chars=12)
    a_input = st.text_input("Admin Key", type="password")
    if st.button("Enter General"):
        if u_input:
            st.session_state.user_name = u_input
            st.session_state.is_admin = (a_input == pwd_secret)
            st.rerun()

st.title("OBEISANCE")

if not st.session_state.user_name:
    st.info("Open Sidebar to Set Identity")
    st.stop()

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for m in st.session_state.messages:
    side = "right" if m["user"] == st.session_state.user_name else "left"
    style = "admin-box" if m["is_admin"] else side
    name_tag = f'<span class="admin-label">{m["user"]}</span>' if m["is_admin"] else f'<b>{m["user"]}</b>: '
    
    st.markdown(f"""
    <div class="msg {style}">
        {name_tag} {m["content"]}
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

char_max = 1000 if st.session_state.is_admin else 30
prompt = st.chat_input(f"General Room | {char_max} chars max")

if prompt:
    if len(prompt) > char_max:
        st.error(f"Limit exceeded: {len(prompt)}/{char_max}")
    else:
        st.session_state.messages.append({
            "user": st.session_state.user_name,
            "content": prompt,
            "is_admin": st.session_state.is_admin
        })
        st.rerun()
