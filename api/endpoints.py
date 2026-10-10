from fastapi import FastAPI, File, UploadFile, APIRouter, Form
import os
from pathlib import Path

router = APIRouter(prefix="/api")

@router.post("/documents")
async def upload_document(file: UploadFile = File(...)):

    APP_DIR = Path(__file__).resolve().parent.parent
    data_folder = APP_DIR / "data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    
    file_path = data_folder / file.filename

    if os.path.exists(file_path):
        return {"filename": file.filename, "message": "File already exists."}
    
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    return {"filename": file.filename, "message": "File uploaded successfully."}

@router.post("/ask")
async def ask_question(question: str = Form(...), pdf_name: str = Form(...)):
    from src.extract import extract_content_from_pdf
    from src.chunk import split_text_into_chunks
    from src.embed import generate_embeddings
    from src.retrieve import retrieve_top_chunks
    from src.generate import generate_answer_from_chunks

    APP_DIR = Path(__file__).resolve().parent.parent

    data_folder = APP_DIR / "data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    if pdf_name:
        pdf_path = data_folder / pdf_name
        if not os.path.exists(pdf_path):
            return {"error": "PDF file not found."}

    extracted_text = extract_content_from_pdf(pdf_path)
    chunks = split_text_into_chunks(extracted_text)
    chunks_with_embeddings = generate_embeddings(chunks)
    retreived_chunks = retrieve_top_chunks(chunks_with_embeddings, question)

    print(f"Question: {question}")
    print("Top relevant chunks:")
    for chunk in retreived_chunks:
        print(f"Page {chunk['page']}")
        print(f"Text: {chunk['text']}")
        print(" --- --- ")

    answer = generate_answer_from_chunks(retreived_chunks, question) 
    return {"question": question, "answer": answer}