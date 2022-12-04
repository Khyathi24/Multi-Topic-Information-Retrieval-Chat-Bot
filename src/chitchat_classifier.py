"""
    chitchat data 7000 convesr 
    each conv has about 20-30 msgs
    1. we will take all the msgs 
    2. preprocess the data
    3. remove the duplicates 20-30k 
    4. attach the above data with reddit data ; labels will be chitchat : 1, reddit data : 0
    5. Build a classifier - predicts chitchat data or reddit data 
    6. lets save the model
"""

"""
    1. load the model  ( this should happen in main; happens only once)
    2. Also load sentence transformer model 
    3. query should go same preprocessing steps
    4. to get the embeddings using sbert model 
    5. so predict using our model ; chitchat or topic
    6. pass "chitchat" or "topic"
"""
from app import chitchat_model, sbert_model, stop_words, ps
import re

labels = {
    1 : 'chitchat',
    0 : 'topic'
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
    ypred_ = chitchat_model.predict([Xtest]) 
    print('the prediction found is ', ypred_)
    return labels[ypred_[0]]

def check_if_chitchat_reddit(query):
    preprocessed_query = preprocessing(query)
    print(query)
    print(preprocessed_query)
    xtest = get_the_embeddings(query)
    return get_the_prediction(xtest)

