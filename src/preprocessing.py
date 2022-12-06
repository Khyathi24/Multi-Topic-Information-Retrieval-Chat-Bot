import re
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

def chitchat_preprocessing(text_):
    try:
        text_ = text_.lower()
        text_ = re.sub(r'[^\w\s\n\r]', '', text_)
        text_ = re.sub('[ +]', ' ', text_).strip()
        terms = []
        for token in text_.split():
                terms.append(ps.stem(token.strip()))   # stemmer
        return ' '.join(terms)
    
    except:
        return text_

def reddit_preprocessing(text_):
    try:
        text_ = text_.lower()
        text_ = re.sub(r'[^\w\s\n\r]', '', text_)
        text_ = re.sub('[ +]', ' ', text_).strip()
        terms = []
        for token in text_.split():
            if token not in stop_words:              #stopwords
                terms.append(ps.stem(token.strip())) # stemmer
        return ' '.join(terms)
    except:
        return text_