# Spotify & YouTube Export

Small Python tools to export Spotify playlists/liked songs and YouTube playlists to CSV.

## Setup

1. **Clone and install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Environment variables**

   Copy `env_example` to `.env` and fill in your keys:

   - **Spotify** (for liked songs and playlists): create an app at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard), then set `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, and `SPOTIFY_REDIRECT_URI` (e.g. `http://127.0.0.1:8888/callback`).
   - **Spotify playlist only**: set `SPOTIFY_PLAYLIST_ID` to the playlist ID from the playlist URL.
   - **YouTube**: get an API key from [Google Cloud Console](https://console.cloud.google.com/) (YouTube Data API v3), then set `YOUTUBE_API_KEY` and `YOUTUBE_PLAYLIST_ID`.

## Usage

| Script                         | Description                                                      | Output                    |
| ------------------------------ | ---------------------------------------------------------------- | ------------------------- |
| `spo_export_like_songs.py`     | Export your Spotify **Liked Songs** (browser login on first run) | `spotify_liked_songs.csv` |
| `spo_export_playlist_songs.py` | Export a **Spotify playlist** by ID                              | `spotify_playlist.csv`    |
| `yt_export_songs.py`           | Export a **YouTube playlist** by ID                              | `youtube_playlist.csv`    |

Run any script with:

```bash
python spo_export_like_songs.py
python spo_export_playlist_songs.py
python yt_export_songs.py
```

## License

MIT
