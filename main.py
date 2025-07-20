from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

model = joblib.load("fake_follower_model.pkl")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, followers: int = Form(...), following: int = Form(...), posts: int = Form(...)):
    data = [[followers, following, posts]]
    prediction = model.predict(data)[0]
    result = "Fake Follower ❌" if prediction == 1 else "Real Follower ✅"
    return templates.TemplateResponse("index.html", {"request": request, "result": result})