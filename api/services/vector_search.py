import os
import faiss
import pickle
from core.config import Config
from api.services.logging import get_logger
from openai import OpenAI
import numpy as np

client = OpenAI(api_key=Config.OPENAI_API_KEY)

logger = get_logger()

# FAISS index and document chunks are loaded globally for efficiency
index = None
chunks = None

def load_chunks_and_index():
    global chunks, index
    # Preprocess document and build index only if not already done
    if chunks is None or index is None:
        chunks = preprocess_document()
        index = build_index(chunks)

def get_embedding(text: str) -> list:
    embedding = client.embeddings.create(input=[text], model="text-embedding-ada-002")
    return embedding.data[0].embedding

def build_index(chunks):
    try:
        # Generate embeddings
        embeddings = []
        for chunk in chunks:
            embedding = get_embedding(chunk)
            embeddings.append(embedding)
        
        # Create FAISS index
        dimension = len(embeddings[0])
        new_index = faiss.IndexFlatL2(dimension)
        embedding_array = np.array(embeddings).astype("float32")
        new_index.add(embedding_array)

        # Save the index
        faiss.write_index(new_index, Config.FAISS_INDEX_PATH)
        logger.info(f"Successfully built index with {len(chunks)} chunks")
        return new_index
    except Exception as e:
        logger.error(f"Error building index: {e}")
        return None

def preprocess_document():
    try:
        with open(Config.DATA_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Split by parts/sections
        sections = []
        lines = content.split("\n")
        current_section = []
        
        for line in lines:
            if line.startswith("Part ") and "." in line[:10]:
                if current_section:
                    sections.append("\n".join(current_section))
                    current_section = []
            current_section.append(line)
        
        if current_section:
            sections.append("\n".join(current_section))
        
        # Further chunk each section if it's too long
        chunk_size = 1000  # Define chunk size
        chunk_overlap = 200  # Define overlap
        chunks = []
        for section in sections:
            if len(section) <= chunk_size:
                chunks.append(section)
            else:
                # Process into overlapping chunks
                for i in range(0, len(section), chunk_size - chunk_overlap):
                    chunk = section[i:i + chunk_size]
                    if len(chunk) >= 100:  # Only keep meaningful chunks
                        chunks.append(chunk)
        
        # Save the chunks to your data file
        with open(Config.DATA_PATH, "w") as f:
            for chunk in chunks:
                f.write(chunk + "\n")
                
        return chunks
    except Exception as e:
        logger.error(f"Error preprocessing document: {e}")
        return []

def query_faiss(query: str, top_k: int = 10) -> str:
    load_chunks_and_index()

    query_vector = np.array(get_embedding(query)).astype("float32")
    logger.info(f"query_vector : {query_vector}")

    distances, indices = index.search(np.array([query_vector]), top_k)
    logger.info(f"indices : {indices}")
    
    # Get chunks from indices
    context_chunks = [chunks[i] for i in indices[0]]  # Using chunks instead of 'documents'
    filtered_chunks = [chunk for chunk in context_chunks if len(chunk.strip()) > 100]
    
    # If filtering removed all chunks, fall back to original chunks
    if not filtered_chunks:
        filtered_chunks = context_chunks
    
    # Build context from filtered chunks
    context = "\n\n---\n\n".join(filtered_chunks[:5])  # Use top 5 most relevant chunks
    logger.info(f"context : {context}")

    return context
