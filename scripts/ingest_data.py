import os
import argparse
from langchain_community.document_loaders import PyMuPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from app.rag_engine import rag_engine
from app.core.config import settings

def ingest_data(source_dir: str):
    """
    Ingests PDF and TXT data from the source directory into the ChromaDB vector store.
    """
    if not os.path.exists(source_dir):
        print(f"Error: Source directory {source_dir} does not exist.")
        return

    print(f"Loading documents from {source_dir}...")
    
    # Load PDFs
    pdf_loader = DirectoryLoader(source_dir, glob="**/*.pdf", loader_cls=PyMuPDFLoader)
    pdf_docs = pdf_loader.load()
    
    # Load TXTs
    # (Simplified for now)
    txt_loader = DirectoryLoader(source_dir, glob="**/*.txt")
    txt_docs = txt_loader.load()
    
    all_docs = pdf_docs + txt_docs
    
    if not all_docs:
        print("No documents found to ingest.")
        return

    print(f"Loaded {len(all_docs)} documents. Splitting into chunks...")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(all_docs)
    
    print(f"Created {len(chunks)} chunks. Adding to Vector Store at {settings.CHROMA_DB_DIRECTORY}...")
    
    # Add chunks to vectorstore
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=rag_engine.embeddings,
        persist_directory=settings.CHROMA_DB_DIRECTORY
    )
    
    print("Ingestion complete. Vector store updated successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest data into Astro-Oracle Vector Store")
    parser.add_argument("--source", type=str, default="./app/data", help="Directory containing source documents")
    
    args = parser.parse_args()
    ingest_data(args.source)
