from langchain import text_splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


def load_resume(file_path):

  loader = PyPDFLoader(file_path)
  documents = loader.load()

  text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

  chunks = text_splitter.split_documents(documents)
  return chunks