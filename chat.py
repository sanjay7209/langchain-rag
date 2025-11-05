# chat.py

# ---- Imports (PEP 8: imports first; E402-safe) ------------------------------
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


# ---- Configuration -----------------------------------------------------------
def configure_env() -> None:
    """Load .env and sync a few keys into os.environ (assignment, not compare)."""
    load_dotenv()

    # Only set if present; leave unset otherwise.
    for key in (
        "OPENAI_API_KEY",
        "LANGCHAIN_API_KEY",
        "LANGCHAIN_TRACING_V2",
        "LANGCHAIN_TRACING_PROJECT",
    ):
        val = os.getenv(key)
        if val is not None:
            os.environ[key] = val  # <- assignment, not '=='

    # Optional: normalize LANGCHAIN_TRACING_V2 to 'true'/'false' strings
    if os.environ.get("LANGCHAIN_TRACING_V2") in {"1", "true", "True"}:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"


# ---- Index building ----------------------------------------------------------
def build_index(
    pdf_path: str = "DATA.pdf",
    chroma_dir: str = "./chroma_db",
    chunk_size: int = 1000,
    chunk_overlap: int = 0,
) -> None:
    """Load a PDF, split, embed, and persist a Chroma collection."""
    configure_env()

    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path.resolve()}")

    loader = PyPDFLoader(str(path))
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    final_docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    db = Chroma.from_documents(
        final_docs,
        embedding=embeddings,
        persist_directory=chroma_dir,
        collection_metadata={"hnsw:space": "cosine"},
    )
    db.persist()


# ---- CLI entrypoint ----------------------------------------------------------
if __name__ == "__main__":
    build_index()
