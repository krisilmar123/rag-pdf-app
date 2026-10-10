# rag-pdf-app
RAG app for asking questions about an uploaded PDF file. Uses FastAPI for backend endpoints. Streamlit for frontend.

MiniLM-L6-v2 is used for embeddings. Link: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2


# How to run locally

Make sure you are in project root before proceeding.

## Python dependencies

Install all necessary packages

```
pip install -r requirements.txt
```

## Download local model from Ollama

Llama 3.2 model was used for testing. Can be changed in src/generate.py.

```
ollama pull llama3.2
```

## Run backend api (FastAPI)

```
uv run fastapi dev --entrypoint main:app
```

## Run frontend

```
streamlit run frontend\front.py
```

# API endpoints

## POST /api/documents

### For uploading PDF file

Request:
```
{
    "file": File
}
```

Response:
```
{
    "filename": str.
    "message": str
}
```

## POST /api/ask

### For asking question about file

Request:
```
{
    "question": str,
    "pdf_name": str
}
```

Response:
```
{
    "question": str,
    "answer": {
                "answer": str
                "sources": [
                    {
                        "page": int,
                        "text": str
                    }
                ]
            }
                
}
```