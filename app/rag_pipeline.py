import os

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

load_dotenv()

def create_vector_store(chunks, path):

  embeddings = OpenAIEmbeddings(openai_api_key = os.getenv("OPENAI_API_KEY"))

  vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
  )

  vectorstore.save_local(path)

  return vectorstore