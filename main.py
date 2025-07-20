from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import uvicorn

# Load the trained model
model = joblib.load("fake_follower_model.pkl")

# Define app
app = FastAPI()

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request data structure
class AccountData(BaseModel):
    followers: int
    following: int
    posts: int
    has_profile_picture: int  # 1 or 0
    bio_length: int
    is_private: int           # 1 or 0
    engagement_rate: float

# Home route
@app.get("/")
def read_root():
    return {"message": "Welcome to GramRadar AI"}

# Prediction route
@app.post("/predict")
def predict(data: AccountData):
    features = [[
        data.followers,
        data.following,
        data.posts,
        data.has_profile_picture,
        data.bio_length,
        data.is_private,
        data.engagement_rate
    ]]
    prediction = model.predict(features)
    is_fake = bool(prediction[0])
    return {"is_fake": is_fake}