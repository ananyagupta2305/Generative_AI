from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  # Use an appropriate model

def embed_text(texts):
    embeddings = model.encode(texts, convert_to_tensor=True)
    return embeddings