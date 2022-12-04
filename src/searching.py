import json
import urllib.request
import urllib

def get_search_results_from_chitchat(query):
    q='%20'.join(query.split(' '))
    base_url='http://35.226.106.255:8983/solr/Chit_Chat_Indexer/select?indent=true&q.op=OR&q=preprocessed_question%3A%22'+q+'%22~5'
    response = urllib.request.urlopen(base_url)
    docs = json.load(response)['response']['docs']
    if len(docs)==0:
        base_url='http://35.226.106.255:8983/solr/Chit_Chat_Indexer/select?indent=true&q.op=OR&q=preprocessed_question%3A%22'+q+'%22~50'
        response = urllib.request.urlopen(base_url)
        docs = json.load(response)['response']['docs']
    return str(docs[0]['preprocessed_answer'])

def get_search_results_from_topic(query, topic):
    q='%20'.join(query.split(' '))
    base_url='http://35.226.106.255:8983/solr/RedditIndexer/select?bq=subreddit%3A'+topic+'%5E2&defType=edismax&fl=*%2Cscore&indent=true&wt=json&rows=20&q.op=OR&q=parent_body%3A%22'+q+'%22~20'
    response = urllib.request.urlopen(base_url)
    docs = json.load(response)['response']['docs']
    if len(docs)==0:
        base_url='http://35.226.106.255:8983/solr/RedditIndexer/select?bq=subreddit%3A'+topic+'%5E2&defType=edismax&fl=*%2Cscore&indent=true&wt=json&rows=20&q.op=OR&q=parent_body%3A%22'+q+'%22~100'
        response = urllib.request.urlopen(base_url)
        docs = json.load(response)['response']['docs']
    return str(docs[0]['final_body'][0])