# File: app.py
# To run: uvicorn app:app --reload

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import random

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

# Route for API demo page
@app.get("/api-demo", response_class=HTMLResponse)
async def api_demo(request: Request):
    return templates.TemplateResponse("api_demo.html", {
        "request": request,
        "title": "API Demo"
    })

# Route for about page
@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {
        "request": request,
        "title": "About"
    })

# Route for contact page
@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "title": "Contact"
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