import json

def split_text_into_chunks(json_content, chunk_size=1000):
    pages = json.loads(json_content)
    chunks = []

    for page in pages:
        text = page["text"]
        page_nr = page["page"]
        for i in range(0, len(text), chunk_size):
            chunk = {"text": text[i:i + chunk_size], "page": page_nr}
            chunks.append(chunk)
    return chunks