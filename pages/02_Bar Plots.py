import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

st.markdown("# Bar Graphs")
# bar_data  = st.session_state['df_bars']

numeric_columns = ['Technology', 'Politics', 'Education', 'Environment', 'Healthcare']
xaxis_col = st.sidebar.selectbox(label = 'Select column in x-axis', options = numeric_columns)

print(xaxis_col)
cols = {
    'Technology' :  [st.session_state['df_tech_ques'], st.session_state['df_tech_ans']],
    'Politics':  [st.session_state['df_poltics_ques'], st.session_state['df_poltics_ans']],
    'Education':  [st.session_state['df_edu_ques'], st.session_state['df_edu_ans']],
    'Environment':  [st.session_state['df_env_ques'], st.session_state['df_env_ans']],
    'Healthcare': [st.session_state['df_health_ques'], st.session_state['df_health_ans']]
    }

remove_words = {
    'Technology' :  (['I', '', 'like', 'The', "i'm", '-', '=', "\xa0", "it", "that's", "i've", "2", "&gt", "5"],
    ['', "i'm"]),
    'Politics':  (['could', 'said', 'even', 'also', 'know', 'want', '', '|', 'like', 'would', '-', "i'm", 'get', 'one', '\r', "i've", "i’m", "it’s", "it.", "me.", "us", "go"],
    ['']),
    'Education':  (['one', '|', 'would', '1', '-', '0', 'up', 'us', '.', "it's", "i've"],
    ['']),
    'Environment':  (['', "it.", "us", "i’m", "go", "think", "even", 'like', 'would', 'get', "i'm", 'one', 'know', 'also', '-', "it’s", "i've", "\r", "•"],
    ['']),
    'Healthcare': (["i’m", "would", "think", "really", '', 'one', 'like', 'get',"i'm", "it.", "see", "-", "i’m", "it’s", "i've", "&gt;", 'know', 'want', 'make', 'even', 'also', 'going', 'could', 'go', "don't", "don’t"],
    [''])
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
dict_que = dict(sorted(dict_que.items(), key = lambda x:x[1], reverse = True))
top_ngrams = {}
idx = 0
for key, val in dict_que.items():
    if idx == 20:
        break
    top_ngrams[key] = val
    idx += 1
    
# one_gram_top_words = dict_que(bar_data[xaxis_col])
x,y = list(top_ngrams.keys()), list(top_ngrams.values())

plt.figure(dpi = 200)
plt.ylabel(xaxis_col.title()+ ' Questions')
plt.xlabel("Frequencies")
sns.barplot(x = y,y = x, palette="rocket")
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
dict_ans = dict(sorted(dict_ans.items(), key = lambda x:x[1], reverse = True))
top_ngrams = {}
idx = 0
for key, val in dict_ans.items():
    if idx == 20:
        break
    top_ngrams[key] = val
    idx += 1

# one_gram_top_words = dict_ans(bar_data[xaxis_col])
x,y = list(top_ngrams.keys()), list(top_ngrams.values())

plt.figure( dpi = 200)
plt.ylabel(xaxis_col.title() + ' Answers')
plt.xlabel("Frequencies")
sns.barplot(x = y,y = x, palette="rocket")
st.pyplot()

# def get_ngrams_freq(df_col):
#     ngram_list = {}
#     for col in df_col:
#         try:
#             for token in col.split(' '):
#                 if token not in ngram_list:
#                     ngram_list[token] = 1
#                 else:
#                     ngram_list[token] += 1
#         except:
#             continue
#     ngram_list = dict(sorted(ngram_list.items(), key = lambda x:x[1], reverse = True))
#     top_ngrams = {}
#     idx = 0
#     for key, val in ngram_list.items():
#         if idx == 20:
#             break
#         top_ngrams[key] = val
#         idx += 1
#     return top_ngrams

# numeric_columns = bar_data.columns
# xaxis_col = st.sidebar.selectbox(label = 'Select column in x-axis', options = numeric_columns)

