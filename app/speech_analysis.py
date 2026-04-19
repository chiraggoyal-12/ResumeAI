import librosa
import numpy as np


def analyze_speech(file_path):
  y, sr = librosa.load(file_path)

  duration = librosa.get_duration(y=y, sr=sr)

  #Energy(confidence proxy)
  rms = librosa.feature.rms(y=y)[0]
  avg_energy = np.mean(rms)

  #Pause detection
  intervals = librosa.effects.split(y, top_db=20)
  pause_count = len(intervals)

  #Speaking rate 
  words_estimate = duration * 2
  words_per_sec = words_estimate / duration if duration > 0 else 0

  #Pace
  if words_per_sec > 2.5:
    pace = "Fast"
  elif words_per_sec < 1.5:
    pace = "Slow"
  else:
    pace = "Moderate"

  #Confidence
  if avg_energy > 0.05:
    confidence = "High"
  elif avg_energy > 0.02:
    confidence = "Medium"
  else:
    confidence = "Low"

  #Pauses
  if pause_count > 15:
    pauses = "Too many pauses"
  elif pause_count > 8:
    pauses = "Moderate pauses"
  else:
    pauses = "Smooth delivery"


  return {
    "duration": round(duration, 2),
    "confidence": confidence,
    "pace": pace,
    "pauses": pauses
  }

