# 🧠 ResumeAI – AI Interview Coach

An intelligent AI-powered interview preparation system that generates resume-based interview questions, evaluates answers, analyzes speech, and provides a detailed performance report.

---

## 📌 Overview

**ResumeAI** simulates a real technical interview by combining:

* Retrieval-Augmented Generation (RAG)
* Large Language Models (LLMs)
* Speech Recognition (Whisper)
* Audio Signal Processing (Librosa)

It evaluates both:

* ✅ **What you say** (technical correctness)
* 🎙 **How you say it** (confidence, clarity, pace)

---

## 🚀 Features

### 🧠 Resume-Based Question Generation (RAG)

* Upload your resume (PDF)
* Extracts and chunks content using LangChain
* Stores embeddings in FAISS
* Generates **personalized technical questions**

---

### 💬 Adaptive Interview Flow

* Multi-question interview session
* AI-generated **follow-up questions**
* Context-aware questioning using backend session memory

---

### 🤖 Answer Evaluation (LLM)

Evaluates answers based on:

* Technical Accuracy
* Completeness
* Clarity
* Communication

Provides:

* Scores (out of 40)
* Strengths
* Weaknesses
* Improvement suggestions

---

### 🎤 Voice Input (Speech-to-Text)

* Record answers via microphone
* Converts speech → text using Whisper

---

### 🎙 Speech Analysis (Librosa)

Analyzes:

* ⏱ Duration
* ⚡ Confidence (energy)
* 🗣 Pace (fast / moderate / slow)
* ⏸ Pause detection

---

### 📊 Final Interview Report

Generates a comprehensive report including:

* Overall score
* Technical breakdown
* Speech summary
* AI-generated insights

---

## 🏗 Architecture

```
Resume PDF
   ↓
Text Extraction (PyPDF)
   ↓
Chunking (LangChain)
   ↓
Embeddings (OpenAI)
   ↓
Vector Store (FAISS)
   ↓
Retriever (RAG)
   ↓
Question Generator (LLM)
   ↓
User Answer (Text / Voice)
   ↓
Speech-to-Text (Whisper)
   ↓
Speech Analysis (Librosa)
   ↓
Answer Evaluation (LLM)
   ↓
MongoDB (Session Storage)
   ↓
Final Report Generation
```

---

## 🛠 Tech Stack

### 🔹 AI / ML

* LangChain
* OpenAI API (LLMs + Embeddings)
* FAISS (Vector Database)
* Whisper (Speech Recognition)
* Librosa (Audio Analysis)

### 🔹 Backend

* FastAPI
* MongoDB Atlas

### 🔹 Frontend

* Streamlit

### 🔹 Libraries

* NumPy, SciPy
* Transformers
* PyTorch
* PyPDF

---

## 📂 Project Structure

```
ResumeAI/
│
├── app/
│   ├── resume_processor.py
│   ├── rag_pipeline.py
│   ├── question_generator.py
│   ├── answer_evaluator.py
│   ├── followup_generator.py
│   ├── speech_to_text.py
│   ├── speech_analysis.py
│   ├── report_generator.py
│
├── backend/
│   ├── routes/
│   ├── db/
│
├── data/
│   ├── audio_answers/
│   ├── vectorstore/
│
├── main.py (Streamlit UI)
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/chiraggoyal-12/ResumeAI.git
cd ResumeAI
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Add Environment Variables

Create `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
MONGO_URI=your_mongodb_connection_string
```

---

### 5️⃣ Run Backend (FastAPI)

```bash
uvicorn main:app --reload
```

---

### 6️⃣ Run Frontend (Streamlit)

```bash
streamlit run main.py
```

---

## 📌 Usage

1. Upload your resume (PDF)
2. Start interview
3. Answer questions via:

   * Text input
   * 🎤 Voice recording
4. Get:

   * AI evaluation
   * Speech analysis
5. Complete interview → Generate final report

---

## 🚫 Important Notes

* `vectorstore/` and `data/` folders are **not included in repo**
* They are generated locally at runtime
* MongoDB Atlas is used for session persistence

---

## 💡 Key Highlights

* Built a **RAG-based interview system**
* Designed **REST APIs with FastAPI**
* Implemented **persistent sessions using MongoDB**
* Integrated **speech analysis + LLM evaluation**
* Created a **full-stack AI application**

---

## 🧠 Future Improvements

* Recommendation system (skill gap analysis)
* Deployment (Render / Streamlit Cloud)
* Enhanced UI/UX

---

## 👨‍💻 Author

**Chirag Goyal**

---

## ⭐ If you like this project, give it a star!
