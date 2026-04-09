import os
from typing import List, Optional
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from app.core.config import settings

class RAGEngine:
    def __init__(self):
        self.db_directory = settings.CHROMA_DB_DIRECTORY
        self.embeddings = self._get_embeddings()
        self.vectorstore = self._get_vectorstore()

    def _get_embeddings(self):
        if settings.OPENAI_API_KEY:
            return OpenAIEmbeddings(
                api_key=settings.OPENAI_API_KEY,
                model=settings.EMBEDDING_MODEL_NAME
            )
        elif settings.GOOGLE_API_KEY:
            return GoogleGenerativeAIEmbeddings(
                api_key=settings.GOOGLE_API_KEY,
                model="models/embedding-001"
            )
        else:
            # Fallback or error
            raise ValueError("No API Key provided for embeddings (OpenAI or Google required).")

    def _get_vectorstore(self):
        return Chroma(
            persist_directory=self.db_directory,
            embedding_function=self.embeddings
        )

    def search(self, query: str, k: int = 4) -> List[Document]:
        """Search for relevant documents in the vector store."""
        return self.vectorstore.similarity_search(query, k=k)

    def get_llm(self, temperature: float = 0.7):
        """Get the configured LLM instance."""
        if settings.OPENAI_API_KEY:
            return ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model="gpt-4-turbo-preview",
                temperature=temperature
            )
        elif settings.GOOGLE_API_KEY:
            return ChatGoogleGenerativeAI(
                api_key=settings.GOOGLE_API_KEY,
                model="gemini-pro",
                temperature=temperature
            )
        else:
            raise ValueError("No API Key provided for Chat LLM.")

rag_engine = RAGEngine()
