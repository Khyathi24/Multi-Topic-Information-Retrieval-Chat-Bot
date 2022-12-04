"""
1. load the pickle file and follow the process

"""
import os
import pysolr
import requests
import pickle
import pandas as pd

CORE_NAME = "Chitchat_Indexer"
AWS_IP = "35.226.106.255"

tweets = pd.read_pickle("./chit_chat_data.pkl").to_dict(orient="records")

def delete_core(core=CORE_NAME):
    print(os.system('sudo su - solr -c "/opt/solr/bin/solr delete -c {core}"'.format(core=core)))

def create_core(core=CORE_NAME):
    print(os.system(
        'sudo su - solr -c "/opt/solr/bin/solr create -c {core} -n data_driven_schema_configs"'.format(
            core=core)))


class Indexer:
    def _init_(self):
        self.solr_url = f'http://34.83.198.169:8983/solr/'
        self.connection = pysolr.Solr('http://34.83.198.169:8983/solr/' + CORE_NAME, always_commit=True, timeout=5000000)

    def do_initial_setup(self):
        delete_core()
        create_core()

    def create_documents(self, docs):
        print(pysolr.Solr('http://34.83.198.169:8983/solr/'+ CORE_NAME, always_commit=True, timeout=5000000).add(docs))

    def add_fields(self):
        data = {
            "add-field": [
                {
                    "name": "Question",
                    "type": "string",
                    "multiValued": False
                }, {
                    "name": "Answer",
                    "type": "string",
                    "multiValued": False
                },
                {
                    "name": "Prompt",
                    "type": "string",
                    "multiValued": False
                },
                {
                    "name": "preprocessed_question",
                    "type": "string",
                    "multiValued": True
                },
                {
                    "name": "preprocessed_answer",
                    "type": "string",
                    "multiValued": False
                },
                {
                    "name": "preprocessed_prompt",
                    "type": "string",
                    "multiValued": False
                },
                {
                    "name": "topic",
                    "type": "string",
                    "multiValued": False
                },
            ]
        }

        print(requests.post('http://34.83.198.169:8983/solr/'+CORE_NAME + "/schema", json=data).json())


if __name__ == "__main__":
    i = Indexer()
    i.do_initial_setup()
    i.add_fields()
    i.create_documents(tweets)
