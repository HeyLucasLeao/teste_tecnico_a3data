import streamlit as st
from src.utils.logging import logger
from time import time


def chat_interface():
    "Helper function to create the chat interface from Streamlit"
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me something about the epidemiological reports..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    start_time = time()
                    if st.session_state.assistant:
                        response = st.session_state.assistant.ask_question(prompt)
                        st.markdown(response)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )

                        logger.info(f"Question: {prompt} | Answer: {response}")
                        end_time = time()
                        logger.debug(
                            f"Processing time: {end_time - start_time:.2f} seconds"
                        )
                    else:
                        st.warning("Please upload the reports first.")
                except Exception as e:
                    print(e)
                    error_msg = (
                        "Sorry, an error occurred while processing your question."
                    )
                    st.error(error_msg)
                    logger.error(f"Error processing question '{prompt}': {str(e)}")
