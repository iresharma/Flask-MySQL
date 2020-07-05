from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from uuid import uuid4
from peewee import *
from hashlib import sha256
import random

db = MySQLDatabase('deshik', user = 'root', password = 'Mahesh-01022001', host = '127.0.0.1')


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
    col1 = BooleanField(null = False, default = False)
    col2 = BooleanField(null = False, default = False)
    col3 = BooleanField(null = False, default = False)
    row1 = BooleanField(null = False, default = False)
    row2 = BooleanField(null = False, default = False)
    row3 = BooleanField(null = False, default = False)
    dia1 = BooleanField(null = False, default = False)
    dia2 = BooleanField(null = False, default = False)
    entire = BooleanField(null = False, default = False)
    type = IntegerField(null = False, default = 0)
    played = IntegerField()
    win = FloatField()
    
class students(BaseModel):
    sid = CharField(primary_key = True, null = False)
    name = CharField(null = False)
    pas = CharField(null = False)
    email = CharField(null = False, unique = True)

def create_tables():
    db.create_tables([games, students])

def choiceQues(ids):
    seq = ['row1', 'row2', 'row3', 'col1', 'col2', 'col3', 'dia1', 'dia2', 'entire']
    gameS = games.select().where(games.gid == ids).dicts().get()
    print('=================================')
    print(gameS)
    while(True):
        sel = random.choice(seq)
        if gameS[sel]:
            print(sel)
            return sel
        

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

@app.route('/student/pastgames')
def pastgames():
    return render_template('pastgame.html')

@app.route('/teacher/createagame')
def createagame():
    return render_template('creategame.html')


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
            return render_template('login.html', err = 'Incorrect password')
        else:
            try:
                user = students.get(students.email == data['name'])
                if user.pas == sha256(data['password'].encode()).hexdigest():
                    return render_template('student.html', name = user.name)
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
                return render_template('student.html', name = data['name'])
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

@app.route('/createGame', methods = ['POST'])
def createGame():
    if request.method == 'POST':
        data = request.form
        games.create(
            gid = uuid4(),
            name = data['name'],
            x_value = data['x_value'],
            o_value = data['o_value'],
            empty_value = data['empty_value'],
            col1 = True if 'col1' in data else False,
            col2 = True if 'col2' in data else False,
            col3 = True if 'col2' in data else False,
            row1 = True if 'row1' in data else False,
            row2 = True if 'row2' in data else False,
            row3 = True if 'row3' in data else False,
            dia1 = True if 'dia1' in data else False,
            dia2 = True if 'dia2' in data else False,
            entire = True if 'entire' in data else False,
            type = 0 if data['type'] else 1
        )
        gameds = list(games.select())
        return render_template('showgameslist.html', games = gameds)
        


@app.route('/student/viewgames')
def viewgames():
    gameds = list(games.select())
    return render_template('viewgames.html', games = gameds)



@app.route('/student/gamepage/<ids>')
def gamepage(ids):
    game = games.get(games.gid == ids)
    type = choiceQues(ids)
    return render_template('gamepage.html', game = game, type = type)


@app.route('/gamesPlayed', methods = ['POST'])
def gamePlayed():
    if request.method == 'POST':
        data = request.form
        print(data)
        game = games.get(games.gid == data['gid'])
        played = games.update(played = game.played + 1).where(games.gid == data['gid'])
        played.execute()
        if data['result'] == '0':
            wincalc = (game.played * game.win)/(game.played + 1) if game.win != 0 else 1/(game.played + 1)
            played = games.update(win = wincalc).where(games.gid == data['gid'])
            played.execute()
        else:
            wincalc = ((game.played * game.win) + 1)/(game.played + 1) if game.win != 0 else 1/(game.played + 1)
            played = games.update(win = wincalc).where(games.gid == data['gid'])
            played.execute()
        return render_template('student.html')


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)