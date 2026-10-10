import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api"

st.set_page_config(page_title="PDF Q&A", page_icon="📄")

st.title("PDF Question Answering")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# Question input
question = st.text_area("Your question", placeholder="Ask something about the PDF...")

if st.button("Ask", disabled=not uploaded_file or not question.strip()):
    with st.spinner("Processing..."):
        try:
            # 1. Upload PDF
            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
            }

            upload_response = requests.post(
                f"{API_URL}/documents",
                files=files,
                timeout=60
            )
            upload_response.raise_for_status()

            pdf_name = upload_response.json()["filename"]
            print(f"Uploaded PDF: {pdf_name}")
            print(f"Question: {question}")

            # 2. Ask question
            ask_response = requests.post(
                f"{API_URL}/ask",
                data={
                    "question": question,
                    "pdf_name": pdf_name
                },
                timeout=120
            )
            ask_response.raise_for_status()

            result = ask_response.json()
            #Structure is result = {"question": question, "answer": {"answer": answer, "sources": [{"page": page_number, "text": text}, ...]}}

            # 3. Display results
            st.subheader("Answer")
            st.write(result.get("answer", {}).get("answer", "No answer returned."))

            st.subheader("Sources")
            sources = result.get("answer", {}).get("sources", [])

            if sources:
                for source in sources:
                    st.write(f"**Page {source['page']}**: {source['text']}")
            else:
                st.write("No sources returned.")
        except requests.RequestException as e:
            st.error(f"API request failed: {e}")
        except (KeyError, ValueError) as e:
            st.error(f"Unexpected API response: {e}")