from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)