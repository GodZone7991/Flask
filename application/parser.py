import requests


id = str(input())

URL_SPOTIFY = 'https://api.spotify.com/v1/users/{id}/playlists'

def parse_playlist():

    pass


def parser_test( test_element: str) -> bool:
    '''  the function returns True if the first element in the returned list
    matches the expected result
    '''
    playlist_name = 'Night chilling'
    first_track:str = 'Saturn Boy'

    if test_element == first_track:
         return True
    return False







