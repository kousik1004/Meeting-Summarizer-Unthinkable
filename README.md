# 🧠 AI Meeting Summarizer

## Objective
A web app that transcribes meeting audio using **OpenAI Whisper (tiny model)** and summarizes it using **Google Gemini API**.

---

## 🚀 Features
- Upload `.mp3`, `.wav`, or `.m4a` audio files
- Whisper-powered transcription
- Gemini-powered summary & action items
- Automatic text file output storage

---
## ⚙️ Setup
1. Clone this repository  
2. Install dependencies  
   ```bash
   pip install -r requirements.txt
3. Create a .env file: GEMINI_API_KEY=your_api_key_here
4. Run: python app.py
5. Open in browser: http://127.0.0.1:5000