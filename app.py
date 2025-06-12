import streamlit as st
from embedder import extract_text_from_pdf, split_text, embed_and_store
from retriever import retrieve_relevant_chunks
from generator import generate_answer
import os

st.set_page_config(page_title="Academic Research Assistant", layout="wide")
st.title("Academic Research Assistant")

st.sidebar.header("Upload PDF and Ask")

# Step 1: Upload PDF
pdf_file = st.sidebar.file_uploader("Upload Research Paper", type=["pdf"])
if pdf_file:
    pdf_path = f"data/{pdf_file.name}"
    with open(pdf_path, "wb") as f:
        f.write(pdf_file.read())
    st.sidebar.success(f"Uploaded: {pdf_file.name}")

    if st.sidebar.button("Process PDF"):
        with st.spinner("Extracting and embedding..."):
            text = extract_text_from_pdf(pdf_path)
            chunks = split_text(text)
            embed_and_store(chunks, pdf_name=os.path.splitext(pdf_file.name)[0])
        st.sidebar.success("PDF processed and embedded!")

# Step 2: Ask a Question
st.subheader("Ask a question about your uploaded paper:")
query = st.text_input("Enter your question here")

if st.button("Get Answer") and query:
    with st.spinner("Thinking..."):
        context = retrieve_relevant_chunks(query)
        answer = generate_answer(context, query)
        st.markdown("### Answer:")
        st.write(answer)
