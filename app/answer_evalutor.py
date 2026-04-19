import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

def evaluate_answer(question, answer):

  llm = ChatOpenAI(
    model = "gpt-4o-mini",
    temperature = 0,
    api_key = os.getenv("OPENAI_API_KEY")
  )

  prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a senior technical interviewer evaluating candidate answers." ),
    ("human","""
      Evaluate the following answer to the given technical interview question. 

      Question:
      {question}

      Candidate's Answer:
      {answer}

      Score the answer based on the following criteria:
      1. Accuracy: Does the answer correctly address the question and demonstrate a clear understanding of the technical concepts involved?(0-10 points)

      2. Completeness: Does the answer cover all relevant aspects of the question, including edge cases and potential pitfalls?(0-10 points)

      3. Clarity: Is the answer well-structured and easy to understand, with clear explanations and logical flow?(0-10 points)

      4. Communication quality: Does the answer effectively communicate the candidate's thought process and reasoning?(0-10 points)

      Then provide:
      - A total score out of 40 points.
      - A brief explanation of the strengths and weaknesses of the answer.
      - Suggestions for improvement.

      Return the response in the following format:

      Technical Accuracy: X/10
      Completeness: X/10
      Clarity: X/10
      Communication Quality: X/10

      Total Score: X/40

      Strengths:
      - List the strengths of the answer here.

      Weaknesses:
      - List the weaknesses of the answer here.

      Suggestions for Improvement:
      - Provide specific suggestions for how the candidate can improve their answer.
    """)

  ])

  parser = StrOutputParser()

  chain = prompt | llm | parser

  result = chain.invoke({
    "question": question,
    "answer": answer
  })

  return result
  
