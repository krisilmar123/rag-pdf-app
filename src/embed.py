from sentence_transformers import SentenceTransformer




def generate_embeddings(chunks):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    for chunk in chunks:
        text = chunk["text"]
        embedding = model.encode(text)
        chunk["embedding"] = embedding.tolist() 
    return chunks