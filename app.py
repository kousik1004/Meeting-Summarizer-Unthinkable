import os
import re
import requests
from flask import Flask, request, render_template
import whisper
from dotenv import load_dotenv
from pathlib import Path

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_TRACE"] = ""
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import google.generativeai as genai

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

app = Flask(__name__)

MODEL = whisper.load_model("tiny")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_GEMINI = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

def clean_summary(text):
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            return {"error": "No file uploaded"}

        file = request.files["file"]
        if file.filename == "":
            return {"error": "Empty filename"}

        os.makedirs("uploads", exist_ok=True)
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        result = MODEL.transcribe(filepath)
        transcript = clean_summary(result["text"])

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

        os.remove(filepath)

        return {
            "transcript": transcript,
            "summary": summary,
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
