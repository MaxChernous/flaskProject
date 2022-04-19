from flask import Flask
import flask as f
from flask import request
from jinja2 import FileSystemLoader, Environment
from pymongo import MongoClient
app = f.Flask(__name__)
templateLoader = Environment(loader=FileSystemLoader(searchpath='./template'))
client = MongoClient('localhost', 27017)
database = client.test_database
tasks = database.tasks

@app.route('/', methods=['GET', 'POST'])
def home():
    return f.render_template('register.html')


@app.route('/action_page.php', methods=['GET', 'POST'])
def parse_request():
    name = f.request.values['login']
    key = f.request.values['psw']
    tasks.insert_one({name: key})
    return f.render_template("main.html")


@app.route('/scrum')
def main():
    return f.render_template('main.html')


# @app.get()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
