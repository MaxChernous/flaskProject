from flask import Flask
import flask
from flask import request
import random
from flask import make_response

def is_reg(login):
    return True


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return flask.render_template('register.html')


@app.route('/action_page.php', methods=['GET', 'POST'])
def reg_parse():
    print(request.values['login'])
    print(request.values['psw'])
    if not is_reg(request.values['login']):
        set_cookies(request)
        resp=make_response(flask.render_template("main.html"))
        resp.set_cookie('userID')
        return flask.render_template("main.html")  # data is empty


def set_cookies(req):
    cookie = str(random.randint(-10 ** 200, 10 ** 200))

@app.route('/scrum')
def main():
    return flask.render_template('main.html')


# @app.get()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
