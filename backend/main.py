import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from fastapi import FastAPI

from backend.routes import interview, resume

app = FastAPI()

@app.get("/")
def root():
  return {"message": "Hello World"}

app.include_router(resume.router)
app.include_router(interview.router)