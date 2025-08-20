import streamlit as st
import os
from src.file_upload import file_uploader
from src.vector_store import load_documents, process_reports, vector_store_in_memory
from src.assistant import EpidemiologicalAssistant
from src.chat_interface import chat_interface
import tempfile


def main():
    st.set_page_config(
        page_title="Epidemiological Assistant", page_icon="🦠", layout="wide"
    )

    if "assistant" not in st.session_state:
        st.session_state.assistant = None
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.title("Epidemiological Assistant")

        uploaded_files = file_uploader()

    st.header("🦠 EU Epidemiological Reports Assistant")

    if uploaded_files and st.session_state.assistant is None:
        with st.spinner("Processing documents and preparing the assistant..."):
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    for uploaded_file in uploaded_files:
                        temp_path = os.path.join(temp_dir, uploaded_file.name)
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                    documents = load_documents(temp_dir)
                    processed_docs = process_reports(documents)
                    vector_store = vector_store_in_memory(processed_docs)

                    assistant = EpidemiologicalAssistant(vector_store)

                    st.session_state.vector_store = vector_store
                    st.session_state.assistant = assistant

                    st.success(
                        "Documents processed successfully! You can now ask questions."
                    )
            except Exception as e:
                st.error(f"Error processing documents: {str(e)}")

    chat_interface()


if __name__ == "__main__":
    main()
