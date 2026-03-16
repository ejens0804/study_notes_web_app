# File: app.py
# To run: uvicorn app:app --reload
# If you have any issues and need to see what python libraries you have installed run:
# python -m pip list

from xmlrpc import client

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates  
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import random
import sys
from google import genai #pip install google-genai
import time
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from elevenlabs.client import ElevenLabs
import io
import os

# Handle token file gracefully
try:
    with open('token.txt', 'r') as file:
        key = file.read().strip()
except FileNotFoundError:
    key = None
    print("Warning: token.txt not found. AI features will not work.")

app = FastAPI()

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory="templates")

# Route for home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "title": "Home"
    })

# Route for Text2Flashcards page
@app.get("/api-demo", response_class=HTMLResponse)
async def api_demo(request: Request):
    return templates.TemplateResponse("text2flashcards.html", {
        "request": request,
        "title": "Text2Flashcards"
    })

# Route for Text2Speech page
@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("text2speech.html", {
        "request": request,
        "title": "Text2Speech"
    })

# Route for contact page
@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "title": "Contact"
    })

# Route for Docx Summary page
@app.get("/docx-summary", response_class=HTMLResponse)
async def docx_summary(request: Request):
    return templates.TemplateResponse("docx_summary.html", {
        "request": request,
        "title": "Docx Summary"
    })

# API Endpoints
@app.get("/api/time")
def get_time():
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": datetime.now().timestamp()
    }

@app.get("/api/random")
def get_random():
    return {
        "random_number": random.randint(1, 100),
        "lucky_number": random.choice([7, 13, 21, 42, 77])
    }

@app.get("/api/status")
def get_status():
    return {
        "status": "online",
        "message": "All systems operational",
        "version": "1.0.0"
    }

@app.get("/api/greet/{name}")
def greet(name: str):
    return {
        "message": f"Hello, {name}!",
        "greeting": random.choice(["Welcome!", "Great to see you!", "How are you?"])
    }

@app.post("/api/contact")
async def submit_contact(data: dict):
    return {
        "status": "success",
        "message": f"Thank you {data.get('name')}! We received your message.",
        "received_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
@app.post("/api/ai-query")
async def ai_query(data: dict):
    prompt = data.get("prompt")

    if not prompt:
        return {"response": "No input provided."}
    
    if not key:
        return {"response": "AI service not configured. Please add your API key to token.txt file."}

    try:
        answer = text_gemini(prompt)
        return {"response": answer}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}

@app.post("/api/summarize")
async def summarize_document(data: dict):
    text = data.get("text")
    
    if not text:
        return {"response": "No text provided."}
    
    if not key:
        return {"response": "AI service not configured. Please add your API key to token.txt file."}
    
    try:
        # Create a summarization prompt
        summary_prompt = f"Please provide a concise summary of the following text, highlighting the main points and key information:\n\n{text}"
        summary = text_gemini(summary_prompt)
        return {"summary": summary}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
    
from pydantic import BaseModel

class TTSRequest(BaseModel):
    prompt: str



class TTSRequest(BaseModel):
    prompt: str

eleven_client = ElevenLabs(api_key=os.getenv("elevenlabs_key"))

@app.post("/api/tts")
async def speak_text(request: TTSRequest):

    audio_generator = eleven_client.text_to_speech.convert(
        voice_id="Bj9UqZbhQsanLzgalpEG",
        model_id="eleven_multilingual_v2",
        text=request.prompt
    )

    audio_bytes = b"".join(audio_generator)

    return StreamingResponse(
        io.BytesIO(audio_bytes),
        media_type="audio/mpeg"
    )
    
    
#for text input only
def text_gemini(input=None):
    if not key:
        return "AI service not configured."
    api_key = key
    client = genai.Client(api_key=os.getenv("gemini_key"))
    while True:
        try:
            response = client.models.generate_content(model='gemini-2.0-flash-lite', contents=f"{input}. Keep your response concise enough that it can be quickly read in one to two minutes.")
            return response.text
        except Exception as e:
            if "503" in str(e) or "overloaded" in str(e):
                time.sleep(5)
            else:
                print(f"An unexpected error has occured: {e}")
                sys.exit(e)

#for text and file input WIP
#for local files uplodading; file argument should be filepath. To add extra file capacity, add file4, file5, etc
def upload_gemini(input=None, file1=None, file2=None, file3=None):
    api_key = key
    client = genai.Client(api_key=os.getenv("gemini_key"))
    contents = []
    if input:
        contents.append(input)
    for file in [file1, file2, file3]:
        if file:
            uploaded = client.files.upload(file=file)
            contents.append(uploaded)
    while True:
        try:
            response = client.models.generate_content(model="gemini-2.5-flash",contents=contents)
            return response.text
        except Exception as e:
            if "503" in str(e) or "overloaded" in str(e):
                time.sleep(5)
            else:
                print(f"Unexpected error: {e}")
                sys.exit(e)