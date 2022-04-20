import random
from flask import make_response
import flask
from flask import Flask, request
from jinja2 import FileSystemLoader, Environment
from pymongo import MongoClient

def _64():
    alpf = 'abcdefghigklmnopqrstuvwxyzABCDEFGHIGKLMNOPQRSTUVWXYZ1234567890#$'
    n = ''
    for i in range(10): n+=alpf[random.randint(0, 63)]
    return n

client = MongoClient('localhost', 27017)
database = client.test_database
tasks = database.tasks
boards = database.board

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return flask.render_template('gt.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg_parse():
    name = (request.values['login'])
    key = (request.values['psw'])
    if not tasks.count_documents({"name": name}):
        tasks.insert_one({"id": _64(), "name": name, "key": key})
        resp = make_response(flask.render_template("main.html"))
        cookie = tasks.find_one({"name": name})["id"]
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
        if tasks.find_one({"name": name})["key"] == key:
            resp = make_response(flask.redirect("/list"))
            cookie = tasks.find_one({"name": name})["id"]
            resp.set_cookie('userID', cookie)
            return resp
        return "неверный пароль"
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
    try: lst = boards.find({"users":  userID})
    except IndexError: lst = []
    return flask.render_template("main.html", lst = lst)

@app.route('/list/add', methods = ['POST'])
def add():
    userID = request.cookies.get("userID")
    boards.insert_one({"id": _64(), "name": request.form.get("board_name"), "users": [userID]})
    return flask.redirect('/list')

@app.route('/list/new_user', methods = ['GET'])
def new_user(): # new user in list 
    userID = request.cookies.get("userID")
    (boards.find_one({"id": request.form.get("id")})["users"]).append(userID)
    return flask.redirect('/list')

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
