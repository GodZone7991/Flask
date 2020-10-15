from flask import Flask
from flask import render_template
import logic
from homework_shooting_range import display_winner, competition

app = Flask(__name__)

response1 = logic.foo()
response2 = "<script> alert( 'Привет, мир!' );</script>"
response3 = "<div> <p> \"О дивный новый\" </p></div>"



@app.route('/')
def show_home():
    return render_template('home.html', context=app.config)


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
    app.run()
