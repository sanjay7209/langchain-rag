from fastapi import FastAPI, Query
from pydantic import BaseModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

app = FastAPI()

class chatResponse(BaseModel):
    answer: str

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = Chroma(
    persist_directory="./chroma_db", embedding_function = embeddings
    )

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 8})

PROMPT = ChatPromptTemplate.from_messages([
    ('system',
     'You ara a helpful AI assistant. Answer ONLY with the context provided.'
     ' If you do not know the answer, say "I do not know."'),
     ('user',
      'Question: {question}\n\nContext:\n{context}\n\nAnswer:')
     ])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

retrieve_stage = RunnableLambda(
    lambda x: {
        "question": x["question"],
        "docs": retriever.invoke(x["question"])
    }
)

def _build_context(docs) -> str:
    parts = []
    for d in docs:
        meta = d.metadata or {}
        page = meta.get("page", "N/A")
        src = meta.get("source_file", meta.get("source", "N/A"))
        parts.append(f"[p.{page} {src}]\n{d.page_content}")
    return "\n\n".join(parts)

context_stage = RunnableLambda(
    lambda x: {
        "question": x["question"],
        "context": _build_context(x["docs"])
    }
)

# 3) Prompt -> LLM -> extract answer text
answer_stage = (
    PROMPT
    | llm
    | RunnableLambda(lambda m: {"answer": m.content})
)

chain = retrieve_stage | context_stage | answer_stage

@app.get("/ask", response_model=chatResponse)
def ask_question(q: str = Query(..., description="The question to ask the AI")):
    result = chain.invoke({"question": q})
    return chatResponse(answer=result["answer"])

