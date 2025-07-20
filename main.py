from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import uvicorn

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = joblib.load("fake_follower_model.pkl")

class InstaProfile(BaseModel):
    followers: int
    following: int
    posts: int
    bio: str
    has_dp: bool
    avg_likes: int
    avg_comments: int

@app.post("/predict")
def predict(profile: InstaProfile):
    bio_len = len(profile.bio)
    follow_ratio = profile.following / profile.followers if profile.followers else 0
    engagement = (profile.avg_likes + profile.avg_comments) / profile.followers if profile.followers else 0

    features = [[
        profile.followers,
        profile.following,
        profile.posts,
        bio_len,
        int(profile.has_dp),
        profile.avg_likes,
        profile.avg_comments,
        follow_ratio,
        engagement
    ]]

    pred = model.predict(features)
    return {"result": "Fake" if pred[0] == 1 else "Real"}

# For local testing
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=10000)