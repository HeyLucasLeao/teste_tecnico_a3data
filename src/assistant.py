from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate
from src.preprocess import do_preprocessing


def setup_local_llm():
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
    def __init__(self, vector_store=None):
        self.llm = setup_local_llm()
        self.vector_store = vector_store
        self.qa_chain = None

        if vector_store:
            self.setup_assistant(vector_store)

    def setup_assistant(self, vector_store):
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

    def ask_question(self, question):
        question = do_preprocessing(question)
        return self.retrieval_chain.invoke({"input": question}).get("answer")
