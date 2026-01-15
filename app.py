import streamlit as st
import datetime

st.set_page_config(page_title="Obeisance", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

ADMIN_PASS = st.secrets.get("admin_password", "default_dev_pass")

theme_css = f"""
<style>
    .stApp {{
        background-color: #1a0033;
        color: #FFD700;
    }}
    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0);
    }}
    .stTextInput > div > div > input {{
        background-color: #2b0054;
        color: #FFD700;
        border: 2px solid #39FF14 !important;
    }}
    div[data-testid="stChatMessage"] {{
        border: 1px solid #FF0000;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }}
    .user-msg {{
        background-color: #555555 !important;
        margin-left: 20% !important;
        text-align: right;
    }}
    .other-msg {{
        background-color: #888888 !important;
        margin-right: 20% !important;
    }}
    .admin-msg {{
        background: linear-gradient(90deg, #C0C0C0, #FFFFFF, #C0C0C0);
        background-size: 200% 200%;
        animation: silverFlow 3s ease infinite;
        color: #0000FF !important;
        border: 2px solid #FFD700 !important;
    }}
    .admin-name {{
        color: #FFD700;
        font-weight: bold;
    }}
    @keyframes silverFlow {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
</style>
"""
st.markdown(theme_css, unsafe_allow_html=True)

with st.sidebar:
    st.title("Settings")
    new_name = st.text_input("Username (Max 12)", max_chars=12)
    admin_attempt = st.text_input("Admin Key", type="password")
    
    if st.button("Save Profile"):
        if new_name:
            st.session_state.user_name = new_name
            st.session_state.is_admin = (admin_attempt == ADMIN_PASS)
            st.rerun()

st.title("Obeisance - General")

if not st.session_state.user_name:
    st.warning("Please set a username in the settings sidebar to join.")
    st.stop()

for msg in st.session_state.messages:
    is_me = msg["user"] == st.session_state.user_name
    css_class = "admin-msg" if msg["is_admin"] else ("user-msg" if is_me else "other-msg")
    name_style = "admin-name" if msg["is_admin"] else ""
    
    st.markdown(f"""
    <div class="chat-bubble {css_class}" style="padding:10px; border-radius:10px; margin-bottom:5px; border: 1px solid red;">
        <span class="{name_style}">{msg['user']}</span>: {msg['content']}
    </div>
    """, unsafe_allow_html=True)

limit = 1000 if st.session_state.is_admin else 30
prompt = st.chat_input(f"Message (Max {limit} chars)")

if prompt:
    if len(prompt) > limit:
        st.error(f"Message too long! Max {limit} characters.")
    else:
        st.session_state.messages.append({
            "user": st.session_state.user_name,
            "content": prompt,
            "is_admin": st.session_state.is_admin,
            "time": datetime.datetime.now().strftime("%H:%M")
        })
        st.rerun()
