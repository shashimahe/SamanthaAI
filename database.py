import chromadb
import psycopg2

with psycopg2.connect(
    dbname="samanthadb",
    host="localhost",
    user="shashimahe",
    password="Shashi@24",
    port="5432"
) as conn:

    cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE nodes (
        id SERIAL PRIMARY KEY,
        type VARCHAR(100),
        label VARCHAR(1000)
        properties JSONB
        )
        """
    )

    cursor.close()

class Memory:
    def __init__(self, path, db_name):
        self.chroma_client = chromadb.PersistentClient(path=path)
        self.collection = self.chroma_client.get_or_create_collection(name=db_name)

    def UpdateMemory(self, documents, metadatas, ids):
        self.collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        return "Memory Updated.."

    def RetreiveMemory(self, query):
        results = self.collection.query(
            query_texts=["donut"],
            n_results=5,
            include=['documents', 'distances', 'metadatas']
        )
        return results['documents']


