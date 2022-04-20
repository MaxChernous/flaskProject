import random
from flask import make_response
import flask
from flask import Flask, request
from jinja2 import FileSystemLoader, Environment
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
database = client.test_database
tasks = database.tasks

database = client.test_database
cookie_id = database.cookie
# tasks.delete_many({})
# cookie_id.delete_many({})


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return flask.render_template('gt.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg_parse():
    name = (request.values['login'])
    key = (request.values['psw'])
    if not tasks.count_documents({"name": name}):
        resp = make_response(flask.render_template("main.html"))
        cookie = str(random.randint(-(10 ** 200), 10 ** 200))
        id = str(random.randint(-(10 ** 200), 10 ** 200))
        resp.set_cookie('userID', cookie)
        tasks.insert_one({"name": name, "key": key})
        cookie_id.insert_one({name: id})
        return resp
    else:
        resp = (flask.render_template("register.html"))
        resp += "<p class=text>извините данный логин уже занят, авторизуйтесь</p>"
        return resp


@app.route('/auth', methods=['GET', 'POST'])
def authorize():
    name = (request.values['login'])
    key = (request.values['psw'])
    if not tasks.count_documents({"name": name}):
        if tasks.find({"name": name})["key"] == key:
            return "забись рега прошла"
        return "нет пароля"
    return "нет логина"


@app.route("/form_reg")
def reg_send():
    return flask.render_template("register.html")


@app.route("/form_auth")
def auth_send():
    return flask.render_template("authorize.html")


@app.route('/scrum')
def main():
    return flask.render_template('main.html')


# @app.get()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
