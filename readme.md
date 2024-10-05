## Playlist Exporter

This repository contains a Python script designed to export playlist titles and song URLs to a CSV file.

## Features

- Extracts titles and corresponding song URLs.
- Outputs the data into a structured CSV format for easy access.
- Separate scripts for exporting from Spotify (`spotify-exp.py`) and YouTube (`youtube-exp.py`).

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/redhcp/youtube-spotify-playlist-export.git
   ```

2. Navigate to the project directory:

   ```bash
   cd youtube-spotify-playlist-export
   ```

3. Complete `.env` file with the necessary credentials.

   - [Spotify Documentation](https://developer.spotify.com/documentation/web-api/concepts/apps/)
   - [Google Documentation](https://cloud.google.com/docs/authentication/api-keys) & [Console.Cloud.Google](https://console.cloud.google.com/apis/credentials)

4. #### Make sure you have the following installed:

- Python 3.x

- Create a virtual environment:

  `python -m venv venv`

- Activate the virtual environment:

  `.\venv\Scripts\activate`

- Install only the required libraries for your project:

  ```
  pip install requests
  pip install python-dotenv
  ```

- Freeze only necessary packages:

  ` pip freeze > requirements.txt`

- Required libraries (can be installed via `requirements.txt`):
  ```bash
  pip install -r requirements.txt
  ```

5. Run the Python script:

```bash
  python .\spotify-exp.py
```

OR

```bash
  python .\youtube-exp.py
```

## Notes

The script will generate a CSV file containing the playlist details in root dir.

- `spotify_playlist.csv`
- `youtube_playlist.csv`
