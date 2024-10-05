import requests
import csv
from config import YOUTUBE_API_KEY, YOUTUBE_PLAYLIST_ID

YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/playlistItems'

def get_youtube_playlist(api_key, playlist_id):
    songs = []
    url = f"{YOUTUBE_API_URL}?part=snippet&maxResults=50&playlistId={playlist_id}&key={api_key}"

    while url:
        response = requests.get(url).json()
        for item in response['items']:
            title = item['snippet']['title']
            video_id = item['snippet']['resourceId']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            songs.append({
                'title': title,
                'url': video_url
            })

        # Check if there is another page of results
        next_page_token = response.get('nextPageToken')
        if next_page_token:
            url = f"{YOUTUBE_API_URL}?part=snippet&maxResults=50&pageToken={next_page_token}&playlistId={playlist_id}&key={api_key}"
        else:
            url = None

    return songs

def export_to_csv(songs, filename='youtube_playlist.csv'):
    # Open or create the CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'URL'])
        writer.writeheader()  # Write the header
        for song in songs:
            writer.writerow({'Title': song['title'], 'URL': song['url']})

    print(f'Exported {len(songs)} songs to {filename}')


# Fetch the playlist and export it to CSV
if __name__ == '__main__':
    youtube_songs = get_youtube_playlist(YOUTUBE_API_KEY, YOUTUBE_PLAYLIST_ID)
    export_to_csv(youtube_songs, filename='youtube_playlist.csv')
