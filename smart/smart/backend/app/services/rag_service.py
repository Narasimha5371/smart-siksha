import os
from typing import List

from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "backend/vector_store/faiss_index")
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "huggingface").lower()
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = (
    "You are an empathetic tutor. Answer only using the provided context. "
    "If the student answers incorrectly, explain why using the Socratic method "
    "(ask guiding questions). If context is missing, say you do not have enough "
    "curriculum context to answer."
)


def _build_embeddings():
    if EMBEDDING_PROVIDER == "openai":
        return OpenAIEmbeddings(model="text-embedding-3-small")
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def _load_vector_store() -> FAISS:
    embeddings = _build_embeddings()
    if not os.path.exists(VECTOR_STORE_PATH):
        raise RuntimeError(
            f"Vector store not found at '{VECTOR_STORE_PATH}'. Run backend/train_ai.py first."
        )
    return FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )


def retrieve_context(query: str, k: int = 4) -> List[str]:
    store = _load_vector_store()
    docs = store.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]


def get_tutor_response(user_query: str) -> str:
    context_chunks = retrieve_context(user_query)
    context = "\n\n".join(context_chunks)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            (
                "human",
                "Use only this context:\n{context}\n\nStudent question: {question}",
            ),
        ]
    )

    llm = ChatOpenAI(model=LLM_MODEL, temperature=0.2)
    response = llm.invoke(prompt.format_messages(context=context, question=user_query))
    return response.content


def get_tutor_response_with_context(user_query: str) -> tuple[str, List[str]]:
    context_chunks = retrieve_context(user_query)
    context = "\n\n".join(context_chunks)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            (
                "human",
                "Use only this context:\n{context}\n\nStudent question: {question}",
            ),
        ]
    )

    llm = ChatOpenAI(model=LLM_MODEL, temperature=0.2)
    response = llm.invoke(prompt.format_messages(context=context, question=user_query))
    return response.content, context_chunks
