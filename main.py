import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy import oauth2

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')# Verify it worked
if CLIENT_ID is not None and CLIENT_SECRET is not None:
    print('It worked')


REDIRECT_URI='http://example.com'  # "http://localhost:8888/callback"  'http://example.com'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'
##############################
# fetch test
print("WE GOIN BACK IN TIME MARTY! WHERE DO YOU WANT TO GO? YYYY-MM-DD format")
date = input()
link = "https://www.billboard.com/charts/hot-100/" + date
print(link)
year = date[0:4]
print(year)
response = requests.get(link)
webpage = response.text
# print(webpage)
soup = BeautifulSoup(webpage, "html.parser")
search_result = soup.select("li ul li h3")
song_titles = [song.getText().strip() for song in search_result]
print(song_titles)
# bazdmek

sp = spotipy.Spotify(
    auth_manager=oauth2.SpotifyOAuth(
        scope="playlist-modify-public",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]


# urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'
# sp = spotipy.Spotify()
#
# artist = sp.artist(urn)
# print(artist)
#
user = sp.user(user_id)
print(user)

song_uris = []
for song in song_titles:
    result = sp.search(q='track:' + song, type='track', limit=1)  # , year:{year} , limit=1
    print(result)
    if len(result["tracks"]["items"]) > 0:
        song_uris.append(result["tracks"]["items"][0]["uri"])
# result = sp.search(q='track:' + song_titles[0], type='track', limit=1)  # , year:{year} , limit=1
# song_uri = result["tracks"]["items"][0]["uri"]
# print("song uri: " + song_uri)
playlist_info = sp.user_playlist_create(user=user_id,
                                        name="billboard top100 " + date,
                                        public=True,
                                        collaborative=False,
                                        description="The top 100 songs on the week of " + date)

print(playlist_info)
playlist_id = playlist_info["id"]
print("playlist id: " + playlist_id)
playlist_add_info = sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)

# {"uris": ["spotify:track:4iV5W9uYEdYUVa79Axb7Rh","spotify:track:1301WleyT98MSxVHPZCA6M", "spotify:episode:512ojhOuo1ktJprKbVcKyQ"]}
