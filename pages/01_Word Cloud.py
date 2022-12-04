import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

st.sidebar.subheader("wordcloud Selection")
st.markdown("# WORD CLOUD")

numeric_columns = ['Technology', 'Politics', 'Education', 'Environment', 'Healthcare']
xaxis_col = st.sidebar.selectbox(label = 'Select column in x-axis', options = numeric_columns)


cols = {
    'Technology' :  [st.session_state['df_tech_ques'], st.session_state['df_tech_ans']],
    'Politics':  [st.session_state['df_poltics_ques'], st.session_state['df_poltics_ans']],
    'Education':  [st.session_state['df_edu_ques'], st.session_state['df_edu_ans']],
    'Environment':  [st.session_state['df_env_ques'], st.session_state['df_env_ans']],
    'Healthcare': [st.session_state['df_health_ques'], st.session_state['df_health_ans']]
    }

remove_words = {
    'Technology' :  (['I', '', 'like', 'The', "i'm", '-', '=', "\xa0", "it", "that's", "i've", "2", "&gt", "5"],
    []),
    'Politics':  (['could', 'said', 'even', 'also', 'know', 'want', '', '|', 'like', 'would', '-', "i'm", 'get', 'one', '\r', "i've", "i’m", "it’s", "it.", "me.", "us", "go"],
    []),
    'Education':  (['one', '|', 'would', '1', '-', '0', 'up', 'us', '.', "it's", "i've"],
    []),
    'Environment':  (['', "it.", "us", "i’m", "go", "think", "even", 'like', 'would', 'get', "i'm", 'one', 'know', 'also', '-', "it’s", "i've", "\r", "•"],
    []),
    'Healthcare': (["i’m", "would", "think", "really", '', 'one', 'like', 'get',"i'm", "it.", "see", "-", "i’m", "it’s", "i've", "&gt;", 'know', 'want', 'make', 'even', 'also', 'going', 'could', 'go', "don't", "don’t"],
    [])
    }

dict_que = {}
for ques in cols[xaxis_col][0]:
    for token in ques.split(' '):
        token = token.replace('\t', '').replace('\n', '')
        token = token.lower()
        if token not in stop_words and token not in remove_words[xaxis_col][0]:
            if token not in dict_que:
                dict_que[token] = 1
            else:
                dict_que[token] += 1
    
wordcloud = WordCloud(width=1600,
                    height=800,
                    background_color = 'silver',
                    ).generate_from_frequencies(frequencies=dict_que)
st.write(f'Questions in {xaxis_col} Topic')
plt.figure(figsize=(30,15))
plt.imshow(wordcloud)
plt.axis("off")
st.pyplot()

dict_ans = {}
for ques in cols[xaxis_col][1]:
    for token in ques.split(' '):
        token = token.replace('\t', '').replace('\n', '')
        token = token.lower()
        if token not in stop_words and token not in remove_words[xaxis_col][1]:
            if token not in dict_ans:
                dict_ans[token] = 1
            else:
                dict_ans[token] += 1
    
wordcloud = WordCloud(width=1600,
                    height=800,
                    background_color = 'silver',
                    ).generate_from_frequencies(frequencies=dict_ans)
st.write(f'Answers in {xaxis_col} Topic')
plt.figure(figsize=(30,15))
plt.imshow(wordcloud)
plt.axis("off")
st.pyplot()