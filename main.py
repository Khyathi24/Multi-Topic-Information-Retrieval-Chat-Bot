import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import pickle

st.set_page_config(layout="wide")
st.header("IR Chatbot")
st.set_option('deprecation.showPyplotGlobalUse', False)

HtmlFile = open("index.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code,height=700)


with open(r"data/RedditData.pkl", "rb") as f:
     df = pickle.load(f)
print(df.shape)

# word cloud
df_poltics_ques = list(set(list(df[df['topic'] == 'Politics']['Question'])))
st.session_state['df_poltics_ques'] = df_poltics_ques

df_poltics_ans = list(set(list(df[df['topic'] == 'Politics']['Answer'])))
st.session_state['df_poltics_ans'] = df_poltics_ans


df_health_ques = list(set(list(df[df['topic'] == 'Healthcare']['Question'])))
st.session_state['df_health_ques'] = df_health_ques

df_health_ans = list(set(list(df[df['topic'] == 'Healthcare']['Answer'])))
st.session_state['df_health_ans'] = df_health_ans


df_edu_ques = list(set(list(df[df['topic'] == 'Education']['Question'])))
st.session_state['df_edu_ques'] = df_edu_ques

df_edu_ans = list(set(list(df[df['topic'] == 'Education']['Answer'])))
st.session_state['df_edu_ans'] = df_edu_ans


df_env_ques = list(set(list(df[df['topic'] == 'Environment']['Question'])))
st.session_state['df_env_ques'] = df_env_ques

df_env_ans = list(set(list(df[df['topic'] == 'Environment']['Answer'])))
st.session_state['df_env_ans'] = df_env_ans


df_tech_ques = list(set(list(df[df['topic'] == 'Technology']['Question'])))
st.session_state['df_tech_ques'] = df_tech_ques

df_tech_ans = list(set(list(df[df['topic'] == 'Technology']['Answer'])))
st.session_state['df_tech_ans'] = df_tech_ans