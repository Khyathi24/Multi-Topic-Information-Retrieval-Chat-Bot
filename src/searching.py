import json
import urllib.request
import urllib
from sklearn.metrics.pairwise import cosine_similarity
from .preprocessing import reddit_preprocessing, chitchat_preprocessing
from app import reddit_data, chitchat_data, sbert_model

def get_cosine_similary(a, b):
    return cosine_similarity(a,b)

def get_ranked_doc_chitchat_data(data, preprocessed_query):
    query_emedding = sbert_model.encode([preprocessed_query])

    responses = {}
    for value in data:
        if chitchat_data.iloc[value['index'][0]]['question'] ==  value['question'][0]:
            print(True)
        print(value['index'],  value['preprocessed_question'], value['answer'], value['preprocessed_answer'] )
        val = get_cosine_similary(chitchat_data.iloc[value['index'][0]-1]['pre_ques_embeddings'], query_emedding)
        responses[value['answer'][0]] = float(val)
    responses = sorted(responses.items(), key=lambda x: x[1], reverse=True)
    print(responses)
    if len(responses) > 0:
        return responses[0][0]
    else:
        return None

def get_ranked_doc_reddit_data(data, preprocessed_query):
    query_emedding = sbert_model.encode([preprocessed_query])

    responses = {}
    responses1 = {}
    for value in data:
        val = get_cosine_similary(reddit_data.iloc[value['index'][0]]['pre_ques_embeddings'], query_emedding)
        val1 = get_cosine_similary(reddit_data.iloc[value['index'][0]]['pre_ans_embeddings'], query_emedding)
        responses[value['Answer'][0]] = float(val)
        responses1[value['Answer'][0]] = float(val1)
    responses = sorted(responses.items(), key=lambda x: x[1], reverse=True)
    responses1 = sorted(responses1.items(), key=lambda x: x[1], reverse=True)
    print(responses)
    if len(responses) > 0:
        if responses[0][1]>responses1[0][1]:
            return responses[0][0]
        else:
            return responses1[0][0]
    else:
        return None

def get_the_reddit_result_based_on_cs(query, topic):
    query_emedding = sbert_model.encode([query])
    max_ = -9
    print(topic)
    reddit_topic_data = reddit_data[reddit_data['topic'] == topic]
    for idx, doc in reddit_topic_data.iterrows():
        ques_embedding = doc['pre_ques_embeddings']
        val = get_cosine_similary(ques_embedding, query_emedding)
        if val > max_:
            max_ = val
            resultant_que = doc['Question']
            resultant_ans = doc['Answer']
    print(resultant_que, resultant_ans, max_)
    return resultant_ans

def get_the_chitchat_result_based_on_cs(query):
    query_emedding = sbert_model.encode([query])
    max_ = -9
    for idx, doc in chitchat_data.iterrows():
        ques_embedding = doc['pre_ques_embeddings']
        val = get_cosine_similary(ques_embedding, query_emedding)
        if val > max_:
            max_ = val
            resultant_que = doc['question']
            resultant_ans = doc['answer']
    # print(resultant_que, resultant_ans, max_)
    return resultant_ans

# http://34.125.248.82:8000/
def get_search_results_from_chitchat(query):
    print(query)
    query = chitchat_preprocessing(query)
    q='%20'.join(query.split(' '))
    base_url='http://34.125.248.82:8983/solr/ChitChatIndexer/select?indent=true&q.op=OR&q=preprocessed_question%3A'+q
    response = urllib.request.urlopen(base_url)
    docs = json.load(response)['response']['docs']
    response = get_ranked_doc_chitchat_data(docs, query)
    print('response ', response)
    if not response:
        return get_the_chitchat_result_based_on_cs(query)
    return response

# def get_search_results_from_topic(query, topic):
#     query = reddit_preprocessing(query)
#     q='%20'.join(query.split(' '))
#     topic=topic.capitalize()
#     base_url = 'http://34.125.248.82:8983/solr/RedditIndexers/select?facet.field=topic&facet=true&fq=topic%3A'+topic+'&indent=true&q.op=OR&q=preprocessed_question%3A'+q    
#     response = urllib.request.urlopen(base_url)
#     docs = json.load(response)['response']['docs']
#     response = get_ranked_doc_reddit_data(docs, query)
#     print('response ', response)
#     if not response:
#         return get_the_reddit_result_based_on_cs(query, topic)
#     return response

def get_search_results_from_topic(query, topic):
    query = reddit_preprocessing(query)
    q='%20'.join(query.split(' '))
    if topic:
        topic=topic.capitalize()
    if topic==None:
        base_url = 'http://34.125.248.82:8983/solr/RedditIndexers/select?facet.field=topic&indent=true&q.op=OR&q=preprocessed_question%3A'+q
    elif len(query):
        base_url = 'http://34.125.248.82:8983/solr/RedditIndexers/select?facet.field=topic&facet=true&fq=topic%3A'+topic+'&indent=true&q.op=OR&q=preprocessed_question%3A'+q
    else:
        s=''
        for e in query:
            if e.isalnum():
                s+=e
            elif e==' ':
                s+='%20'
        base_url = 'http://34.125.248.82:8983/solr/RedditIndexers/select?facet.field=topic&facet=true&fq=topic%3A'+topic+'&indent=true&q.op=OR&q=preprocessed_question%3A'+q
    response = urllib.request.urlopen(base_url)
    docs = json.load(response)['response']['docs']
    response = get_ranked_doc_reddit_data(docs, query)
    if not response:
        return get_the_reddit_result_based_on_cs(query, topic)
    return response