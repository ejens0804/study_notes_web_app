# SmartTools - AI-Powered Study Assistant

An AI-powered web application that helps students study more effectively. SmartTools converts notes and documents into flashcards, generates audio from text, and summarizes documents using Google Gemini and ElevenLabs APIs.

## Features

- **Text to Flashcards** — Paste notes or upload a document to generate interactive Q&A flashcards with 3D flip animations
- **Text to Speech** — Convert written text or uploaded documents into natural-sounding audio
- **Document Summarizer** — Upload a PDF, DOCX, or TXT file and receive key takeaways and a concise summary
- **AI Query** — Send custom prompts directly to Google Gemini for any question

## Instructions for Build and Use

Steps to build and run the software:

1. Clone the repository and navigate to the project folder
2. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS/Linux
   venv\Scripts\activate           # Windows
   ```
3. Install dependencies:
   ```bash
   pip install fastapi uvicorn jinja2 python-docx pypdf pdfplumber google-genai elevenlabs python-dotenv
   ```
4. Create a `.env` file in the project root and add your API keys:
   ```
   gemini_key = YOUR_GOOGLE_GEMINI_API_KEY
   elevenlabs_key = YOUR_ELEVENLABS_API_KEY
   ```
5. Start the server:
   ```bash
   uvicorn app:app --reload
   ```
6. Open `http://localhost:8000` in your browser

Instructions for using the software:

1. Navigate to the desired tool using the top navigation bar
2. Either paste text directly into the input box or upload a `.txt`, `.pdf`, or `.docx` file
3. Click the action button (e.g., "Generate Flashcards", "Summarize", "Convert to Speech")
4. Results appear below — flashcards can be flipped by clicking them

## Development Environment

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* Python 3.8+
* fastapi
* uvicorn
* jinja2
* python-docx
* pypdf
* pdfplumber
* google-genai
* elevenlabs
* python-dotenv

## API Keys

| Service | Purpose | Where to get it |
|---------|---------|----------------|
| Google Gemini | Flashcard generation, summarization, AI queries | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| ElevenLabs | Text-to-speech audio synthesis | [ElevenLabs Account Settings](https://elevenlabs.io/) |

## Project Structure

```
study_notes_web_app/
├── app.py                  # FastAPI application and all route handlers
├── .env                    # API keys (not committed to git)
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Shared layout with navbar
│   ├── home.html           # Landing page
│   ├── text2flashcards.html
│   ├── text2speech.html
│   ├── docx_summary.html
│   └── contact.html
├── static/
│   ├── css/style.css       # Global styles
│   └── js/                 # Frontend scripts
└── MailExperiment/
    └── mail.py             # Experimental email script
```

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [Google Gemini API Docs](https://ai.google.dev/gemini-api/docs)
* [ElevenLabs API Docs](https://elevenlabs.io/docs)

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] Add a login/account system to save flashcard sets
* [ ] Support additional file types (e.g., `.pptx`, images with OCR)
* [ ] Implement email delivery of summaries and flashcards via the contact/email module
* [ ] Add a quiz mode that tracks scores across flashcard sessions
* [ ] Deploy to a cloud platform (e.g., Railway, Render, or AWS)
