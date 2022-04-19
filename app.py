from flask import Flask
import flask

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return flask.render_template('register.html')


@app.route('/scrum')
def main():
    return flask.render_template('main.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
