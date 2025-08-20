import streamlit as st


def chat_interface():
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
                    if st.session_state.assistant:
                        response = st.session_state.assistant.ask_question(prompt)
                        print(response)
                        st.markdown(response)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )

                        ## Log interaction
                        # logger.info(f"Question: {prompt} | Answer: {response}")
                    else:
                        st.warning("Please upload the reports first.")
                except Exception as e:
                    print(e)
                    error_msg = (
                        "Sorry, an error occurred while processing your question."
                    )
                    st.error(error_msg)
                    # logger.error(f"Error processing question '{prompt}': {str(e)}")
