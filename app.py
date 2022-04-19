import random
from flask import make_response
import flask
from flask import Flask, request
from jinja2 import FileSystemLoader, Environment
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
database = client.test_database
tasks = database.tasks


def is_reg(login):
    return False


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return flask.render_template('gt.html')


@app.route('/action_page.php', methods=['GET', 'POST'])
def reg_parse():
    print(request.values['login'])
    print(request.values['psw'])
    if not is_reg(request.values['login']):
        resp = make_response(flask.render_template("main.html"))
        cookie = str(random.randint(-(10 ** 200), 10 ** 200))
        resp.set_cookie('userID', cookie)
        return resp
    return "ты долбаеб"


@app.route('/scrum')
def main():
    return flask.render_template('main.html')


# @app.get()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
