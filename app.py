import uuid
import streamlit as st
import requests

# Backend API URL
API_URL = "http://localhost:8000/chat"

# Generate session_id once per Streamlit run
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.set_page_config(page_title="CRM RAG Chatbot", page_icon="💬")
st.title("🤖 CRM Chatbot (Powered by LLaMA + RAG)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about your leads, opportunities..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        res = requests.post(API_URL, json={
            "question": prompt,
            "session_id": st.session_state.session_id
        })
        res.raise_for_status()
        answer = res.json()["response"]
    except Exception as e:
        answer = f"⚠️ Error contacting backend: {e}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
