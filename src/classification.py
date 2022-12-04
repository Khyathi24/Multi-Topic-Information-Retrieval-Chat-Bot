"""
    We will have two classifiers 
    1. chitchat_classifier - Identifies if chit chat or not
    2. topic_classifier - Identifies the topic from the list of 5 or list of selected topics
"""

from .chitchat_classifier import check_if_chitchat_reddit
from .topic_classifier import check_the_topic, get_highest_similarity_topic
from .searching import get_search_results_from_chitchat, get_search_results_from_topic


def identify_the_index(query):
    """
    Takes Query as Input
    Outputs the topic
    index should be chitchat or reddit
    """
    #pass to the classifier 
    index = check_if_chitchat_reddit(query)
    if index == "chitchat":
        topic = None
        response = get_search_results_from_chitchat(query)
    else:
        topic = check_the_topic(query)
        response = get_search_results_from_topic(query, topic)
    return topic, response 


def get_response(query, topic_list = None):
    if not topic_list:
        topic, response = identify_the_index(query)
        # list of topics []
        # check whether it is a chitchat or topic
    elif topic_list:
        #Assuming there is no chitchat ques
        if len(topic_list) == 1:
            topic = [topic_list]
            #we can directly search in solr
            response = get_search_results_from_topic(query, topic_list[0])
        else:
            # topic classifier classifies the topic (remove results )
            # how to restrict the classifier to output certain topic
            #classfier -> topic : we can pick it
            # use the method cosine similarities <- 
            topic = check_the_topic(query)
            if topic in topic_list:
                response = get_search_results_from_topic(query, topic)
            else:
                topic = get_highest_similarity_topic(query, topic_list)
                response = get_search_results_from_topic(query, topic)
    return topic, response