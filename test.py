import requests
import json

class MySong:
    CLIENT_ID = '8a32e7538e224beab1b1cfa6f38463b3'
    CLIENT_SECRET = 'c496c68c14f14d6096d0d956289f1a95'

    def __init__(self):
        self.get_token()

    def get_token(self):
        response = requests.post(url='https://accounts.spotify.com/api/token',
                                 data={ 'grant_type': 'client_credentials' },
                                 auth=(self.CLIENT_ID, self.CLIENT_SECRET))
        self.spotify_token = response.json()['access_token']
        
    def find_songs(self, playlist_id):
        headers = {
            'Authorization': "Bearer {}".format(self.spotify_token)
        }
        songs=[]
        url = 'https://api.spotify.com/v1/playlists/{}'.format(playlist_id)
        while True:
            response = requests.get(url, headers=headers)
            results = response.json()
            newResponse = None
            
            if (results.get("items",None) is not None):
                newResponse = results['items']
            elif (results.get("tracks",None) is not None):
                newResponse = results['tracks']['items']
            
            for item in newResponse:
                if (item is not None):
                    songs.append({
                        'id' : item['track']['id'],
                        'name': item['track']['name'],
                        'url': item['track']['external_urls']['spotify'],
                        'album_name': item['track']['album']['name'],
                        'artists': item['track']['artists'][0]['name']
                    })
            if (results.get("next",None) is not None):
                url = results['next']
            elif (results.get("tracks",None) is not None):
                url = results['tracks']['next']
            else:   # no more songs
                break
        return songs

playlist_id = '<your playlist id>' # more than 700 songs playlist
my_song = MySong()
songs = my_song.find_songs(playlist_id)

print(json.dumps(songs[:3], indent=2)) # print fisrt 3 songs

print(json.dumps(songs[-3:], indent=2)) # print last 3 songs
print(len(songs)) # print total number of songs