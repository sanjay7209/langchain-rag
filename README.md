#  Retrieval-Augmented Generation (RAG) System using LangChain & OpenAI

This project demonstrates a **Retrieval-Augmented Generation (RAG)** architecture built with **LangChain**, **OpenAI Embeddings**, and **ChromaDB**.  
It focuses on creating a modular, scalable, and explainable pipeline for context-aware AI responses — ideal for enterprise knowledge management and intelligent assistants.

---

## Overview

This R&D implementation showcases how to:
- Ingest data (PDF)
- Split content into meaningful chunks for embedding
- Generate embeddings using OpenAI’s `text-embedding-3-large` model
- Store and retrieve vector data efficiently via **ChromaDB**
- Build a complete **RAG pipeline** that retrieves context and generates grounded answers using LangChain’s **ChatOpenAI**

---

## 🧠 Architecture

A[Data Sources: Text/PDF/JSON] --> B[Text Splitter]
B --> C[Embeddings (OpenAI)]
C --> D[Vector Store: ChromaDB]
E[User Query] --> F[Retriever]
D --> F
F --> G[Prompt Builder (RunnableLambda)]
G --> H[LLM - ChatOpenAI]
H --> I[Context-Aware Answer]


| Component             | Description                                                    |
| --------------------- | -------------------------------------------------------------- |
| **LangChain**         | Framework for chaining retrieval and LLM tasks                 |
| **OpenAI Embeddings** | Used for semantic vector representation                        |
| **ChromaDB**          | Vector database for document persistence and similarity search |
| **Python**            | Core programming language                                      |
| **RunnableLambda**    | Used to define modular and testable pipeline stages            |


🧩 Key Features
Multi-source ingestion: Supports text and PDF document loaders
Recursive splitting: Handles large documents efficiently using RecursiveCharacterTextSplitter
Semantic search: Finds contextually relevant data via vector similarity
Composability: Uses RunnableLambda for modular pipeline design
RAG-ready integration: Seamless connection between retrieval and LLM stages


Run RAG Pipeline - > python rag.py
Run LLM Query -> python langchain.py
