from flask import make_response, jsonify, request, redirect, url_for, session
from .spotify import spotify_bp
from . import controller
import uuid
from application.bot.controller import callback as bot_callback
from application import utils


# TODO: Make user login function


@spotify_bp.route('/account', methods=['GET'])
def login():
    user_id = session.get('user')
    if not user_id:
        user_id = request.args.get('user')
    user = utils.UserCache(user_id)
    if not user.cached_data['logged_in']:
        session_id = user.cached_data['spotify_session']
        session['user'] = user_id
        session['uuid'] = session_id
        user.update_cache(spotify_session=session_id)
        manager = controller.Manager(user)
        return redirect(manager.authorize_url)
    return make_response(f"Nice to meet you, {user.cached_data.get('spotify_name')}! You've successfully logged in!", 200)


@spotify_bp.route('/account/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    user = utils.UserCache(session['user'])
    manager = controller.Manager(user)
    manager.spotify.auth_manager.get_access_token(code)
    user_info = manager.spotify.me()
    user_top_tracks = manager.get_user_top_tracks()
    features = manager.spotify.audio_features(user_top_tracks)
    data = {
        'spotify_name': user_info['display_name'],
        'spotify_id': user_info['id'],
        'logged_in': 1,
        'current_status': 1,
        'features': features}
    user.update_cache(**data)
    bot_callback(user.user_id, text=user_info['display_name'])
    return redirect(url_for('spotify_bp.login'))


@spotify_bp.route('/parse_playlist', methods=['GET'])
def parse_playlist() -> make_response():

    """
    This view expect three request parameters:
    user - a telegram id of requesting user,
    spotify id,
    mood label
    It finds spotify playlist by Spotify API, gets track's features list, and sets a mood label to every track in it.
    After all it saves the added track to the DB.
    :return: make_response(status, code)
    """
    user_id = request.args.get('user')
    playlist_id = request.args.get('playlist')
    mood = request.args.get('mood')
    user = controller.UserCache(user_id)
    manager = controller.Manager(user)
    features, track_list = manager.parse_playlist(playlist_id)
    # controller.save_tracks(features, track_list, mood)
    # response = {'text': 'The playlist was updated'}
    response = [features, track_list]
    return make_response(jsonify(response), 200)


@spotify_bp.route('/get_recommendations', methods=['GET'])
def get_playlist() -> make_response():
    """
    This function accepts a sequence of http parameters for filtering of Spotify's recommendation query.
    One of required parameters is either seed_genres or seed_tracks or seed_artists. Rest are used for filtering and
    aren't necessary.
    :return: make_response(status, code)
    """
    # TODO: make a returning value of this function more informative and adaptive; make error handlers
    manager = controller.Manager(utils.UserCache(request.args.get('user')))
    response = manager.spotify.me()
    return make_response(response)


@spotify_bp.route('/get_tracks', methods=['GET'])
def get_tracks():
    options = request.args
    tracks = controller.get_tracks_data(**options)
    return make_response(jsonify(tracks), 200)


@spotify_bp.route('/get_user_top_tracks', methods=['GET'])
def get_user_top_tracks():
    user_id = request.args.get('user')
    user = controller.UserCache(user_id)
    manager = controller.Manager(user)
    tracks = manager.get_user_top_tracks()
    features = manager.spotify.audio_features(tracks)
    user.update_cache(features=features)
    return make_response(jsonify(features), 200)


@spotify_bp.route('/test', methods=['GET'])
def test():
    response = ''
    return make_response(jsonify(response))
