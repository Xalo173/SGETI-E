from __future__ import annotations

from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings


class KnowledgeBase:
    def __init__(self) -> None:
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.persist_directory = settings.chroma_persist_dir
        self.vectorstore = Chroma(
            collection_name="auditai-standards",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory,
        )

    def ensure_seeded(self) -> None:
        # Seed the knowledge base only once so repeated starts do not duplicate chunks.
        if self.vectorstore._collection.count() > 0:
            return

        knowledge_dir = Path(__file__).resolve().parents[2] / "data" / "knowledge"
        splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120)
        documents = []
        for file_path in knowledge_dir.glob("*.md"):
            loader = TextLoader(str(file_path), encoding="utf-8")
            documents.extend(loader.load())

        if not documents:
            return

        chunks = splitter.split_documents(documents)
        self.vectorstore.add_documents(chunks)

    def get_retriever(self):
        self.ensure_seeded()
        return self.vectorstore.as_retriever(search_kwargs={"k": 4})


knowledge_base = KnowledgeBase()
