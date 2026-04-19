import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.makedirs("data/audio_answers", exist_ok=True)

import requests
import streamlit as st
from dotenv import load_dotenv
from streamlit_mic_recorder import mic_recorder

from app.speech_analysis import analyze_speech
from app.speech_to_text import transcribe_audio

load_dotenv()

BASE_URL = "http://localhost:8000"

st.title("ResumeAI - Interview Preparation Tool")

if "questions" not in st.session_state:
  st.session_state.questions = []

if "current_q" not in st.session_state:
  st.session_state.current_q = 0

MAX_FOLLOWUPS = 2

if "followup_count" not in st.session_state:
  st.session_state.followup_count = 0

if "current_question" not in st.session_state:
  st.session_state.current_question = None

if "evaluation" not in st.session_state:
  st.session_state.evaluation = None

if "transcribed_text" not in st.session_state:
  st.session_state.transcribed_text = ""

if "session_id" not in st.session_state:
  st.session_state.session_id = None

if "followup" not in st.session_state:
  st.session_state.followup = None

if "file_name" not in st.session_state:
  st.session_state.file_name = None

if "audio_path" not in st.session_state:
    st.session_state.audio_path = None

if st.session_state.session_id:
  if st.button("Start New Interview"):
    for key in list(st.session_state.keys()):
      del st.session_state[key]
    st.rerun()
    

# 🔹 PHASE 1: Upload
if st.session_state.session_id is None:

  st.write("Upload your resume to generate AI interview questions.")

  uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

  st.session_state.file_name = uploaded_file.name if uploaded_file else "No file uploaded"

  if uploaded_file and st.button("Upload Resume"):
    with st.spinner("Uploading resume..."):
      response = requests.post(
        f"{BASE_URL}/upload-resume",
        files={"file": uploaded_file}
      )

      data = response.json()
      st.session_state.session_id = data["session_id"]

      st.success("Resume uploaded successfully!")
      st.rerun()

# 🔹 PHASE 2: Start Interview
elif not st.session_state.questions:

  st.subheader("Ready to start your interview practice?")

  st.write("Uploaded Resume: ", st.session_state.file_name)

  if st.button("Start Interview"):
    response = requests.post(
      f"{BASE_URL}/start-interview",
      json={"session_id": st.session_state.session_id}
    )

    data = response.json()
    st.session_state.questions = data.get("questions", [])
    st.session_state.current_q = 0
    st.rerun()
        

if st.session_state.questions:

  q_index = st.session_state.current_q

  st.progress((q_index) / len(st.session_state.questions))

  if q_index < len(st.session_state.questions):

    if st.session_state.current_question is None:
      st.session_state.current_question = st.session_state.questions[q_index]

    question = st.session_state.current_question

    st.subheader(f"Question {q_index + 1}")
    if st.session_state.followup_count > 0:
      st.subheader(f"Follow-up {st.session_state.followup_count}")
    
    st.write(question)

    st.markdown("Record your Answer(optional)")

    audio = mic_recorder(
      start_prompt="Start Recording",
      stop_prompt="Stop Recording",
      just_once = True,
      key = f"mic_{q_index}_{st.session_state.followup_count}"
    )

    if audio:

      audio_bytes = audio["bytes"]

      audio_path = f"data/audio_answers/audio_{q_index}_{st.session_state.followup_count}.wav"

      with open(audio_path, "wb") as f:
        f.write(audio_bytes)
      
      st.session_state.audio_path = audio_path

      with st.spinner("Transcribing audio..."):
        st.session_state.transcribed_text = transcribe_audio(audio_path)
    if st.session_state.transcribed_text:
      st.subheader("Transcribed Answer")
      st.write(st.session_state.transcribed_text)

    analysis = None
    if st.session_state.audio_path:

      analysis = analyze_speech(st.session_state.audio_path) 

      st.subheader("Speech Analysis")

      st.write(f"Duration: {analysis['duration']} seconds")
      st.write(f"Confidence: {analysis['confidence']}")
      st.write(f"Pace: {analysis['pace']}")
      st.write(f"Pauses: {analysis['pauses']}")

    key_name = f"typed_answer_{q_index}_{st.session_state.followup_count}"

    if not st.session_state.transcribed_text:
      typed_answer = st.text_area("Or type your answer", key = key_name)
    else:
      typed_answer = ""

    answer = st.session_state.transcribed_text if st.session_state.transcribed_text else typed_answer

    #Evaluate button
    if st.session_state.evaluation is None:

      if st.button("Evaluate Answer"):

        if not answer.strip():
          st.warning("Please provide an answer to evaluate.")
        else:
          with st.spinner("Evaluating..."):
            response = requests.post(
              f"{BASE_URL}/submit-answer",
              json = {
                "session_id": st.session_state.session_id,
                "question": question,
                "answer": answer
              }
            )

            data = response.json()

            st.session_state.evaluation = data["evaluation"]
            st.session_state.followup = data["followup_question"]
            st.session_state.transcribed_text = ""
          
    #Show Evaluation
    if st.session_state.evaluation:
      st.subheader("Feedback")
      st.write(st.session_state.evaluation)

      #Generate Follow-up Question
      if st.session_state.followup_count < MAX_FOLLOWUPS:

        if st.button("Next"):
          st.session_state.current_question = st.session_state.followup
          st.session_state.followup_count += 1
          st.session_state.evaluation = None
          st.session_state.transcribed_text = ""
          st.session_state.audio_path = None
          st.session_state.followup = None
          st.rerun()
        
      else:
        if st.button("Next Question"):
          st.session_state.current_q += 1
          st.session_state.followup_count = 0
          st.session_state.current_question = None
          st.session_state.evaluation = None
          st.session_state.transcribed_text = ""
          st.session_state.audio_path = None
          st.rerun()
  else:
    st.success("Interview Completed!")

    if st.button("Generate Final Report"):
      response = requests.post(f"{BASE_URL}/report",             json = {"session_id": st.session_state.session_id})

      report = response.json()

      report_data = response.json()["report"]

      st.header("Final Report")

      st.subheader("Overall Score")
      st.metric("Overall Score", f"{report_data['overall']}/10")

      st.subheader("Technical Scores")
      st.write(report_data["scores"])

      st.subheader("Speech Analysis")
      st.write(report_data["speech"])

      st.subheader("Insights")
      st.write(report_data["summary"])










