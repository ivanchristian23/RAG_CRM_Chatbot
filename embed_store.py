from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

model = SentenceTransformer('all-MiniLM-L6-v2')

def build_vector_store(texts, db_path="faiss_index"):
    if not texts:
        print("[WARNING] No texts provided to embed.")
        return

    embeddings = model.encode(texts)
    
    if len(embeddings) == 0:
        print("[WARNING] No embeddings generated.")
        return

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    
    with open(f"{db_path}.pkl", "wb") as f:
        pickle.dump((texts, index), f)


def load_vector_store(db_path="faiss_index"):
    with open(f"{db_path}.pkl", "rb") as f:
        return pickle.load(f)

def search(query, k=10):
    texts, index = load_vector_store()
    query_vec = model.encode([query])
    _, I = index.search(np.array(query_vec), k)
    return [texts[i] for i in I[0]]
