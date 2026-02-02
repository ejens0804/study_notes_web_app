# To get running:
# 1. make sure you have fastapi and uvicorn installed
# 2. cd into your working directory 
# 3. run "uvicorn working:app --reload" to have the backend continously reload the webpage
# when you change the file

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"Data":"Testing123"}

