import os
import streamlit as st
import pandas as pd
import httpx
import requests
import certifi
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter

# -------------------------------
# SSL/Tiktoken Fixes
# -------------------------------
os.makedirs("./tiktoken_cache", exist_ok=True)
os.environ["TIKTOKEN_CACHE_DIR"] = "./tiktoken_cache"

# Monkey-patch requests globally to skip SSL verification (for Windows/corporate networks)
original_requests_get = requests.get
def unsafe_requests_get(*args, **kwargs):
    kwargs["verify"] = False
    return original_requests_get(*args, **kwargs)

requests.get = unsafe_requests_get

# -------------------------------
# LangChain / LLM Imports
# -------------------------------
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# -------------------------------
# LLM & Embeddings Setup
# -------------------------------
client = httpx.Client(verify=False)

llm = ChatOpenAI(
    base_url="https://genailab.tcs.in",
    model="azure/genailab-maas-gpt-4o",
    api_key="sk-If1PJAnGI-GpKJfyY4qVyw",
    http_client=client
)

embedding_model = OpenAIEmbeddings(
    base_url="https://genailab.tcs.in",
    model="azure/genailab-maas-text-embedding-3-large",
    api_key="sk-If1PJAnGI-GpKJfyY4qVyw",
    http_client=client
)

# -------------------------------
# Streamlit App Setup
# -------------------------------
st.set_page_config(page_title="AI Agent for IT Production RCA")
st.title("🧠 AI Agent for IT Production Incident Root Cause Analysis")

# Upload CSV logs
uploaded_file = st.file_uploader("📂 Upload System Logs (CSV)", type=["csv"])

if uploaded_file:
    # Read logs
    logs_df = pd.read_csv(uploaded_file)
    st.subheader("📋 Preview of Uploaded Logs")
    st.dataframe(logs_df.head())

    # Convert logs to text
    logs_text = "\n".join(
        [f"{row['timestamp']} [{row['level']}] {row['component']}: {row['message']}"
         for _, row in logs_df.iterrows()]
    )

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(logs_text)

    # Create embeddings & Chroma vector store
    with st.spinner("Indexing and analyzing logs..."):
        vectordb = Chroma.from_texts(chunks, embedding_model, persist_directory="./incident_index")
        vectordb.persist()

    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    # User query box
    st.subheader("💬 Ask a Question About the Incident")
    user_query = st.text_input("e.g., What caused the database outage?")

    if user_query:
        with st.spinner("Analyzing logs..."):
            result = rag_chain.invoke(f"""
            Analyze the following system logs and alerts to determine the root cause.
            Question: {user_query}
            Provide a probable cause, confidence level, and recommended actions.
            """)
        st.subheader("🧩 Root Cause Analysis Result:")
        st.write(result)

else:
    st.info("Please upload your `synthetic_logs.csv` file to begin analysis.")
