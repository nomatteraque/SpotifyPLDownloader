import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import youtube_dl
from youtube_search import YoutubeSearch

# Spotify API credentials
client_id = ''
client_secret = ''

# Initialize Spotipy client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_track_info(playlist_id):
    # Retrieve playlist tracks
    tracks = sp.playlist_tracks(playlist_id)

    # Extract track information
    track_info = []
    for item in tracks['items']:
        track = item['track']
        track_info.append({
            'name': track['name'],
            'artist': track['artists'][0]['name']
        })
    return track_info

def download_song(track_name, artist_name):
    # Search for song on YouTube
    search_query = f'{track_name} {artist_name} official audio'
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    url_to_use = ''
    results = YoutubeSearch(search_query, max_results=1).to_dict()
    for result in results:
        url_to_use += f"https://youtube.com{result['url_suffix']}"


    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url_to_use])


def main():
    # Spotify playlist URL
    playlist_url = input("Enter the Spotify playlist URL: ")

    # Extract playlist ID from URL
    playlist_id = playlist_url.split('/')[-1]

    # Retrieve track information from the playlist
    track_info = get_track_info(playlist_id)

    # Download each song
    for track in track_info:
        print(f"Downloading {track['name']} by {track['artist']}")
        download_song(track['name'], track['artist'])

if __name__ == "__main__":
    main()