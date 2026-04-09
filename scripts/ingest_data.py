import os
import argparse
from langchain_community.document_loaders import PyMuPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from app.rag_engine import rag_engine
from app.core.config import settings

def ingest_data(source_dir: str):
    """
    Kaynak dizindeki PDF ve TXT verilerini ChromaDB vektör deposuna işler.
    """
    if not os.path.exists(source_dir):
        print(f"Hata: Kaynak dizini {source_dir} mevcut değil.")
        return

    print(f"Dokümanlar {source_dir} dizininden yükleniyor...")
    
    # PDF'leri Yükle
    pdf_loader = DirectoryLoader(source_dir, glob="**/*.pdf", loader_cls=PyMuPDFLoader)
    pdf_docs = pdf_loader.load()
    
    # TXT'leri Yükle
    txt_loader = DirectoryLoader(source_dir, glob="**/*.txt")
    txt_docs = txt_loader.load()
    
    all_docs = pdf_docs + txt_docs
    
    if not all_docs:
        print("İşlenecek doküman bulunamadı.")
        return

    print(f"{len(all_docs)} doküman yüklendi. Parçalara ayrılıyor...")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(all_docs)
    
    print(f"{len(chunks)} parça oluşturuldu. {settings.CHROMA_DB_DIRECTORY} adresindeki Vektör Deposuna ekleniyor...")
    
    # Parçaları vektör deposuna ekle
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=rag_engine.embeddings,
        persist_directory=settings.CHROMA_DB_DIRECTORY
    )
    
    print("Veri işleme tamamlandı. Vektör deposu başarıyla güncellendi.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Astro-Oracle Vektör Deposuna veri ekleme betiği")
    parser.add_argument("--source", type=str, default="./app/data", help="Kaynak dokümanları içeren dizin")
    
    args = parser.parse_args()
    ingest_data(args.source)
