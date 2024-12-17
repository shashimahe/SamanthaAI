import chromadb
from basic_functions import *

class shortTermMemory:
    def __init__(self):
        self.content = []

    def update(self, memory: dict):
        self.content.append(memory)

    def load(self, n_conv):
        convs = self.content[-n_conv:]
        return json_to_markdown(convs)

class longTermMemory:
    def __init__(self, db_name):
        self.chroma_client = chromadb.PersistentClient(path="SamanthaDB")
        self.collection = self.chroma_client.get_or_create_collection(name=db_name)

    def UpdateMemory(self, memory: dict):
        document = memory["document"]
        metadata = memory["metadata"]
        id = memory["id"]
        self.collection.upsert(
            documents=document,
            metadatas=metadata,
            ids=id
        )
        return "Memory Updated.."

    def RetreiveMemory(self, query):
        results = self.collection.query(
            query_texts=["donut"],
            n_results=3,
            include=['documents', 'distances', 'metadatas']
        )
        return results['documents']
