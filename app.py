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
    return random.choices(list(set(artist_ids)), k=3)

def artist_info(artist_ids):
    artist_names = []
    artist_pictures = []
    artist_followers = []
    for artist in artist_ids:
        artist_info = sp.artist(artist)
        artist_names.append(artist_info.get('name'))
        artist_pictures.append(artist_info.get('images')[0].get("url"))
        artist_followers.append("{:,}".format(artist_info.get('followers').get('total')))
    return artist_names, artist_pictures, artist_followers

artists = generate_artists(playlist)

artists_list = artist_info(artists)

app = Flask(__name__)


@app.route('/')
def main():  # put application's code here
    return render_template("html/index.html", names=artists_list[0], pictures = artists_list[1], followers = artists_list[2])


if __name__ == '__main__':
    app.run()
