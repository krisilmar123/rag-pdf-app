import torch.nn as nn
from .embed import generate_embeddings
from sentence_transformers import SentenceTransformer
import torch
import numpy as np

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')



def retrieve_top_chunks(chunks_with_embeddings, question, top_n=3):
    question_embedding = model.encode([question])
    embedding_tensor = torch.from_numpy(question_embedding)

    similarity_scores = []
    for chunk in chunks_with_embeddings:
        cos = nn.CosineSimilarity(dim=0, eps=1e-6)
        score = cos(embedding_tensor[0], torch.from_numpy(np.array(chunk["embedding"]))[0])
        similarity_scores.append((chunk, score))

    sorted_chunks = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    return [chunk for chunk, score in sorted_chunks[:top_n]]