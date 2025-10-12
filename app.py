import os
import re
import requests
from flask import Flask, request, render_template
import whisper
from dotenv import load_dotenv
from pathlib import Path

# 🔇 Disable noisy Google/gRPC logs before importing generativeai
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_TRACE"] = ""
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import google.generativeai as genai

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

app = Flask(__name__)

# -------------------------------------------------
# Load Whisper model (tiny for minimal RAM use)
# -------------------------------------------------
MODEL = whisper.load_model("tiny")

# -------------------------------------------------
# Configure Gemini API and initialize model globally
# -------------------------------------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_GEMINI = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

# -------------------------------------------------
# Utility function to clean transcript text
# -------------------------------------------------
def clean_summary(text):
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        # Check if a file was uploaded
        if "file" not in request.files:
            return {"error": "No file uploaded"}

        file = request.files["file"]
        if file.filename == "":
            return {"error": "Empty filename"}

        # Save uploaded audio
        os.makedirs("uploads", exist_ok=True)
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        # Step 1: Transcribe with Whisper
        result = MODEL.transcribe(filepath)
        transcript = clean_summary(result["text"])

        # Step 2: Summarize with Gemini
        prompt = f"""
        Summarize the following meeting transcript clearly.
        Include:
        - Key discussion points
        - Decisions made
        - Action items assigned

        Transcript:
        {transcript}
        """

        response = MODEL_GEMINI.generate_content(prompt)
        summary = response.text.strip()

        # Step 3: Clean up
        os.remove(filepath)

        # Step 4: Return results to frontend
        return {
            "transcript": transcript,
            "summary": summary,
        }

    except Exception as e:
        return {"error": str(e)}


# -------------------------------------------------
# Run Flask app
# -------------------------------------------------
if __name__ == "__main__":
    # Disable Flask’s double reloader for clean logs
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
