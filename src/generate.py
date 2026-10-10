from ollama import generate, chat
from pydantic import BaseModel

class Source(BaseModel):
    page: int
    text: str

class Answer(BaseModel):
    answer: str
    sources: list[Source]


def generate_answer_from_chunks(chunks, question):
    context = " ".join([f"Page {chunk['page']}: {chunk['text']}" for chunk in chunks])
    prompt = f"Answer the question based only on the context provided:\nContext: {context}\n\nQuestion: {question}\n\n If the answer is not contained within the context, respond only with the following text: 'Context does not contain the answer.' Include source page numbers in your answer as 'Source: <page_number>'."
    response = generate(model="llama3.2:latest", prompt=prompt, format=Answer.model_json_schema(),)
    answer = response['response']
    answer = Answer.model_validate_json(answer)
    print(f"Answer: {answer}")
    return answer