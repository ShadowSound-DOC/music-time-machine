"""Music Time Machine — Billboard Hot 100 for a date → private Spotify playlist."""
import os

import requests
import spotipy
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

URI = os.environ["SPOTIPY_REDIRECT_URI"]
CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
scope = "playlist-modify-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=URI,
        scope=scope,
        cache_path=".cache",
        show_dialog=True,
    )
)
user_id = sp.current_user()["id"]

header_browser = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
}
date = str(input("Which year do you want to travel to? Type a date in this format YYYY-MM-DD:"))

request = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/", headers=header_browser)
soup = BeautifulSoup(request.text, "html.parser")
all_tags_h3 = soup.body.find_all(
    name="h3",
    id="title-of-a-story",
    class_=(
        "c-title a-no-trucate a-font-primary-bold-s "
        "u-letter-spacing-0021 "
        "lrv-u-font-size-18@tablet "
        "lrv-u-font-size-16 u-line-height-125 "
        "u-line-height-normal@mobile-max "
        "a-truncate-ellipsis u-max-width-330 "
        "u-max-width-230@tablet-only"
    ),
)

songs_list = [tag.getText() for tag in all_tags_h3]
cleaned_list = [item.replace("\n", "").replace("\t", "").strip() for item in songs_list]
print(cleaned_list)

song_uris = []
for song in cleaned_list:
    result = sp.search(q=f"track:{song}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} can't be found in Spotify")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(f"Created playlist: {playlist.get('name')}")
