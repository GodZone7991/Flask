from flask import Flask
from flask import render_template
import logic

app = Flask(__name__)

response = logic.foo()


@app.route('/')
def hello_world():
    return render_template('home.html', context=response)


@app.route('/some_page')
def foo():
    return render_template('home.html', context=response)




if __name__ == '__main__':
    app.run()
