from flask import Flask, request
from jinja2 import FileSystemLoader, Environment
from pymongo import MongoClient

templateLoader = Environment(loader=FileSystemLoader(searchpath='./tem'))
app = Flask(__name__)
client = MongoClient('localhost', 27017)
database = client.test_database
tasks = database.tasks


@app.route("/")
def get_info():
    return templateLoader.get_template('123.html').render()


@app.route("/Tasks", methods=['POST'])
def post_info():
    name = request.form.get('names')
    key = request.form.get('keys')
    tasks.insert_one({name: key})
    return "Успешная Регистрация"


app.run(host='0.0.0.0', port=3000)
