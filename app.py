from flask import Flask
from flask import render_template
import logic

app = Flask(__name__)

response1 = logic.foo()
response2 = "<script> alert( 'Привет, мир!' );</script>"
response3 = "<div> <p> \"О дивный новый\" </p></div>"



@app.route('/')
def hello_world():
    return render_template('home.html', context=app.config)


@app.route('/some_page')
def foo():
    return render_template('home.html', context=response1)


@app.route('/links')
def foo2():
    return render_template('home.html', context=response2)



if __name__ == '__main__':
    app.run(debug=1)
