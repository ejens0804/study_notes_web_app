# File: app.py
# To run: uvicorn app:app --reload

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from docx import Document  # pip install python-docx
from pypdf import PdfReader  # pip install pypdf
from google import genai  # pip install google-genai
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from datetime import datetime
import pdfplumber  # pip install pdfplumber
import random
import time
import sys
import os
import io

load_dotenv()

# --- Configuration ---
GEMINI_KEY = os.getenv("gemini_key")
ELEVENLABS_KEY = os.getenv("elevenlabs_key")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
eleven_client = ElevenLabs(api_key=ELEVENLABS_KEY)

# --- AI Helper Functions ---

def text_gemini(prompt: str) -> str:
    """Send a text prompt to Gemini and return the response."""
    if not GEMINI_KEY:
        return "AI service not configured."
    client = genai.Client(api_key=GEMINI_KEY)
    while True:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=f"{prompt}. Keep your response concise enough that it can be quickly read in one to two minutes.",
            )
            return response.text
        except Exception as e:
            if "503" in str(e) or "overloaded" in str(e):
                time.sleep(5)
            else:
                print(f"Unexpected error: {e}")
                sys.exit(e)


def upload_gemini(prompt: str = None, *filepaths: str) -> str:
    """Send a text prompt plus uploaded files to Gemini and return the response."""
    if not GEMINI_KEY:
        return "AI service not configured."
    client = genai.Client(api_key=GEMINI_KEY)
    contents = []
    if prompt:
        contents.append(prompt)
    for fp in filepaths:
        if fp:
            contents.append(client.files.upload(file=fp))
    while True:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=contents
            )
            return response.text
        except Exception as e:
            if "503" in str(e) or "overloaded" in str(e):
                time.sleep(5)
            else:
                print(f"Unexpected error: {e}")
                sys.exit(e)


# --- Text Extraction Helpers ---

SUPPORTED_EXTENSIONS = {".txt", ".docx", ".pdf"}


def extract_text_from_upload(filename: str, contents: bytes) -> str:
    """Extract plain text from an uploaded file (txt, docx, or pdf)."""
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".txt":
        return contents.decode("utf-8")

    if ext == ".docx":
        doc = Document(io.BytesIO(contents))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    if ext == ".pdf":
        # Try pdfplumber first (better layout-aware extraction)
        text = ""
        try:
            with pdfplumber.open(io.BytesIO(contents)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception:
            pass

        # Fallback to pypdf if pdfplumber got nothing
        if not text.strip():
            reader = PdfReader(io.BytesIO(contents))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        return text

    raise ValueError(f"Unsupported file type: {ext}")


# --- Page Routes ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "title": "Home"})


@app.get("/api-demo", response_class=HTMLResponse)
async def text2flashcards(request: Request):
    return templates.TemplateResponse("text2flashcards.html", {"request": request, "title": "Text2Flashcards"})


@app.get("/about", response_class=HTMLResponse)
async def text2speech(request: Request):
    return templates.TemplateResponse("text2speech.html", {"request": request, "title": "Text2Speech"})


@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request, "title": "Contact"})


@app.get("/docx-summary", response_class=HTMLResponse)
async def docx_summary(request: Request):
    return templates.TemplateResponse("docx_summary.html", {"request": request, "title": "Document Summary"})


# --- Utility API Endpoints ---

@app.get("/api/time")
def get_time():
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": datetime.now().timestamp(),
    }


@app.get("/api/random")
def get_random():
    return {
        "random_number": random.randint(1, 100),
        "lucky_number": random.choice([7, 13, 21, 42, 77]),
    }


@app.get("/api/status")
def get_status():
    return {"status": "online", "message": "All systems operational", "version": "1.0.0"}


@app.get("/api/greet/{name}")
def greet(name: str):
    return {
        "message": f"Hello, {name}!",
        "greeting": random.choice(["Welcome!", "Great to see you!", "How are you?"]),
    }


# --- Core AI Endpoints ---

@app.post("/api/contact")
async def submit_contact(data: dict):
    return {
        "status": "success",
        "message": f"Thank you {data.get('name')}! We received your message.",
        "received_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


@app.post("/api/ai-query")
async def ai_query(data: dict):
    prompt = data.get("prompt")
    if not prompt:
        return {"response": "No input provided."}
    if not GEMINI_KEY:
        return {"response": "AI service not configured. Please add your API key to .env."}
    try:
        return {"response": text_gemini(prompt)}
    except Exception as e:
        return {"response": f"Error: {e}"}


@app.post("/api/summarize")
async def summarize_text(data: dict):
    text = data.get("text")
    if not text:
        return {"response": "No text provided."}
    if not GEMINI_KEY:
        return {"response": "AI service not configured. Please add your API key to .env."}
    try:
        summary_prompt = (
            "Please provide a concise summary of the following text, "
            f"highlighting the main points and key information:\n\n{text}"
        )
        return {"summary": text_gemini(summary_prompt)}
    except Exception as e:
        return {"response": f"Error: {e}"}


@app.post("/api/upload-summarize")
async def upload_and_summarize(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return {"response": f"Unsupported file type '{ext}'. Please upload a .txt, .docx, or .pdf file."}

    try:
        contents = await file.read()
        text = extract_text_from_upload(file.filename, contents)

        if not text.strip():
            return {"response": "The document appears to be empty or contains only images/scanned content."}
        if not GEMINI_KEY:
            return {"response": "AI service not configured. Please add your API key to .env."}

        summary_prompt = (
            "Please provide a concise summary of the following text, "
            f"highlighting the main points and key information:\n\n{text}"
        )
        return {"summary": text_gemini(summary_prompt), "extracted_length": len(text)}

    except Exception as e:
        return {"response": f"Error processing file: {e}"}


class TTSRequest(BaseModel):
    prompt: str


@app.post("/api/tts")
async def speak_text(request: TTSRequest):
    audio_generator = eleven_client.text_to_speech.convert(
        voice_id="Bj9UqZbhQsanLzgalpEG",
        model_id="eleven_multilingual_v2",
        text=request.prompt,
    )
    audio_bytes = b"".join(audio_generator)
    return StreamingResponse(io.BytesIO(audio_bytes), media_type="audio/mpeg")