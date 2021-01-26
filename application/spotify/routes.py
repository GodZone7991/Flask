from flask import make_response, jsonify, request, redirect, url_for, session
from .spotify import spotify_bp
from . import controller
import uuid
from application.bot.controller import callback, TELEGRAM_CACHES
from application import utils


# TODO: Make user login function


@spotify_bp.route('/account', methods=['GET'])
def login():
    code = request.args.get('code')
    user_tg = request.args.get('telegram-id')
    if session.get('uuid') is None:
        session['uuid'] = str(uuid.uuid4())
        session['telegram-id'] = user_tg
        _login = controller.login(session=session.get('uuid'), code=code)
        return redirect(_login)
    if code is not None:
        _login = controller.login(session=session.get('uuid'), code=code)
        return redirect(url_for(_login))
    telegram_session = ''.join((TELEGRAM_CACHES, session['telegram-id']))
    user_info = controller.get_user_info(session['uuid'])
    data = {'spotify_session': session['uuid'],
            'spotify_name': user_info['display_name'],
            'spotify_id': user_info['id'],
            'logged_in': 1,
            'current_status': 1}
    utils.add_cache_data(telegram_session, **data)
    callback(session['telegram-id'], text=user_info['display_name'])
    return make_response("You've successfully logged in!", 200)


@spotify_bp.route('/parse_playlist', methods=['GET'])
def parse_playlist() -> make_response():

    """
    This view expect three request parameters:
    telegram id,
    spotify id,
    mood label
    It finds spotify playlist by Spotify API, gets track's features list, and sets a mood label to every track in it.
    After all it saves the added track to the DB.
    :return: make_response(status, code)
    """
    current_session = utils.read_cache(''.join((TELEGRAM_CACHES, request.args.get('user'))))
    playlist_id = request.args.get('playlist')
    mood = request.args.get('mood')
    features, track_list = controller.parse_playlist(current_session['spotify_session'], playlist_id)
    controller.save_tracks(features, track_list, mood)
    response = {'text': 'The playlist was updated'}
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
    current_session = utils.read_cache(''.join((TELEGRAM_CACHES, request.get('user'))))
    if current_session is None:
        return redirect(url_for('spotify_bp.login'))
    response = controller.get_playlist(session=current_session['spotify_session'])
    return make_response(response)


@spotify_bp.route('/get_tracks', methods=['GET'])
def get_tracks():
    options = request.args
    tracks = controller.get_tracks_data(**options)
    return make_response(jsonify(tracks), 200)


@spotify_bp.route('/get_user_top_tracks', methods=['GET'])
def get_user_top_tracks():
    user = request.args.get('user')
    current_session = utils.read_cache(''.join([TELEGRAM_CACHES, user]))
    tracks = controller.get_user_top_tracks(current_session['spotify_session'])
    tracks = [[track['id'], track['name']] for track in tracks['items']]
    features = controller.get_features_for_track_list(
        current_session['spotify_session'],
        [track[0] for track in tracks])
    controller.save_user_top_features(user, features)
    return make_response(jsonify(features), 200)
