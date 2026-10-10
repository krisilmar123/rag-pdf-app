import pymupdf
import json

def extract_content_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    content = {}
    all_content = []
    i = 1
    for page in doc:
        text = page.get_text().encode("utf8") 
        content["page"] = i
        content["text"] = text.decode("utf8")
        all_content.append(content.copy())
        i += 1
    content_json = json.dumps(all_content, indent=4, ensure_ascii=False)
    return content_json

if __name__ == "__main__":
    pdf_path = "data/example.pdf"
    extracted_content = extract_content_from_pdf(pdf_path)
    print(extracted_content)