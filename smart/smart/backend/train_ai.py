import argparse
import os
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_DIR = Path("backend/data/textbooks")
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "backend/vector_store/faiss_index")
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "huggingface").lower()


def load_documents(data_dir: Path) -> List:
    documents = []
    for file_path in data_dir.rglob("*"):
        if file_path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(file_path))
            documents.extend(loader.load())
        elif file_path.suffix.lower() in {".txt", ".md"}:
            loader = TextLoader(str(file_path), encoding="utf-8")
            documents.extend(loader.load())
    return documents


def build_embeddings():
    if EMBEDDING_PROVIDER == "openai":
        return OpenAIEmbeddings(model="text-embedding-3-small")
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build curriculum vector store for Smart Shiksha")
    parser.add_argument("--data-dir", default=str(DATA_DIR), help="Directory containing PDFs/TXT")
    parser.add_argument("--chunk-size", type=int, default=500)
    parser.add_argument("--chunk-overlap", type=int, default=100)
    args = parser.parse_args()

    source_dir = Path(args.data_dir)
    if not source_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {source_dir}")

    docs = load_documents(source_dir)
    if not docs:
        raise RuntimeError("No PDF/TXT/MD documents found for ingestion.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    split_docs = splitter.split_documents(docs)

    embeddings = build_embeddings()
    store = FAISS.from_documents(split_docs, embeddings)

    target = Path(VECTOR_STORE_PATH)
    target.parent.mkdir(parents=True, exist_ok=True)
    store.save_local(str(target))

    print(f"Ingested documents: {len(docs)}")
    print(f"Generated chunks: {len(split_docs)}")
    print(f"Vector index saved to: {target}")


if __name__ == "__main__":
    main()
