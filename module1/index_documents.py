"""
Index documents.json file in the ElasticSearch database
"""

from elasticsearch import Elasticsearch
import json
from tqdm import tqdm

es_client = Elasticsearch("http://localhost:9200")


def index_documents():
    
    _index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "section": {"type": "text"},
                "question": {"type": "text"},
                "course": {"type": "keyword"} 
            }
        }
    }

    index_name = "course-questions"
    es_client.indices.create(index=index_name, body=_index_settings)
    
    with open("./documents.json") as f_in:
        docs_raw = json.load(f_in)
    
    documents = []
    
    for course_dict in docs_raw:
        for doc in course_dict['documents']:
            doc['course'] = course_dict['course']
            documents.append(doc)
    
    
    for doc in tqdm(documents):
        es_client.index(index=index_name,document=doc)


if __name__ == "__main__":
    index_documents()