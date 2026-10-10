import os
import sys
from src.extract import extract_content_from_pdf
from src.chunk import split_text_into_chunks
from src.embed import generate_embeddings
from src.retrieve import retrieve_top_chunks
from src.generate import generate_answer_from_chunks
from fastapi import FastAPI
from api.endpoints import router

app = FastAPI()
app.include_router(router)

def test():

    data_folder = "data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    pdf_name = sys.argv[1] if len(sys.argv) > 1 else None
    question = sys.argv[2] if len(sys.argv) > 2 else None
    if pdf_name:
        pdf_path = os.path.join(data_folder, pdf_name)
    else:
        print("Please provide a PDF file name as a command-line argument. Usage: python main.py <pdf_file_name> <question>")
        exit(1)

    if not question:
        print("Please provide a question as a command-line argument. Usage: python main.py <pdf_file_name> <question>")
        exit(1)

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

    generate_answer_from_chunks(retreived_chunks, question)

