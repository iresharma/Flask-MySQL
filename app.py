from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request


app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/student')
def student():
    return render_template('student.html')

if __name__ == "__main__":
    app.run(debug=True)