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
        print(value['index'],  value['preprocessed_question'], value['answer'], value['preprocessed_answer'] )
        val = get_cosine_similary(chitchat_data.iloc[value['index'][0]-1]['pre_ques_embeddings'], query_emedding)
        responses[value['answer'][0]] = float(val)
    responses = sorted(responses.items(), key=lambda x: x[1], reverse=True)
    print(responses)
    if len(responses) > 1:
        return responses[0][0]
    else:
        return "No proper response found for this query!"

def get_ranked_doc_reddit_data(data, preprocessed_query):
    query_emedding = sbert_model.encode([preprocessed_query])

    responses = {}
    for value in data:
        print(value['index'],  value['preprocessed_question'], value['Answer'], value['preprocessed_answer'] )
        val = get_cosine_similary(reddit_data.iloc[value['index'][0]-1]['pre_ques_embeddings'], query_emedding)
        responses[value['Answer'][0]] = float(val)
    responses = sorted(responses.items(), key=lambda x: x[1], reverse=True)
    print(responses)
    if len(responses) > 1:
        return responses[0][0]
    else:
        return "No proper response found for this query!"

def get_search_results_from_chitchat(query):
    query = chitchat_preprocessing(query)
    q='%20'.join(query.split(' '))
    base_url='http://34.125.44.135:8983/solr/ChitChatIndexer/select?indent=true&q.op=OR&q=preprocessed_question%3A'+q
    response = urllib.request.urlopen(base_url)
    docs = json.load(response)['response']['docs']
    return get_ranked_doc_chitchat_data(docs, query)

def get_search_results_from_topic(query, topic):
    query = reddit_preprocessing(query)
    q='%20'.join(query.split(' '))
    topic=topic.capitalize()
    base_url = 'http://34.125.44.135:8983/solr/RedditIndexer/select?facet.field=topic&facet=true&fq=topic%3A'+topic+'&indent=true&q.op=OR&q=preprocessed_question%3A'+q    
    response = urllib.request.urlopen(base_url)
    docs = json.load(response)['response']['docs']
    return get_ranked_doc_reddit_data(docs, query)