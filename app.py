from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from uuid import uuid4
from peewee import *
from hashlib import sha256

db = MySQLDatabase('game', user = 'root', password = 'Mahesh-01022001', host = '127.0.0.1')


#MySQL schema
class BaseModel(Model):
    class Meta:
        database = db

class games(BaseModel):
    gid = CharField(primary_key = True, null = False)
    name = CharField(null = False)
    x_value = IntegerField(null = False)
    o_value = IntegerField(null = False)
    empty_value = IntegerField(null = False)
    qType1 = BooleanField(null = False, default = False)
    qType2 = BooleanField(null = False, default = False)
    qType3 = BooleanField(null = False, default = False)
    qType4 = BooleanField(null = False, default = False)
    qType5 = BooleanField(null = False, default = False)
    qType6 = BooleanField(null = False, default = False)
    qType7 = BooleanField(null = False, default = False)
    qType8 = BooleanField(null = False, default = False)
    qType9 = BooleanField(null = False, default = False)
    type = IntegerField(null = False, default = 0)
    win = IntegerField()
    
class students(BaseModel):
    sid = CharField(primary_key = True, null = False)
    name = CharField(null = False)
    pas = CharField(null = False)
    email = CharField(null = False, unique = True)
    win = CharField()
    
class gamesPlayed(BaseModel):
    gid = IntegerField(null = False)
    sid = IntegerField(null = False)
    result = BooleanField(null = False)
    gsid = CharField(primary_key = True, null = False)

def create_tables():
    db.create_tables([games, students, gamesPlayed])

db.connect()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')
                
@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

@app.route('/register')
def register():
    return render_template('register.html', emailerr = '', passerr = '')

@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/student/viewgames')
def viewgames():
    return render_template('viewgames.html')

@app.route('/student/pastgames')
def pastgames():
    return render_template('pastgame.html')

@app.route('/teacher/createagame')
def createagame():
    return render_template('creategame.html')

@app.route('/teacher/gamedetails')
def gamedetails():
    return render_template('gamedetails.html')

@app.route('/student/gamepage')
def gamepage():
    return render_template('gamepage.html')


#########################################################################################################
#Logic routes
#########################################################################################################


@app.route('/loginLogic', methods = ['GET', 'POST'])
def loginLogic():
    if request.method == 'POST':
        data = request.form
        if data['name'] == 'teacher@gmail.com' and data['password'] == '123456789':
            return render_template('teacher.html')
        elif data['name'] == 'teacher@gmail.com' and data['password'] != '123456789':
            return render_template('login.html')
        else:
            try:
                user = students.get(students.email == data['name'])
                if user.pas == sha256(data['password'].encode()).hexdigest():
                    return render_template('student.html')
                else:
                    return render_template('login.html', err = 'incorrect password')
            except:
                return render_template('login.html', err = 'doesnot exist')



@app.route('/registerLogic', methods = ['GET', 'POST'])
def registerLogic():
    if request.method == 'POST':
        data = request.form
        if data['confP'] != data['password']:
            return render_template('register.html', emailerr = '', passerr = 'Both password should match')
        else:
            try:
                students.create(
                    sid = str(uuid4()),
                    name = data['name'],
                    pas = sha256(data['password'].encode()).hexdigest(),
                    email = data['email']
                )
                return redirect(url_for('student'))
            except:
                return render_template('register.html', emailerr = 'Email id already exist', passerr = '')




@app.route('/teacher/showgameslist')
def showgameslist():
    gameds = list(games.select())
    return render_template('showgameslist.html', games = gameds)

@app.route('/deleteGame/<id>')
def deleteGame(id):
    ref = games.get(games.gid == id)
    dell = ref.delete_instance()
    gameds = list(games.select())
    return render_template('showgameslist.html', games = gameds)


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)