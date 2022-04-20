import random
from flask import make_response
import flask
from flask import Flask, request
from jinja2 import FileSystemLoader, Environment
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
database = client.test_database
tasks = database.tasks
# tasks.delete_many({})


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return flask.render_template('register.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg_parse():
    name = (request.values['login'])
    key = (request.values['psw'])
    if not tasks.count_documents({"name": name}):
        tasks.insert_one({"name": name, "key": key, "tasks":[]})
        resp = make_response(flask.render_template("login.html"))
        cookie = str(tasks.find({"name": name})[0]["_id"])
        resp.set_cookie('userID', cookie)
    else:
        resp = make_response(flask.render_template("login.html"))
        resp.set_cookie(tasks.find({"name": name})[0]["_id"])
    return resp

@app.route('/noteslist')
def main():    
    return flask.render_template('main.html')


# @app.get()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
