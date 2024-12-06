# utils/retrieval.py
import numpy as np
import faiss

def retrieve_relevant_content(embeddings, query_embedding):
    # Assuming embeddings is a 2D numpy array
    index = faiss.IndexFlatL2(embeddings.shape[1])  # L2 distance
    index.add(embeddings.numpy())  # Add the document embeddings to the index

    D, I = index.search(query_embedding.numpy(), k=5)  # Search for the top 5 relevant documents
    return I  # Returning indices of the retrieved documents
