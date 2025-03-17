from crewai.tools import tool
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_chroma.vectorstores import Chroma
from dotenv import load_dotenv
from chromadb import HttpClient
import os


load_dotenv()
HOST = os.environ['HOST']
embeddings = OllamaEmbeddings(model="bge-m3:latest", base_url=f"http://{HOST}:11434")
chroma_client = HttpClient(host=HOST, port=8000)

vector_store_retriever = Chroma(
    collection_name="red_hat",
    embedding_function=embeddings,
    client=chroma_client
).as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "lambda_mult": 0.5,
        "score_threshold": 0.8
    }
)


@tool
def retrieve_chunks(query: str) -> str:
    """Gets relevant chunks from chromadb based on passed string query"""

    docs = vector_store_retriever.invoke(query)
    docs_data = []
    for doc_data in docs:
        docs_data.append(doc_data.page_content)
    
    return "\n".join(docs_data)
