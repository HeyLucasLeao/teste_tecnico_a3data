from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate
from src.preprocess import do_preprocessing
from langchain_community.vectorstores import FAISS


def setup_local_llm() -> HuggingFacePipeline:
    """
    Initialize and configure a local language model pipeline using HuggingFace.

    This function sets up Google's FLAN-T5 base model for text-to-text generation tasks.
    The model is optimized for instruction following and question answering.

    Returns:
        HuggingFacePipeline: Configured pipeline ready for language processing tasks

    Note:
        Uses 'google/flan-t5-base' model which is specifically designed for
        instruction following and has strong performance on QA tasks.
    """
    model_id = "google/flan-t5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

    pipe = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
    )

    return HuggingFacePipeline(pipeline=pipe)


class EpidemiologicalAssistant:
    """
    A specialized assistant for epidemiological data analysis and question answering.

    This class provides an interface for querying epidemiological data using
    a local language model combined with vector store retrieval for context-aware
    responses specific to European Union epidemiological standards.

    Attributes:
        llm: The language model pipeline for text generation
        vector_store: Vector database for document retrieval
        retrieval_chain: The configured retrieval and question answering chain
    """

    def __init__(self, vector_store):
        """
        Initialize the epidemiological assistant.

        Parameter:
            vector_store: pre-configured vector store for document retrieval.
        """
        self.llm = setup_local_llm()
        self.vector_store = vector_store
        self.qa_chain = None
        self.setup_assistant(vector_store)

    def setup_assistant(self, vector_store: FAISS) -> None:
        """
        Configure the assistant with a vector store for document retrieval.

        Sets up a retrieval-augmented generation chain that:
        1. Retrieves relevant documents using MMR (Maximal Marginal Relevance) search
        2. Combines retrieved context with the question
        3. Generates answers using the specialized epidemiological prompt template

        Parameter:
            vector_store: Configured FAISS vector store containing processed documents

        Note:
            Uses MMR search to balance relevance and diversity in retrieved documents
            (k=5 final results, fetch_k=10 initial candidates for diversity)
        """
        self.vector_store = vector_store

        custom_prompt = PromptTemplate(
            template="""
            As an EU epidemiological expert, analyze this data to answer the question precisely.

            DATA: {context}

            QUESTION: {input}
            """,
            input_variables=["context", "input"],
        )

        combine_docs_chain = create_stuff_documents_chain(self.llm, custom_prompt)

        self.retrieval_chain = create_retrieval_chain(
            self.vector_store.as_retriever(
                search_type="mmr", search_kwargs={"k": 5, "fetch_k": 10}
            ),
            combine_docs_chain,
        )

    def ask_question(self, question: str) -> str:
        """
        Ask a question and get an evidence-based epidemiological response.

        The process:
        1. Preprocesses the question text
        2. Retrieves relevant context documents from the vector store
        3. Generates an answer using the LLM with retrieved context
        4. Returns the synthesized response

        Parameter:
            question: The epidemiological question to be answered

        Returns:
            str: The generated answer based on retrieved documents and expert analysis
        """
        question = do_preprocessing(question)
        return self.retrieval_chain.invoke({"input": question}).get("answer")
