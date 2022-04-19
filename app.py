from flask import Flask
import flask

app = Flask(__name__)


# максим, ты можешь перезапускать пргу?
# да
# а сайт у тебя работает?
# ты на вай фае?
# классно
@app.route('/', methods=['GET', 'POST'])
def home():
    return flask.render_template('register.html')


# куда хочешь bruh, у тебя полный доступ к проекту

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
