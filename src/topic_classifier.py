"""
    chitchat data 7000 convesr 
    each conv has about 20-30 msgs
    1. we will take all the msgs 
    2. preprocess the data
    3. remove the duplicates 20-30k 
    4. attach the above data with reddit data ; labels will 0 to 5
    5. Build a classifier - predicts chitchat data or reddit data 
    6. lets save the model
"""

"""
    1. load the model  ( this should happen in main; happens only once)
    2. Also load sentence transformer model 
    3. query should go same preprocessing steps
    4. to get the embeddings using sbert model 
    5. so predict using our model ;  topic from 5 topics
    6. pass topic name
"""

#import models

from app import topic_model, sbert_model, stop_words, ps, similarity_data
import re
from sklearn.metrics.pairwise import cosine_similarity


labels = {
    0 : 'politics',
    1 : 'healthcare', 
    2 : 'education',
    3 : 'environment',
    4 : 'technology'
}

def preprocessing(text_):
    try:
        text_ = text_.lower()
        text_ = re.sub('[^A-Za-z0-9 ]+', ' ', text_)
        text_ = re.sub('[ +]', ' ', text_).strip()
        terms = []
        for token in text_.split():
            if token not in stop_words:              #stopwords
                terms.append(ps.stem(token))         # stemmer
        return ' '.join(terms)
    
    except:
        return text_

def get_the_embeddings(preprocessed_query):
    Xtest = sbert_model.encode(preprocessed_query)
    return Xtest

def get_the_prediction(Xtest):
    ypred_ = topic_model.predict([Xtest]) 
    return labels[ypred_[0]]

def check_the_topic(query):
    preprocessed_query = preprocessing(query)
    xtest = get_the_embeddings(preprocessed_query)
    return get_the_prediction(xtest)


"""
cosine similarity get the topic with highest similarity 
removing the topics which are not in the list
"""

def get_cosine_similary(a, b):
    return cosine_similarity(a,b)

def get_topic_based_similarity(query_emedding):
    max_val = -1
    for idx, doc in similarity_data.iterrows():
        val = get_cosine_similary(doc['embeddings'], query_emedding.reshape(1, -1))
        if val > max_val:
            max_val = val
            print(max_val)
            desired_topic = doc['subreddit'] # still code is necessary to restrict the search results
    return desired_topic

def get_highest_similarity_topic(query, topic_list):
    preprocessed_query = preprocessing(query)
    query_emedding = get_the_embeddings(preprocessed_query)
    return get_topic_based_similarity(query_emedding)
