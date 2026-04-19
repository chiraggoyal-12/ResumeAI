import os
import uuid
from json import load

from fastapi import APIRouter, File, UploadFile

from app.rag_pipeline import create_vector_store
from app.resume_processor import load_resume
from backend.db.mongo import sessions_collection

router = APIRouter()

UPLOAD_DIR = "data/resumes"
VECTOR_DIR = "vectorstore"

os.makedirs(UPLOAD_DIR, exist_ok = True)
os.makedirs(VECTOR_DIR, exist_ok = True)

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

  session_id = str(uuid.uuid4())

  file_path = os.path.join(UPLOAD_DIR, f"{session_id}.pdf")

  with open(file_path, "wb") as f:
    f.write(await file.read())

  chunks = load_resume(file_path)

  vectorstore_path = os.path.join(VECTOR_DIR, session_id)
  create_vector_store(chunks, vectorstore_path)

  sessions_collection.insert_one({
    "session_id": session_id,
    "vectorstore_path": vectorstore_path,
    "questions": [],
    "interview_memory": []
  })

  return {
    "message": "Resume processed successfully",
    "session_id": session_id,
    "vectorstore_path": vectorstore_path
  }