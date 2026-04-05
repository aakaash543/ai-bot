import chromadb
from chromadb.config import Settings
import json
import uuid

class ErrorDB:
    def __init__(self, db_path="./chroma_data"):
        self.client = chromadb.PersistentClient(path=db_path)
        # Using the default sentence-transformers model embedded in ChromaDB
        self.collection = self.client.get_or_create_collection(name="error_logs")

    def ingest_data(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        ids = []
        documents = []
        metadatas = []

        for item in data:
            doc_id = str(uuid.uuid4())
            # Embed the error message and stack trace together for semantic search
            document = f"Error: {item['error_message']}\nTrace: {item['stack_trace']}"
            
            # Store the solution in metadata so we can retrieve it
            metadata = {
                "solution_code": item["solution_code"],
                "explanation": item["explanation"]
            }
            
            ids.append(doc_id)
            documents.append(document)
            metadatas.append(metadata)

        if ids:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Ingested {len(ids)} error logs into the database.")

    def query_similar_errors(self, query_text, n_results=3):
        # Determine the number of results to fetch based on collection size
        try:
            count = self.collection.count()
            actual_n = min(n_results, count) if count > 0 else 0
            if actual_n == 0:
                print("Warning: Database is empty. No historical cases found.")
                return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
                
            results = self.collection.query(
                query_texts=[query_text],
                n_results=actual_n
            )
            return results
        except Exception as e:
            print(f"Warning: Failed to fetch from ChromaDB - {e}")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

if __name__ == "__main__":
    # Test ingestion
    db = ErrorDB()
    try:
        db.ingest_data("mock_data.json")
    except Exception as e:
        print("Error ingesting data:", e)
