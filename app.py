from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request

from flask_mysqldb import MySQL

import yaml


app = Flask(__name__)

configs = yaml.load('db.yaml')
app.config['MYSQL_HOST'] = configs['Mysql_host']
app.config['MYSQL_USER'] = configs['user']
app.config['MYSQL_PASSWORD'] = configs['Mysql_password']
app.config['MYSQL_DB'] = configs['Mysql_db']

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loginLogic/<name>/<pas>', methods=['GET', 'POST'])
def loginLogic(name, pas):
    if request.method == 'POST':
        if name == 'teach@gmail.com' and pas == '123456789':
            return render_template()
        elif name == 'teach@gmail.com' and pas != '123456789':
            return redirect('/login')
        else:
            cur = mysql.connection.cursor()
            userslen = cur.execute("SELECT * FROM students")
            if userslen > 0:
                users = cur.fetchAll()
                for i in users:
                    if i[1] == name and i[2] == pas:
                        return render_template('student.html', student = i)
                    elif i[1] == name and i[2] != pas:
                        return redirect('/login')
                    else:
                        return redirect('/login')



                
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