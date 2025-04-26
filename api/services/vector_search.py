import os
import faiss
import pickle
from core.config import Config
from api.services.logging import get_logger
from openai import OpenAI
import numpy as np

client = OpenAI(api_key=Config.OPENAI_API_KEY)

logger = get_logger()

# Global variables
# Load FAISS index and docs
index = faiss.read_index(Config.FAISS_INDEX_PATH)
with open(Config.DATA_PATH, "r") as f:
    documents = f.readlines()

def get_embedding(text: str) -> list:
    embedding = client.embeddings.create(input=[text], model="text-embedding-ada-002")
    return embedding.data[0].embedding

def query_faiss(query: str, top_k: int = 50) -> str:
    query_vector = np.array(get_embedding(query)).astype("float32")
    _, indices = index.search(np.array([query_vector]), top_k)
    context = "\n".join([documents[i] for i in indices[0]])

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use the context provided."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
    ]

    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    return response.choices[0].message.content
