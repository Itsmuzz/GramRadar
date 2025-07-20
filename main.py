from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib
import uvicorn

# App initialization
app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load your trained ML model
model = joblib.load("fake_follower_model.pkl")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/predict")
async def predict(username: str):
    # In real use, you'll fetch real Instagram data here
    # For now, mock input features
    dummy_features = extract_features(username)

    try:
        prediction = model.predict([dummy_features])[0]
        confidence = model.predict_proba([dummy_features])[0].max()
        result = {
            "username": username,
            "result": "Fake" if prediction == 1 else "Real",
            "confidence": f"{confidence*100:.2f}%"
        }
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

# Dummy feature extractor (replace with real logic later)
def extract_features(username):
    return [0.5, 0.2, 0.7, 0.4, 0.9]  # Example: bio score, dp flag, engagement, etc.

# Run only locally
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)