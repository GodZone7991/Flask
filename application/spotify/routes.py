# from flask import current_app as app
from flask import make_response, jsonify, request, redirect, url_for, session
from .spotify import spotify_bp
from . import controller
import uuid


# TODO: Make user login function


@spotify_bp.route('/account', methods=['GET'])
def login():
    code = request.args.get('code')
    if session.get('uuid') is None:
        session['uuid'] = str(uuid.uuid4())
        _login = controller.login(session=session.get('uuid'), code=code)
        return redirect(_login)
    if code is not None:
        _login = controller.login(session=session.get('uuid'), code=code)
        return redirect(url_for(_login))
    return make_response("You've successfully logged in!", 200)


@spotify_bp.route('/parse_playlist', methods=['GET'])
def parse_playlist() -> make_response():

    """
    This view expect two request parameters: spotify id and mood label. It finds spotify playlist by Spotify API, gets
    track's features list, and sets a mood label to every track in it. After all it saves the added track to the DB.
    :return: make_response(status, code)
    """
    playlist_id = request.args.get('playlist')
    if playlist_id is None:
        return make_response('No arguments transmitted', 200)
    else:
        response = controller.parse_playlist(playlist_id)
        return make_response(response, 200)


@spotify_bp.route('/get_recommendations', methods=['GET'])
def get_playlist() -> make_response():
    """
    This function accepts a sequence of http parameters for filtering of Spotify's recommendation query.
    One of required parameters is either seed_genres or seed_tracks or seed_artists. Rest are used for filtering and
    aren't necessary.
    :return: make_response(status, code)
    """
    # TODO: make a returning value of this function more informative and adaptive; make error handlers
    current_session = session.get('uuid')
    if current_session is None:
        return redirect(url_for('spotify_bp.login'))
    response = controller.get_playlist(session=current_session)
    return make_response(response)
