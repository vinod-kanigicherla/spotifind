# Importing Necessary Libraries
import os
from typing import List

import spotipy
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from reco import fetch_user_playlists, recommendation_driver, set_username
from spotipy.oauth2 import SpotifyOAuth

# Initialize FastAPI app
app = FastAPI()

# Spotify API credentials from environment variables for security
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "your_default_client_id")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "your_default_client_secret")
SPOTIFY_REDIRECT_URI = os.getenv(
    "SPOTIFY_REDIRECT_URI", "http://localhost:3000/callback"
)

# Configure CORS middleware for the FastAPI app
origins = ["http://localhost:3000", "localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request bodies
class Username(BaseModel):
    username: str


class PlaylistIds(BaseModel):
    playlistIds: List[str]


# Initialize Spotipy with SpotifyOAuth without a specific username
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-top-read playlist-modify-private playlist-modify-public",
)

# Root endpoint
@app.get("/")
async def read_root() -> dict:
    return {"Hello": "World."}


# Endpoint to start the Spotify authorization flow
@app.get("/authorize/")
async def authorize():
    auth_url = sp_oauth.get_authorize_url()
    return {"auth_url": auth_url}


# Callback endpoint to handle the response from Spotify after authorization
@app.get("/callback")
async def callback(code: str):
    token_info = sp_oauth.get_access_token(code)
    access_token = token_info["access_token"]
    return {
        "message": "Authorization successful. You can now use Spotipy to make authenticated API requests.",
        "token": access_token,
    }


# Placeholder for the /recommend endpoint
@app.get("/recommend")
async def recommend() -> dict:
    return {"message": "Unauthorized"}


# Endpoint to submit a username and fetch user playlists if valid
@app.post("/submit_username/")
async def submit_username(data: Username):
    user_playlists = fetch_user_playlists(data.username)
    if user_playlists:
        set_username(
            data.username
        )  # Assuming this function sets the username globally within `reco`
        return {
            "message": f"Valid Username: {data.username}",
            "playlists": user_playlists,
        }
    else:
        return {"message": f"Invalid Username: {data.username}. Try Again!"}


# Dependency function to get access token
def get_access_token(token: str) -> str:
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")
    return token


# Endpoint to submit selected playlists for recommendation processing
@app.post("/submit_playlists/")
async def submit_playlists(
    data: PlaylistIds, access_token: str = Depends(get_access_token)
):
    user_sp = spotipy.Spotify(auth=access_token)
    final_recommendations = recommendation_driver(data.playlistIds, user_sp)
    return {"reco_playlists_link": final_recommendations}
