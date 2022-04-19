import random
from flask import make_response
import flask
from flask import Flask, request
from jinja2 import FileSystemLoader, Environment
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
database = client.test_database
tasks = database.tasks



app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return flask.render_template('register.html')


@app.route('/action_page.php', methods=['GET', 'POST'])
def reg_parse():
    name = (request.values['login'])
    key = (request.values['psw'])
    if not list(tasks.find({"name": name})) != []:
        resp = make_response(flask.render_template("main.html"))
        cookie = str(random.randint(-(10 ** 200), 10 ** 200))
        resp.set_cookie('userID', cookie)
        tasks.insert_one({"name":name, "key": key})
        return resp
    else:
        return "вы уже зарегестрированы"


@app.route('/scrum')
def main():
    return flask.render_template('main.html')


# @app.get()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
