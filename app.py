import streamlit as st
import time
import os, base64
import random
import asyncio
from main import ask_bodysync

# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="BodySync",
    page_icon="🧠",
    layout="wide"
)

# -------------------------------
# LOAD CSS
# -------------------------------
CSS_PATH = os.path.join(os.path.dirname(__file__), "style.css")

with open(CSS_PATH, "r", encoding="utf-8") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

if "_css_ready" not in st.session_state:
    st.session_state["_css_ready"] = True
    st.rerun()


# ========================
# LOGO PATH
# ========================
LOGO_PATH = os.path.join(
    "assets",
    "logo.png"
)

def get_base64_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ========================
# HEADER
# ========================
if os.path.exists(LOGO_PATH):
    logo_b64 = get_base64_image(LOGO_PATH)
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: -2rem;">
            <img src="data:image/png;base64,{logo_b64}" style="width:400px;" />
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        "<h1 style='text-align:center; margin-top: 0rem;'>BodySync</h1>",
        unsafe_allow_html=True,
    )


# -------------------------------
# SESSION STATE
# -------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# CHAT WINDOW
# -------------------------------

chat_box = st.container()

with chat_box:

    for msg in st.session_state.messages:

        if msg["role"] == "user":

            st.markdown(
                f'<div class="user-bubble">{msg["content"]}</div>',
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f'<div class="bot-bubble">{msg["content"]}</div>',
                unsafe_allow_html=True
            )

# -------------------------------
# USER INPUT
# -------------------------------

prompt = st.chat_input("Ask BodySync about your health")

if prompt:

    # show user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    # AI response
    with st.spinner("Analyzing your body data..."):
        answer = asyncio.get_event_loop().run_until_complete(
            ask_bodysync(prompt)
    )

    st.markdown(
        f'<div class="bot-bubble">{answer}</div>',
        unsafe_allow_html=True
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })