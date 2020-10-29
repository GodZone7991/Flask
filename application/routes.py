import requests
from flask import render_template
from flask import current_app as app
from application.config import API_KEY, API_URL
from application.homework_shooting_range import display_winner, competition

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


if __name__ == '__main__':
   application = app.run()
