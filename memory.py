import json
import chromadb

from models import *

class shortTermMemory:
    def __init__(self):
        self.content = []

    def update(self, conversation: conversationModel):
        self.content.append(conversation.model_dump_json())

    def load(self, n_conv):
        convs = self.content[-n_conv:]  # Fixed off-by-one error
        markdown_output = "# Recent converstaions\n"
        for entry in convs:
            record = json.loads(entry)
            user = record["user"]
            ai_response = record["ai"]
            markdown_output += f"{user['username']}: {user['query']}\n"
            markdown_output += f"AI: {ai_response}\n\n"
        return markdown_output


class longTermMemory:
    def __init__(self, db_name):
        self.chroma_client = chromadb.PersistentClient(path="SamanthaDB")
        self.collection = self.chroma_client.get_or_create_collection(name=db_name)

    def UpdateMemory(self, documents, ids):
        self.collection.upsert(
            documents=documents,
            #metadatas=metadatas,
            ids=ids
        )
        return "Memory Updated.."

    def RetreiveMemory(self, query):
        results = self.collection.query(
            query_texts=["donut"],
            n_results=1,
            include=['documents', 'distances', 'metadatas']
        )
        return results['documents']
