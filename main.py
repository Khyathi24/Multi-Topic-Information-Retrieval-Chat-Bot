import streamlit as st
import streamlit.components.v1 as components

# st.set_page_config(
#     page_title="Ex-stream-ly Cool App",
#     page_icon="🧊",
#     layout="centered")
st.set_page_config(layout="wide")
st.header("IR Chatbot")


HtmlFile = open("index.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code,height=700)