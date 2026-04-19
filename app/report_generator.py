import os
import re

from langchain_openai import ChatOpenAI


def extract_scores(evaluation_text):
  scores = {}

  patterns = {
    "accuracy": r"Technical Accuracy: \s*(\d+)",
    "completeness": r"Completeness: \s*(\d+)",
    "clarity": r"Clarity: \s*(\d+)",
    "communication": r"Communication(?:Quality)?:\s*(\d+)",
  }

  for key, pattern in patterns.items():
    match = re.search(pattern, evaluation_text)
    if match:
      scores[key] = int(match.group(1))

  return scores


def generate_report(interview_memory):
  
  all_scores = {
    "accuracy": [],
    "completeness": [],
    "clarity": [],
    "communication": []
  }

  speech_data = []

  for entry in interview_memory:
    eval_text = entry.get("evaluation", "")
    scores = extract_scores(eval_text)

    for k in all_scores:
      if k in scores:
        all_scores[k].append(scores[k])
    
    if entry.get("speech_analysis"):
      speech_data.append(entry["speech_analysis"])
  
  avg_scores = {k: round(sum(v) / len(v) if v else 0) for k, v in all_scores.items()}

  overall = round(sum(avg_scores.values())/len(avg_scores), 2)

  confidence_levels = [s["confidence"] for s in speech_data]
  pace_levels = [s["pace"] for s in speech_data]
  pause_levels = [s["pauses"] for s in speech_data]

  def most_common(lst):
    return max(set(lst), key=lst.count) if lst else None
  
  speech_memory = {
    "confidence": most_common(confidence_levels),
    "pace": most_common(pace_levels),
    "pauses": most_common(pause_levels)
  }

  llm = ChatOpenAI(
    model = "gpt-4o-mini",
    temperature = 0.5,
    api_key = os.getenv("OPENAI_API_KEY")
  )

  history_text = "\n\n".join([f"Q: {entry['question']}\nA: {entry['answer']}\nEvaluation: {entry['evaluation']}" for entry in interview_memory])

  prompt = f"""
    You are an expert interview coach.

    Based on the following interview history, generate:

    1. Strengths
    2. Weaknesses
    3. Final Suggestions

    Interview History:
    {history_text}
  """

  summary = llm.invoke(prompt).content

  return{
    "overall": overall,
    "scores": avg_scores,
    "speech": speech_memory,
    "summary": summary
  }