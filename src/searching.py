import json
import urllib.request
import urllib
import re

def preprocessing(text_):
    try:
        text_ = text_.lower()
        # text_ = re.sub('[^A-Za-z0-9 ]+', ' ', text_)
        text_ = re.sub(r'[^\w\s]', '', text_)
        text_ = re.sub('[ +]', ' ', text_).strip()
        terms = []
        for token in text_.split():
            # if token not in stop_words:              #stopwords
                terms.append(ps.stem(token.strip()))         # stemmer
        return ' '.join(terms)
    
    except:
        return text_


def get_search_results_from_chitchat(query):
    query = preprocessing(query)
    q='%20'.join(query.split(' '))
    base_url='http://35.226.106.255:8983/solr/ChitchatIndexing/select?indent=true&q.op=OR&q=preprocessed_question%3A%22'+q+'%22~5'
    response = urllib.request.urlopen(base_url)
    docs = json.load(response)['response']['docs']
    if len(docs)==0:
        base_url='http://35.226.106.255:8983/solr/ChitchatIndexing/select?indent=true&q.op=OR&q=preprocessed_question%3A%22'+q+'%22~50'
        response = urllib.request.urlopen(base_url)
        docs = json.load(response)['response']['docs']
    if docs:
        return str(docs[0]['Answer'])
    else:
        return "No proper response found for this query!"

def get_search_results_from_topic(query, topic):
    query = preprocessing(query)
    q='%20'.join(query.split(' '))
    base_url='http://35.226.106.255:8983/solr/RedditIndexer/select?bq=subreddit%3A'+topic+'%5E2&defType=edismax&fl=*%2Cscore&indent=true&wt=json&rows=20&q.op=OR&q=parent_body%3A%22'+q+'%22~20'
    response = urllib.request.urlopen(base_url)
    docs = json.load(response)['response']['docs']
    if len(docs)==0:
        base_url='http://35.226.106.255:8983/solr/RedditIndexer/select?bq=subreddit%3A'+topic+'%5E2&defType=edismax&fl=*%2Cscore&indent=true&wt=json&rows=20&q.op=OR&q=parent_body%3A%22'+q+'%22~100'
        response = urllib.request.urlopen(base_url)
        docs = json.load(response)['response']['docs']
    if docs:
        return str(docs[0]['final_body'][0])
    else:
        return "No proper response found for this query!"