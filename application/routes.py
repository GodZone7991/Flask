import requests
from flask import render_template
from flask import current_app as app
from application.config import API_KEY, API_URL, SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_ID
from application.homework_shooting_range import display_winner, competition
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


response2 = "<script> alert( 'Привет, мир!' );</script>"

@app.route('/')
def show_home():
    headers = {
        'user-agent': 'Psychomusic'
    }

    payload = {
        'artist': 'Drake',
        'api_key': API_KEY,
        'method': 'artist.getsimilar',
        'format': 'json'
    }

    r = requests.get(API_URL, params = payload, headers=headers)

    return render_template('about.html', context=r.json())


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
    return render_template('home.html', context=response2)

@app.route('/api')
def show_api():
    auth_manager = SpotifyClientCredentials()
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

    results = spotify.artist_top_tracks(lz_uri)

    for track in results['tracks'][:10]:
        print('track    : ' + track['name'])
        print('audio    : ' + track['preview_url'])
        print('cover art: ' + track['album']['images'][0]['url'])
        print()


if __name__ == '__main__':
   application = app.run()


