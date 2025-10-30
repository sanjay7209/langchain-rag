import os
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] == os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] == os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] == os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_TRACING_PROJECT"] == os.getenv("LANGCHAIN_TRACING_PROJECT")

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


loader = PyPDFLoader("DATA.pdf")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, 
                                               chunk_overlap=0,
                                               separators=["\n\n", "\n", ".", " ", ""]
                                               )
final_docs = text_splitter.split_documents(documents)

CHROMA_DIR = "./chroma_db"
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
db = Chroma.from_documents(
    final_docs, embedding=embeddings,
    persist_directory=CHROMA_DIR,
    collection_metadata={"hnsw:space": "cosine"},
)
db.persist()