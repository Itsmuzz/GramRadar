from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import instaloader

model = joblib.load("fake_follower_model.pkl")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UsernameRequest(BaseModel):
    username: str

@app.get("/")
def root():
    return {"message": "GramRadar AI is live!"}

@app.post("/scan")
def scan_user(req: UsernameRequest):
    try:
        loader = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(loader.context, req.username)

        followers = profile.followers
        following = profile.followees
        posts = profile.mediacount
        has_pic = 1 if profile.profile_pic_url else 0
        bio_len = len(profile.biography or "")
        is_private = 1 if profile.is_private else 0
        engagement_rate = (profile.mediacount / followers) * 100 if followers else 0

        features = [[
            followers, following, posts,
            has_pic, bio_len, is_private, engagement_rate
        ]]
        prediction = model.predict(features)
        is_fake = bool(prediction[0])

        return {"is_fake": is_fake}
    except Exception as e:
        return {"error": str(e)}