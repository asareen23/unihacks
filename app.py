from flask import Flask, redirect, url_for, render_template
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import os 
import sys
import random

load_dotenv() #Load Env Variables

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET))
playlist = sp.playlist("37i9dQZEVXbLRQDuF5jeBp")

def generate_artists(playlist):
    artist_ids = []
    for x in range(0,len(playlist.get("tracks").get("items"))):
        artist_ids.append(playlist.get("tracks").get("items")[x].get("track").get('artists')[0].get('id'))
    return random.choices((list(set(artist_ids))), k=3)


def get_artist_by_id(id):
    artist_info = sp.artist(id)
    artist_name = artist_info.get('name')
    artist_picture = artist_info.get('images')[0].get("url")
    artist_followers = "{:,}".format(artist_info.get('followers').get('total'))
    artist_genres = artist_info.get('genres')
    if len(artist_genres) <= 3:
        pass
    else:
        artist_genres = artist_genres[0:3]
    return artist_name, artist_picture, artist_followers, artist_genres

def preview_songs(id):
    results = sp.artist_top_tracks(id)
    track_names = []
    track_audio = []
    track_cover_art = []
    for track in results['tracks'][:3]:
        track_names.append(track['name'])
        track_audio.append(track['preview_url'])
        track_cover_art.append(track['album']['images'][0]['url'])
    return track_names, track_audio, track_cover_art

def artist_info(artist_ids):
    artist_names = []
    artist_pictures = []
    artist_followers = []
    for artist in artist_ids:
        artist_info = get_artist_by_id(artist)
        artist_names.append(artist_info[0])
        artist_pictures.append(artist_info[1])
        artist_followers.append(artist_info[2])
    return artist_names, artist_pictures, artist_followers, artist_ids


artists = generate_artists(playlist)

artists_list = artist_info(artists)

app = Flask(__name__)

@app.route('/')
def main():  # put application's code here
    return render_template("html/index.html", names=artists_list[0], pictures = artists_list[1], followers = artists_list[2], ids = artists_list[3])

@app.route("/<id>")
def artist_page(id):
    info = get_artist_by_id(id)
    tracks = preview_songs(id)
    return render_template("html/artist_page.html", name=info[0], picture = info[1], followers = info[2], genres = info[3], track_names = tracks[0], track_audio = tracks[1], track_cover = tracks[2])

if __name__ == '__main__':
    app.run()
