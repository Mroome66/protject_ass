import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from auth_key import get_api_key
from PdfLoader import PDFProcessor
from analysis_level import det_user_level
from Custom_GigaChat import LogGigaChat


key = get_api_key()
giga =LogGigaChat(log_file='log.txt',credentials=key, verify_ssl_certs=False)


st.set_page_config(page_title="Диалог с GigaChat", layout="wide")
st.title("Диалог с GigaChat")

if "messages" not in st.session_state:
    level_prompt = det_user_level(giga)
    pdf_path = "NLP.pdf"
    documentation_prompt = PDFProcessor(pdf_path=pdf_path).load_and_prepare_pdf()
    
    st.session_state.messages = [
        SystemMessage(content=f"{level_prompt}\n{documentation_prompt}")
    ]

for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    elif isinstance(message, SystemMessage):
        continue  
    else:
        with st.chat_message("assistant"):
            st.write(message.content)

if prompt := st.chat_input("Введите ваше сообщение"):
    st.session_state.messages.append(HumanMessage(content=prompt))
   
    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("GigaChat думает..."):
        response = giga.invoke(st.session_state.messages)
        st.session_state.messages.append(response)
    
    with st.chat_message("assistant"):
        st.write(response.content)