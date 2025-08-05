import chromadb
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from datetime import datetime
import uuid

class MemoryEngine:
    def __init__(self, collection_name="hiro_memory"):
        # Connect to local ChromaDB
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name=collection_name)

        # Sentence embedding model (tiny but good)
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        # Emotion classifier (offline-capable)
        self.emotion_classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=1
        )

    def _embed(self, text):
        return self.embedder.encode([text])[0].tolist()

    def _get_emotion(self, text):
        result = self.emotion_classifier(text)
        return result[0][0]['label']

    def add_memory(self, text, people=None, themes=None, timestamp=None):
        if not timestamp:
            timestamp = datetime.now().isoformat()
        if people is None:
            people = []
        if themes is None:
            themes = []

        memory_id = str(uuid.uuid4())
        embedding = self._embed(text)
        emotion = self._get_emotion(text)

        self.collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[{
                "timestamp": timestamp,
                "people": people,
                "themes": themes,
                "emotion": emotion
            }],
            ids=[memory_id]
        )

        return memory_id

    def search_memory(self, query, top_k=5):
        embedding = self._embed(query)
        results = self.collection.query(query_embeddings=[embedding], n_results=top_k)
        return results

    def forget(self, keyword):
        results = self.search_memory(keyword, top_k=50)
        ids_to_delete = results.get("ids", [[]])[0]
        if ids_to_delete:
            self.collection.delete(ids=ids_to_delete)