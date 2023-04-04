import requests
import json

# Spotify API credentials
SPOTIFY_CLIENT_ID = 'your_spotify_client_id'
SPOTIFY_CLIENT_SECRET = 'your_spotify_client_secret'

# Apple Music API credentials
APPLE_MUSIC_DEVELOPER_TOKEN = 'your_apple_music_developer_token'

# Spotify playlist URL
SPOTIFY_PLAYLIST_URL = 'https://api.spotify.com/v1/playlists/your_spotify_playlist_id/tracks'

# Apple Music playlist name
APPLE_MUSIC_PLAYLIST_NAME = 'your_apple_music_playlist_name'

# Authenticate with the Spotify API
auth_response = requests.post('https://accounts.spotify.com/api/token', {
    'grant_type': 'client_credentials',
    'client_id': SPOTIFY_CLIENT_ID,
    'client_secret': SPOTIFY_CLIENT_SECRET,
})
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']

# Get the list of tracks from the Spotify playlist
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}
response = requests.get(SPOTIFY_PLAYLIST_URL, headers=headers)
response_data = response.json()

# Get the Apple Music ID for each track
apple_music_track_ids = []
for track in response_data['items']:
    query_params = {
        'term': f'{track["track"]["name"]} {track["track"]["artists"][0]["name"]}',
        'types': 'songs',
        'limit': '1',
    }
    headers = {
        'Authorization': f'Bearer {APPLE_MUSIC_DEVELOPER_TOKEN}',
        'Music-User-Token': 'your_apple_music_user_token',
    }
    response = requests.get('https://api.music.apple.com/v1/catalog/us/search', headers=headers, params=query_params)
    response_data = response.json()
    if response_data['results']['songs']['data']:
        apple_music_track_ids.append(response_data['results']['songs']['data'][0]['id'])

# Create a new Apple Music playlist and add the tracks to it
headers = {
    'Authorization': f'Bearer {APPLE_MUSIC_DEVELOPER_TOKEN}',
    'Music-User-Token': 'your_apple_music_user_token',
    'Content-Type': 'application/json'
}
playlist_data = {
    'attributes': {
        'name': APPLE_MUSIC_PLAYLIST_NAME,
        'description': 'Converted from Spotify',
    },
    'relationships': {
        'tracks': {
            'data': [{'id': track_id, 'type': 'songs'} for track_id in apple_music_track_ids]
        }
    },
    'type': 'playlists',
}
response = requests.post('https://api.music.apple.com/v1/me/library/playlists', headers=headers, data=json.dumps(playlist_data))
response_data = response.json()
