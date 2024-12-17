import chromadb
import json

from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


from groq import Groq

class Model:
    def __init__(self):
        API_KEY = "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"
        self.client = Groq(api_key=API_KEY)

    def Complete(self, system, user):
        completion = self.client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": user
            },
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
        )
        result = completion.choices[0].message.content
        return result

class longTermMemory:
    def __init__(self, db_name):
        self.chroma_client = chromadb.PersistentClient(path="SamanthaDB")
        self.collection = self.chroma_client.get_or_create_collection(name=db_name)

    def UpdateMemory(self, doc):
        document = doc.get("content")
        metadata = doc.get("metadata")
        id = doc.get("id")
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

class Metadata(BaseModel):
    tags: List[str]
    note_type: str

class memoryDocModel(BaseModel):
    id: UUID = uuid4()
    content: str
    metadata: Metadata


model = Model()

long_term_memory = longTermMemory("first_test")

def agentDocUpdate(document):
    prompt = f"""
    User has provided the following information:
    ----

    {document}

    ----

    Your objective is to the contruct a JSON structure according to the given pydantic model in order to save the information in the database.
    
    Pydantic model:
    
    class Metadata(BaseModel):
        note_type: Literal['note', 'link', 'code', 'identity', 'list']

    class memoryDocModel(BaseModel):
        id: UUID = uuid4()
        content: str = Field(descrption="Copy the given information in this filed")
        metadata: Metadata
    
    Instructions to construct memoryDocModel:
    1. Read the information and decide weather its a plain note, any URL or links, any programming codes etc
    2. Dont delete any information just add all the given information in a content field of the above pydantic model
    3. Add appropriate note_type in the metadata, For example
    - If the information contains any code or programming related informations then add note_type as 'code'.
    - If the information contains any links or url then add note_type as 'link',
    - If the information contains any personal details or identities such as passwords, phone numbers etc. then add note_type as 'identity'

    Construct the output for memoryDocModel in JSON formate that validates the above pydantic model
    """
    response = model.Complete("", prompt)
    json_data = json.loads(response)
    print(f"Resulting model is:\n{json_data}")
    memory_update = long_term_memory.UpdateMemory(json_data)
    return {"success": True, "output": "MemoryUpdated"}

