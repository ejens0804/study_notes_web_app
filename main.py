from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount the static directory to the "/static" path
app.mount("/static", StaticFiles(directory="static"), name="static")

# (You will add the templates configuration and routes below)



templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    # Pass data to the template via the 'context' dictionary
    return templates.TemplateResponse("index.html", {"request": request, "name": "World"})