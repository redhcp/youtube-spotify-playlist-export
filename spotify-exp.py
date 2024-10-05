import os
import requests
import csv
import base64
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

SPOTIFY_PLAYLIST_ID = os.getenv('SPOTIFY_PLAYLIST_ID')
SPOTIFY_PLAYLIST_URL = 'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_TOKEN_URL = os.getenv('SPOTIFY_TOKEN_URL')

def get_spotify_token(client_id, client_secret):
    # Create the authorization header
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        'Authorization': f'Basic {b64_auth_str}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }

    # Request a token from Spotify
    response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)
    
    # Check if the request was successful
    if response.status_code == 200:
        token = response.json().get('access_token')
        print(f"Successfully Token received: {token}")  # Debugging line
        return token
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Function to get playlist tracks from Spotify
def get_spotify_playlist_tracks(token, playlist_id):
    url = SPOTIFY_PLAYLIST_URL.format(playlist_id=playlist_id)
    headers = {
        'Authorization': f'Bearer {token}'
    }

    songs = []
    while url:
        response = requests.get(url, headers=headers)
        
        # Check for a successful response
        if response.status_code != 200:
            return songs  # Return what we've fetched so far or an empty list

        data = response.json()
        
        # Check if 'items' exists in the response
        if 'items' in data:
            
            for item in data['items']:
                if item['track']:  # Ensure track exists
                    track_name = item['track']['name']
                    track_url = item['track']['external_urls']['spotify']
                    songs.append({
                        'name': track_name,
                        'url': track_url
                    })
        else:
            # print("No 'items' found in response.")  # Debugging line
            return songs  # Exit the loop if no items found

        # Get the next page of results (if available)
        url = data.get('next')

    return songs

# Function to export the playlist to a CSV file
def export_to_csv(songs, filename='spotify_playlist.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'URL'])
        writer.writeheader()  # Write the header
        for song in songs:
            writer.writerow({'Title': song['name'], 'URL': song['url']})

# Main function to get playlist tracks and export them
if __name__ == '__main__':
    
    # Get Spotify OAuth token
    spotify_token = get_spotify_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

    if spotify_token:
        # Fetch the playlist tracks
        spotify_songs = get_spotify_playlist_tracks(spotify_token, SPOTIFY_PLAYLIST_ID)

        # Export the tracks to a CSV file
        export_to_csv(spotify_songs, filename='spotify_playlist.csv')
