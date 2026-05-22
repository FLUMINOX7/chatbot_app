import streamlit as st
import requests

st.set_page_config(page_title="Pandas Chatbot", page_icon="🤖")

st.title("Chatbot Table Question Answering")

# ======================
# INIT CHAT HISTORY
# ======================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================
# DISPLAY CHAT HISTORY
# ======================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ======================
# INPUT (BOTTOM BAR)
# ======================
user_input = st.chat_input("Écris ton message...")

if user_input:

    # 1️⃣ afficher message utilisateur
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # 2️⃣ appel backend
    response = requests.post(
        "http://127.0.0.1:5000/pandas_predict",
        json={"text": user_input}
    )

    result = response.json()

    label = result["label"]
    message = result["message"]

    # 3️⃣ message assistant
    assistant_text = f"**{label}**\n\n{message}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_text
    })

    with st.chat_message("assistant"):
        st.markdown(assistant_text)