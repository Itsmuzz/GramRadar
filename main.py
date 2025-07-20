from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import random

app = FastAPI()

# CORS (Allow frontend to access backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace * with your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load AI model
model = joblib.load("fake_follower_model.pkl")

# Input schema
class ScanRequest(BaseModel):
    username: str

# Dummy follower data generator (simulate followers)
def simulate_followers(n=50):
    followers = []
    for _ in range(n):
        # Each follower has some fake/real traits
        data = {
            "has_profile_pic": random.choice([0, 1]),
            "has_bio": random.choice([0, 1]),
            "followers_count": random.randint(10, 5000),
            "following_count": random.randint(10, 5000),
            "posts": random.randint(0, 50),
            "is_private": random.choice([0, 1])
        }
        followers.append(data)
    return followers

# API Endpoint
@app.post("/scan")
async def scan_user(request: ScanRequest):
    username = request.username

    # Simulate 50 followers
    followers = simulate_followers(50)

    # Convert to model input format
    X = [[
        f["has_profile_pic"],
        f["has_bio"],
        f["followers_count"],
        f["following_count"],
        f["posts"],
        f["is_private"]
    ] for f in followers]

    # Predict using model
    predictions = model.predict(X)

    real = int(sum(predictions))
    fake = len(predictions) - real
    fake_ratio = round((fake / len(predictions)) * 100, 2)

    return {
        "username": username,
        "total_followers_scanned": len(predictions),
        "real": real,
        "fake": fake,
        "fake_ratio_percent": fake_ratio
    }