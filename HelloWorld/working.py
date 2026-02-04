# # To get running:
# # 1. make sure you have fastapi and uvicorn installed
# # 2. cd into your working directory 
# # 3. run "uvicorn working:app --reload" to have the backend continously reload the webpage
# # when you change the file

# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"Data":"Testing123"}



# To get running:
# 1. make sure you have fastapi and uvicorn installed
# 2. cd into your working directory 
# 3. run "uvicorn working:app --reload" to have the backend continously reload the webpage
# when you change the file

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
import random

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI Dashboard</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                padding: 40px;
                max-width: 800px;
                width: 100%;
            }
            
            h1 {
                color: #667eea;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            
            .subtitle {
                color: #666;
                margin-bottom: 30px;
                font-size: 1.1em;
            }
            
            .card-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px;
                border-radius: 15px;
                cursor: pointer;
                transition: transform 0.3s, box-shadow 0.3s;
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
            }
            
            .card h3 {
                margin-bottom: 10px;
                font-size: 1.2em;
            }
            
            .card p {
                font-size: 2em;
                font-weight: bold;
            }
            
            .button-group {
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
                margin-bottom: 30px;
            }
            
            button {
                background: #667eea;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 1em;
                cursor: pointer;
                transition: background 0.3s, transform 0.2s;
            }
            
            button:hover {
                background: #5568d3;
                transform: scale(1.05);
            }
            
            button:active {
                transform: scale(0.95);
            }
            
            .output {
                background: #f7f7f7;
                border-radius: 10px;
                padding: 20px;
                margin-top: 20px;
                min-height: 100px;
                font-family: 'Courier New', monospace;
            }
            
            .output h3 {
                color: #667eea;
                margin-bottom: 10px;
            }
            
            .output pre {
                white-space: pre-wrap;
                word-wrap: break-word;
            }
            
            .loading {
                display: none;
                color: #667eea;
                font-style: italic;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 FastAPI Dashboard</h1>
            <p class="subtitle">Interactive API Demo</p>
            
            <div class="card-grid">
                <div class="card" onclick="updateCard(this)">
                    <h3>Server Status</h3>
                    <p>✅ Online</p>
                </div>
                <div class="card" onclick="updateCard(this)">
                    <h3>API Version</h3>
                    <p>v1.0</p>
                </div>
                <div class="card" onclick="updateCard(this)">
                    <h3>Requests</h3>
                    <p id="requestCount">0</p>
                </div>
            </div>
            
            <div class="button-group">
                <button onclick="fetchData('/api/time')">Get Server Time</button>
                <button onclick="fetchData('/api/random')">Get Random Number</button>
                <button onclick="fetchData('/api/status')">Check Status</button>
                <button onclick="fetchData('/api/greet/World')">Say Hello</button>
            </div>
            
            <div class="output" id="output">
                <h3>Output</h3>
                <p class="loading" id="loading">Loading...</p>
                <pre id="result">Click a button to see the API response...</pre>
            </div>
        </div>
        
        <script>
            let requestCount = 0;
            
            function updateCard(card) {
                card.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    card.style.transform = 'scale(1)';
                }, 200);
            }
            
            async function fetchData(endpoint) {
                requestCount++;
                document.getElementById('requestCount').textContent = requestCount;
                
                const loading = document.getElementById('loading');
                const result = document.getElementById('result');
                
                loading.style.display = 'block';
                result.textContent = '';
                    
                try {
                    const response = await fetch(endpoint);
                    const data = await response.json();
                    
                    loading.style.display = 'none';
                    result.textContent = JSON.stringify(data, null, 2);
                } catch (error) {
                    loading.style.display = 'none';
                    result.textContent = 'Error: ' + error.message;
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

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