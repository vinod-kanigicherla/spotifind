import os
import spotipy
from fastapi import FastAPI, Form, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from spotipy.oauth2 import SpotifyOAuth
from starlette.responses import RedirectResponse

from reco import *

app = FastAPI()
username = ""

SPOTIFY_CLIENT_ID = '01385e98a17747c58c71ebdf6c755f58'
SPOTIFY_CLIENT_SECRET = '89c5965b40484437ae9a13c53af6ca9a'
SPOTIFY_REDIRECT_URI = 'http://localhost:3000/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope='user-top-read playlist-modify-private playlist-modify-public',
                                               username=username))
sp_with_token = None

access_token = None

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

class Username(BaseModel):
    username: str

class PlaylistIds(BaseModel):
    playlistIds: List[str]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def read_root() -> dict:
    return {"Hello": "World."}

@app.get("/authorize/")
async def authorize():
    # This will redirect the user to the Spotify authorization page
    auth_url = sp.auth_manager.get_authorize_url()
    print(f"Auth URL: {auth_url}")
    return {"auth_url": auth_url}

# Endpoint to handle the Spotify callback with the authorization code
@app.get("/callback")
async def callback(code: str):
    # This will exchange the authorization code for an access token
    global username
    global access_token
    global sp_with_token
    global SPOTIFY_CLIENT_ID
    global SPOTIFY_CLIENT_SECRET
    global SPOTIFY_REDIRECT_URI
    global sp_with_token
    print(f"Callback Username: {username}")
    access_token = sp.auth_manager.get_access_token(code)
    sp_with_token = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope='user-top-read playlist-modify-private playlist-modify-public',
        username=username))
    
    return {
        "message": "Authorization successful. You can now use Spotipy to make authenticated API requests.",
        "token": f"{access_token}"
            }


@app.get("/recommend")
async def read_root() -> dict:
    return {"message": "Unauthorized"}

@app.post("/submit_username/")
async def submit_username(data: Username):
    global username
    global sp
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope='user-top-read playlist-modify-private playlist-modify-public',
                                               username=username))
    user_playlists = fetch_user_playlists(data.username)
    if user_playlists:
        set_username(data.username)
        username = data.username

        return {
            "message": f"Valid Username: {data.username}", 
            "playlists": fetch_user_playlists(data.username)
        }
    else:
        return {
            "message": f"Invalid Username: {data.username}. Try Again!"
        }

@app.post("/submit_playlists/")
async def submit_playlists(data: PlaylistIds):
    global username
    global access_token
    global sp_with_token

    print(f"Access Token: {access_token}")
    user_sp = spotipy.Spotify(auth=access_token['access_token'])

    print("Loading..")
    print(f"Spotipy Username Used: {username}")

    final_recommendations = recommendation_driver(data.playlistIds, user_sp)

    print(final_recommendations)
    
    return {
        "reco_playlists_link": f"{final_recommendations}"
    }