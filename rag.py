import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()
from langchain.embeddings import OpenAIEmbeddings
os.environ["ANONYMIZED_TELEMETRY"] = "False" 

# 1. Data Ingestion
from langchain_community.document_loaders import TextLoader
loader = TextLoader("sanjay.txt")
documents = loader.load()

from langchain_community.document_loaders import PyPDFLoader
ploader = PyPDFLoader("rl_1725739097.pdf")
pdocuments = ploader.load()

# 2. Text Splitting
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
final_docs = text_splitter.split_documents(pdocuments)

# splitting JSON data

json_data = requests.get("https://api.smith.langchain.com/openapi.json").json()
from langchain_text_splitters import RecursiveJsonSplitter
json_splitter = RecursiveJsonSplitter(max_chunk_size=300)
json_chunks = json_splitter.split_json(json_data)

docs = json_splitter.create_documents(texts = [json_data])

for doc in docs[:3]:
    print(doc)

# 3. Embedding
os.environ["OPENAI_API_KEY"] == os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(model = "text-embedding-3-large")

text = "This is a sample text to be embedded."
query_result = embeddings.embed_query(text)
print(query_result)

# 4. vector Embedding and vector store
from langchain_community.vectorstores import Chroma
from chromadb.config import Settings
PERSIST_DIR = "./chroma_db"
db = Chroma.from_documents(final_docs, embedding = embeddings,
                           persist_directory=PERSIST_DIR,
    client_settings=Settings(anonymized_telemetry=False),)
db

# 5. similarity search

query = "What are the tools useful for data analysis?"

results = db.similarity_search(query)