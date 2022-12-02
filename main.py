from flask import Flask, request
from src import classification 
import ast
import pickle
from flask_cors import CORS
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()
    
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

app = Flask(__name__)
CORS(app)

@app.route('/chat/')
def get_chattext():
    data = dict(request.args)
    print(dict(data))
    # data = request.json
    query = data.get('query', None)
    topic = data.get('topic', None)
    if not query:
        return "Give Valid Response" 
    if topic:
        topic =  ast.literal_eval(topic)
        result = classification.get_response(query, topic)
    else:
        result = classification.get_response(query)
    return result

"""
Load chitchat_classifier
"""
with open(r"data/chitchat_classifier.pkl", "rb") as f:
     chitchat_model = pickle.load(f)

"""
Load topic_classifier
"""
with open(r"data/topic_classifier.pkl", "rb") as f:
     topic_model = pickle.load(f)

"""
Load sbert model
"""
with open(r"data/df_topic_similarity.pkl", "rb") as f:
     similarity_data = pickle.load(f)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port = 5001)