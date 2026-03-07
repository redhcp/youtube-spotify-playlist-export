import requests
import base64
import csv

from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_CLIENT_ID=os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET=os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_PLAYLIST_ID = os.getenv("SPOTIFY_PLAYLIST_ID")

def get_token():
    auth_string = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": f"Basic {auth_base64}"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]


def get_playlist_tracks(token):
    url = f"https://api.spotify.com/v1/playlists/{SPOTIFY_PLAYLIST_ID}/tracks"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    songs = []

    while url:
        response = requests.get(url, headers=headers)
        data = response.json()

        for item in data["items"]:
            track = item["track"]
            songs.append({
                "name": track["name"],
                "artist": ", ".join(a["name"] for a in track["artists"]),
                "url": track["external_urls"]["spotify"]
            })

        url = data["next"]

    return songs


def export_csv(tracks):
    with open("spotify_playlist.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "artist", "url"])
        writer.writeheader()
        writer.writerows(tracks)

token = get_token()
tracks = get_playlist_tracks(token)
export_csv(tracks)

print("Playlist exported to spotify_playlist.csv")
