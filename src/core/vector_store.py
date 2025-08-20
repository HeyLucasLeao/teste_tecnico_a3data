import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import TokenTextSplitter
from .preprocess import do_preprocessing
from typing import List
from langchain_core.documents import Document


def load_documents(directory_path: str) -> List[Document]:
    """
    Load and preprocess PDF documents from a directory.

    Parameter:
        directory_path: Path to the directory containing PDF files

    Returns:
        List of preprocessed Document objects

    Raises:
        FileNotFoundError: If the directory doesn't exist
        Exception: If PDF loading fails for any file
    """
    files = os.listdir(directory_path)
    loaders = [PyPDFLoader(os.path.join(directory_path, f)) for f in files]
    documents = []
    for loader in loaders:
        loaded_docs = loader.load()
        for doc in loaded_docs:
            doc.page_content = do_preprocessing(doc.page_content)
        documents.extend(loaded_docs)

    return documents


def process_reports(documents: List[Document]) -> List[Document]:
    """
    Split documents into smaller chunks using token-based splitting.

    Parameter:
        documents: List of Document objects to be processed

    Returns:
        List of Document objects split into smaller chunks

    Note:
        Uses chunk size of 400 tokens with 100 token overlap
    """
    text_splitter = TokenTextSplitter(
        chunk_size=400, chunk_overlap=100, encoding_name="cl100k_base"
    )
    return text_splitter.split_documents(documents)


def vector_store_in_memory(documents: List[Document]) -> FAISS:
    """
    Create an in-memory vector store from documents using HuggingFace embeddings.

    Args:
        documents: List of Document objects to be vectorized

    Returns:
        FAISS vector store containing the document embeddings

    Note:
        Uses 'BAAI/bge-small-en-v1.5' model with CPU device and normalized embeddings
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={"device": "cpu"},
        encode_kwargs={
            "normalize_embeddings": True,
            "batch_size": 32,
        },
    )

    vector_store = FAISS.from_documents(
        documents,
        embeddings,
        distance_strategy="COSINE",
    )

    return vector_store
