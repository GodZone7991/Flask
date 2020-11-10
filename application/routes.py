import spotipy
from flask import render_template, make_response
from flask import current_app as app
from application.config import SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_ID
from application.homework_shooting_range import display_winner, competition
from spotipy.oauth2 import SpotifyClientCredentials
# from .models import db, User


@app.route('/')
def show_home():
    return render_template('about.html')


@app.route('/game')
def show_game():
    data = competition()
    data = display_winner(data)
    for i, table in enumerate(data):
        table_ = table.to_html(classes="table")
        data[i] = table_.replace('\n', '')
    print(*map(type, data))
    return render_template('home.html', context=data)


@app.route('/about')
def show_about():
    return render_template('home.html')


@app.route('/api')
def show_api():
    auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    results = spotify.playlist('7kTsQDqmiqND9wxEP4sZx4', fields=None, market='RU', additional_types=('track', ))
    results = results['tracks']['items']
    results = [item['track']['id'] for item in results]
    features = spotify.audio_features(tracks=results)
    print(features)
    return make_response('OK!', 200)
