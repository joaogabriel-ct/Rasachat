import streamlit as st
import requests

st.title("Rasa Chat")

# Função para enviar a entrada do usuário para o Rasa e obter a resposta do assistente
def send_to_rasa(message):
    url = "http://localhost:5005/webhooks/rest/webhook"  # Endereço do servidor Rasa
    payload = {"sender": "user", "message": message}
    response = requests.post(url, json=payload).json()
    return response if response else [{"text": "No response from Rasa"}]

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):  # Mostrar um spinner enquanto aguarda a resposta do Rasa
        assistant_responses = send_to_rasa(prompt)
        for response in assistant_responses:
            with st.chat_message("assistant"):
                st.markdown(response['text'])
                st.session_state.messages.append({"role": "assistant", "content": response['text']})
