#  Meeting Summarizer

## Objective
Transcribe meeting audio and generate concise, action-oriented summaries with decisions and tasks.

---

### Click the link here to see the demo video: https://drive.google.com/file/d/1JkBkCKBTqLo2aC5u21Lyra7tOw2tsJzk/view?usp=sharing

---

## Features
- Upload and process meeting audio files
- Automatic transcription using OpenAI Whisper
- Smart summarization using Google Gemini API
- Simple, modern frontend built with HTML, CSS, and JavaScript
- Flask-based backend

---

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Flask (Python)
- **ASR Model:** OpenAI Whisper
- **LLM:** Google Gemini
- **Environment Management:** python-dotenv

---

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/meeting-summarizer-Unthinkable.git
   cd meeting-summarizer-Unthinkable

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Environment Setup
1. Create a `.env` file in the project root.
2. Add your Gemini API key like this:
   ```bash
   GEMINI_API_KEY=your_api_key_here
3. Run the app: 
   ```bash
   python app.py
4. Open in browser:
   ```bash
   http://127.0.0.1:5000
