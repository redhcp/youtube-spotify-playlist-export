# """
# Spotify Liked Songs Exporter
# Exports all your liked/saved songs to a CSV file.

# Requirements:
#     pip install spotipy

# Setup:
#     1. Go to https://developer.spotify.com/dashboard
#     2. Create an app (any name/description)
#     3. In the app settings, add this Redirect URI: http://localhost:8888/callback
#     4. Copy your Client ID and Client Secret
#     5. Fill in the constants below (CLIENT_ID, CLIENT_SECRET)
# """
from dotenv import load_dotenv
import os

import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
load_dotenv()
# ── FILL THESE IN ─────────────────────────────────────────────────────────────
SPOTIFY_CLIENT_ID=os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET=os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI =os.getenv("SPOTIFY_REDIRECT_URI") # must match your app settings
OUTPUT_FILE   = "spotify_liked_songs.csv"
# ──────────────────────────────────────────────────────────────────────────────

SCOPE = "user-library-read"


def get_all_liked_songs(sp: spotipy.Spotify) -> list[dict]:
    """Fetch every liked track using Spotify's paginated API."""
    tracks = []
    limit  = 50   # max allowed per request 50
    offset = 0

    while True:
        response = sp.current_user_saved_tracks(limit=limit, offset=offset)
        items    = response.get("items", [])

        if not items:
            break

        for item in items:
            track   = item["track"]
            artists = ", ".join(a["name"] for a in track["artists"])

            tracks.append({
                "title":        track["name"],
                "artist":       artists,
                "spotify_url":  track["external_urls"]["spotify"],
            })

        offset += limit
        print(f"  Fetched {len(tracks)} songs so far...", end="\r")

        # stop when we've received everything
        if offset >= response["total"]:
            break

    return tracks


def export_to_csv(tracks: list[dict], filepath: str) -> None:
    """Write the track list to a CSV file."""
    if not tracks:
        print("No tracks found.")
        return

    fieldnames = list(tracks[0].keys())

    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tracks)

    print(f"\nExported {len(tracks)} songs to '{filepath}'")


def main():
    # SpotifyOAuth opens a browser for login on first run,
    # then caches the token in .cache for subsequent runs.
    auth_manager = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SCOPE,
        open_browser=True,
    )

    sp = spotipy.Spotify(auth_manager=auth_manager)

    print("Fetching liked songs...")
    tracks = get_all_liked_songs(sp)
    export_to_csv(tracks, OUTPUT_FILE)


if __name__ == "__main__":
    main()
