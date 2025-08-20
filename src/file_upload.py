import streamlit as st


def file_uploader():
    st.subheader("Report Upload")
    uploaded_files = st.file_uploader(
        "Select the PDF reports",
        type="pdf",
        accept_multiple_files=True,
        help="Upload epidemiological reports in PDF format",
    )

    if uploaded_files:
        st.info(f"{len(uploaded_files)} file(s) selected")
        for uploaded_file in uploaded_files:
            st.write(f"📄 {uploaded_file.name}")

    return uploaded_files
