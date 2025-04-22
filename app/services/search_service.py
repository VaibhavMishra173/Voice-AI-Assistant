import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel
from app.config import Config

# Load model
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def embed_text(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings.numpy()

def search_knowledge_base(query):
    index = faiss.read_index(Config.FAISS_INDEX_PATH)
    vector = embed_text(query)
    D, I = index.search(vector, k=5)
    with open(Config.DATA_PATH, 'r') as f:
        lines = f.readlines()
    return [lines[i] for i in I[0] if i < len(lines)]

