import pdfplumber
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter


load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

class LocalEmbeddingFunction:
    def __init__(self, model):
        self.model = model

    def __call__(self, input):
        if isinstance(input, str):
            input = [input]
        return self.model.encode(input).tolist()

    def name(self):
        return "local_sentence_transformer"


embedder = LocalEmbeddingFunction(model)

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=500
    )
    return splitter.split_text(text)

def embed_and_store(docs, pdf_name):
    client = chromadb.PersistentClient(path="db/")
    collection = client.get_or_create_collection(
        name="papers",
        embedding_function=embedder
    )

    for i, chunk in enumerate(docs):
        collection.add(
            documents=[chunk],
            ids=[f"{pdf_name}_{i}"]
        )

    print(f"Embedded {len(docs)} chunks from {pdf_name}")
