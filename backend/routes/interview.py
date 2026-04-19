import os
import re

from fastapi import APIRouter
from pydantic import BaseModel
from requests import session

from app.answer_evalutor import evaluate_answer
from app.followup_generator import generate_followup
from app.question_generator import generate_questions
from app.report_generator import generate_report
from backend.db.mongo import sessions_collection

router = APIRouter()

VECTOR_DIR = "vectorstore"

class StartInterviewRequest(BaseModel):
  session_id: str

@router.post("/start-interview")
async def start_interview(request: StartInterviewRequest):

  vectorstore_path = os.path.join(VECTOR_DIR, request.session_id)

  if not os.path.exists(vectorstore_path):
    return{"error": "Invalid session_id"}
  
  questions = generate_questions(vectorstore_path)

  sessions_collection.update_one(
    {"session_id": request.session_id},
    {"$set": {"questions": questions}}
  )

  return {
    "questions": questions
  }


class AnswerRequest(BaseModel):
  session_id: str
  question: str
  answer: str


@router.post("/submit-answer")
async def submit_answer(request: AnswerRequest):

  session = sessions_collection.find_one({"session_id": request.session_id})

  if not session:
    return {"error": "Invalid session_id"}
  history = session.get("interview_memory", [])

  evaluation = evaluate_answer(request.question, request.answer)

  followup = generate_followup(
    request.question,
    request.answer,
    history
  )

  memory_entry = {
    "question": request.question,
    "answer": request.answer,
    "evaluation": evaluation
  }
  
  sessions_collection.update_one(
    {"session_id": request.session_id},
    {"$push": {"interview_memory": memory_entry}}
  )


  return {
    "evaluation": evaluation,
    "followup_question": followup,
  }


class ReportRequest(BaseModel):
  session_id: str

@router.post("/report")
async def generate_final_report(request: ReportRequest):
  session = sessions_collection.find_one({"session_id": request.session_id})

  if not session:
    return {"error": "Invalid session_id"}
  
  history = session.get("interview_memory", [])

  report = generate_report(history)
  return {"report": report}