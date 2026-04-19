import os

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

def generate_questions(vectorstore_path):

  embeddings = OpenAIEmbeddings(openai_api_key = os.getenv("OPENAI_API_KEY"))

  vectorstore = FAISS.load_local(
    vectorstore_path,
    embeddings,
    allow_dangerous_deserialization=True
  )
  
  retriever = vectorstore.as_retriever(search_kwargs = {"k":5})

  docs = retriever.invoke("technical skills projects experience")

  context = "\n".join([doc.page_content for doc in docs])

  llm = ChatOpenAI(
    model = "gpt-4o-mini",
    temperature = 0.7,
    api_key = os.getenv("OPENAI_API_KEY")
  )

  prompt = ChatPromptTemplate.from_messages([
    ('system', "You are a senior technical interviewer"),
    ("human", """
    
      Based on the following resume context, generate 5 technical interview questions that are relevant to the candidate's experience and skills.
     
      Resume Context:
      {context}
     
      Instructions for question generation:
      1. Focus on the candidate's technical skills, projects, and experience mentioned in the resume context.
      2. Generate questions that assess the candidate's depth of knowledge and practical experience.
      3. Avoid generic questions that could apply to any candidate; tailor the questions to the specific information provided in the resume context.
      4. Ensure the questions are clear, concise, and unambiguous.
      5. Format the output as a numbered list of questions.
    """)
  ])

  parser = StrOutputParser()

  chain = prompt | llm | parser

  result = chain.invoke({
    "context": context
  })

  questions = []

  for line in result.split("\n"):
    if line.strip():
      q =line.split(".", 1)[-1].strip()
      questions.append(q)
  
  return questions
