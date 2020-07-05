from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from flask_mysqldb import MySQL

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

@app.route('/student/viewgames')
def viewgames():
    return render_template('viewgames.html')

@app.route('/student/pastgames')
def pastgames():
    return render_template('pastgame.html')

@app.route('/teacher/showgameslist')
def showgameslist():
    return render_template('showgameslist.html')

@app.route('/teacher/createagame')
def createagame():
    return render_template('creategame.html')

@app.route('/teacher/gamedetails')
def gamedetails():
    return render_template('gamedetails.html')

@app.route('/student/gamepage')
def gamepage():
    return render_template('gamepage.html')

if __name__ == "__main__":
    app.run(debug=True)
