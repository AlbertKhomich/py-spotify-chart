import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Date to travel back in format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{date}/"

site = requests.get(URL).text

soup = BeautifulSoup(site, "html.parser")

top_1 = soup.find("h3", class_="c-title").a.text.strip()
top_html = soup.find_all("h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 "
                               "lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 "
                               "u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 "
                               "u-max-width-230@tablet-only")
top = [title.text.strip() for title in top_html]
top.append(top_1)

# Auth Spotify Api
scope = 'playlist-modify-private'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

result = sp.current_user()
user = result["id"]

# Making a playlist on Spotify
uri = [sp.search(f'track:{track}, year:{date[0:4]}', limit=1)['tracks']['items'][0]['uri'] for track in top
       if len(sp.search(f'track:{track}, year:{date[0:4]}', limit=1)['tracks']['items']) > 0]

playlist = sp.user_playlist_create(user, f"Top by {date}", public=False)

sp.playlist_add_items(playlist['id'], [uri][0])
