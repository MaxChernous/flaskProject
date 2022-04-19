from flask import Flask
import flask
from flask import request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return flask.render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
def parse_request():
    data = request.data  # data is empty
    # need posted data here


@app.route('/scrum')
def main():
    return flask.render_template('main.html')


# @app.get()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
