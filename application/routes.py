import spotipy
from flask import render_template, make_response, jsonify, request
from flask import current_app as app
from application.config import SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_ID
from application.homework_shooting_range import display_winner, competition
from spotipy.oauth2 import SpotifyClientCredentials
from .models import db, Track
from sqlalchemy import exc


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


@app.route('/api', methods=['GET'])
def show_api():
    auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    results = spotify.playlist(request.args['playlist'], fields=None, market=None, additional_types=('track',))
    results = results['tracks']['items']
    ids = [item['track']['id'] for item in results]
    features = spotify.audio_features(tracks=ids)
    for index, item in enumerate(features):
        track = Track(name=results[index]['track']['name'],
                      track_id=item['id'],
                      danceability=item['danceability'],
                      energy=item['energy'],
                      key=item['key'],
                      loudness=item['loudness'],
                      mode=item['mode'],
                      speechiness=item['speechiness'],
                      acousticness=item['acousticness'],
                      instrumentalness=item['instrumentalness'],
                      liveness=item['liveness'],
                      valence=item['valence'],
                      tempo=item['tempo'],
                      mood_label=request.args['mood'])
        set_fields = track.__dict__.copy()
        del set_fields['_sa_instance_state']
        try:
            db.session.add(track)
            db.session.commit()
        except exc.IntegrityError or exc.InvalidRequestError:
            db.session.rollback()
            changed_track = Track.query.filter_by(track_id=ids[index]).update(set_fields)
            db.session.commit()
    return make_response(jsonify(features), 200)


@app.route('/clear_db')
def clear_db():
    pass
