import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import TokenTextSplitter
from src.preprocess import do_preprocessing


def load_documents(directory_path):
    files = os.listdir(directory_path)
    loaders = [PyPDFLoader(os.path.join(directory_path, f)) for f in files]
    documents = []
    for loader in loaders:
        loaded_docs = loader.load()
        for doc in loaded_docs:
            doc.page_content = do_preprocessing(doc.page_content)
        documents.extend(loaded_docs)

    return documents


def process_reports(documents):
    text_splitter = TokenTextSplitter(
        chunk_size=400, chunk_overlap=100, encoding_name="cl100k_base"
    )
    return text_splitter.split_documents(documents)


def vector_store_in_memory(documents):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-distilroberta-v1",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vector_store = FAISS.from_documents(documents, embeddings)

    return vector_store
