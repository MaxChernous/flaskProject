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
    return flask.render_template('index.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg_parse():
    name = (request.values['login'])
    key = (request.values['psw'])
    if not tasks.count_documents({"name": name}):
        tasks.insert_one({"id": str(random.randint(-(2 ** 200), 2 ** 200)), "name": name, "key": key, "desks":['desk 1', 'desk 2']})
        resp = make_response(flask.render_template("main.html"))
        cookie = tasks.find({"name": name})[0]["id"]
        resp.set_cookie('userID', cookie)
    else:
        resp = (flask.render_template("register.html"))
        resp += "<p class=text>извините данный логин уже занят</p>"
    return resp


@app.route('/auth', methods=['GET', 'POST'])
def authorize():
    name = (request.values['login'])
    key = (request.values['psw'])
    if tasks.count_documents({"name": name}):
        if tasks.find({"name": name})[0]["key"] == key:
            resp = make_response(flask.render_template("main.html"))
            cookie = tasks.find({"name": name})[0]["id"]
            resp.set_cookie('userID', cookie)
            return flask.redirect("/list")
        return "нет пароля"
    return "нет логина"


@app.route("/form_reg")
def reg_send():
    return flask.render_template("register.html")


@app.route("/form_auth")
def auth_send():
    return flask.render_template("authorize.html")


@app.route('/list')
def main():
    userID = request.cookies.get("userID")
    lst = tasks.find({"id": userID})[0]["desks"]
    print(lst) 
    return flask.render_template("main.html", lst = lst)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
