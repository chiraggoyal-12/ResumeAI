import os

from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from torch.special import entr

load_dotenv()

def generate_followup(question, answer, history):

  llm = ChatOpenAI(
    model = "gpt-4o-mini",
    temperature = 0.7,
    api_key = os.getenv("OPENAI_API_KEY")
  )

  conversation = ""

  for entry in history:
    conversation += f"Q: {entry['question']}\nA: {entry['answer']}\n"

  conversation += f"Q: {question}\nA: {answer}\n"

  prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a technical interviewer conducting a deep interview."),
    ("human", """
      Continue the interview based on the conversation.
      {conversation}

      Ask ONE follow-up question that:
      - digs deeper into the candidate's knowledge
      - avoids repeating previous questions
      - builds on prior discussion

      Return only the question.
    """)
  ])

  parser = StrOutputParser()

  chain = prompt | llm | parser


  result = chain.invoke({
    "conversation": conversation
  })

  return result