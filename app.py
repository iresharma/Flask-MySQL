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

class gameplayed(BaseModel):
    gid = CharField(null = True)
    sid = CharField(null = True)
    points = IntegerField(null = False)

class logged(BaseModel):
    sid = CharField(null = False)

def create_tables():
    db.create_tables([games, students, gameplayed, logged])

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

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')
                
@app.route('/teacher')
def teacher():
    gameds = list(games.select())
    idk = list(gameplayed.select().order_by(-gameplayed.points))
    results = []
    for i in range(len(idk)):
        name = students.get(students.sid == idk[i].sid).name
        print(name)
        k = {
            'name': name,
            'points': idk[i].points,
            'gid': idk[i].gid
        }
        results.append(k)
        print(results)
    return render_template('teacher.html', games = gameds, umm = results)

@app.route('/register')
def register():
    return render_template('register.html', emailerr = '', passerr = '')

@app.route('/student')
def student():
    gameds = list(games.select())
    idk = list(gameplayed.select().order_by(-gameplayed.points))
    results = []
    for i in range(len(idk)):
        name = students.get(students.sid == idk[i].sid).name
        print(name)
        k = {
            'name': name,
            'points': idk[i].points,
            'gid': idk[i].gid
        }
        results.append(k)
        print(results)
    return render_template('student.html', games = gameds, umm = results)

@app.route('/student/pastgames')
def pastgames():
    return render_template('pastgame.html')

@app.route('/teacher/createagame')
def createagame():
    return render_template('creategame.html')


#########################################################################################################
###############################################Logic routes##############################################
#########################################################################################################


@app.route('/loginLogic', methods = ['GET', 'POST'])
def loginLogic():
    if request.method == 'POST':
        data = request.form
        if data['name'] == 'teacher@gmail.com' and data['password'] == '123456789':
            gameds = list(games.select())
            loggedUser = 'teach'
            idk = list(gameplayed.select().order_by(-gameplayed.points))
            results = []
            for i in range(len(idk)):
                name = students.get(students.sid == idk[i].sid).name
                print(name)
                k = {
                    'name': name,
                    'points': idk[i].points,
                    'gid': idk[i].gid
                }
                results.append(k)
                print(results)
            return render_template('teacher.html', games = gameds, umm = results)
        elif data['name'] == 'teacher@gmail.com' and data['password'] != '123456789':
            return render_template('login.html', err = 'Incorrect password')
        else:
            try:
                user = students.get(students.email == data['name'])
                if user.pas == sha256(data['password'].encode()).hexdigest():
                    try:
                        gameds = list(games.select())
                        ref = list(logged.select())[0].sid
                        remove = logged.get(logged.sid == ref)
                        remove.delete_instance()
                    finally:
                        logged.create(
                            sid = user.sid
                        )
                        idk = list(gameplayed.select().order_by(-gameplayed.points))
                        results = []
                        for i in range(len(idk)):
                            name = students.get(students.sid == idk[i].sid).name
                            print(name)
                            k = {
                                'name': name,
                                'points': idk[i].points,
                                'gid': idk[i].gid
                            }
                            results.append(k)
                            print(results)
                        return render_template('student.html', games = gameds, umm = results)
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
                sid = str(uuid4())
                students.create(
                    sid = sid,
                    name = data['name'],
                    pas = sha256(data['password'].encode()).hexdigest(),
                    email = data['email']
                )
                try:
                    gameds = list(games.select())
                    ref = list(logged.select())[0].sid
                    remove = logged.get(logged.sid == ref)
                    remove.delete_instance()
                finally:
                    logged.create(
                        sid = sid
                    )
                    idk = list(gameplayed.select().order_by(-gameplayed.points))
                    results = []
                    for i in range(len(idk)):
                        name = students.get(students.sid == idk[i].sid).name
                        print(name)
                        k = {
                            'name': name,
                            'points': idk[i].points,
                            'gid': idk[i].gid
                        }
                        results.append(k)
                        print(results)
                return render_template('student.html', games = gameds, umm = results)
            except:
                return render_template('register.html', emailerr = 'Email id already exist', passerr = '')


@app.route('/deleteGame/<id>')
def deleteGame(id):
    ref = games.get(games.gid == id)
    dell = ref.delete_instance()
    gameds = list(games.select())
    idk = list(gameplayed.select().order_by(-gameplayed.points))
    results = []
    for i in range(len(idk)):
        name = students.get(students.sid == idk[i].sid).name
        print(name)
        k = {
            'name': name,
            'points': idk[i].points,
            'gid': idk[i].gid
        }
        results.append(k)
        print(results)
    return render_template('showgameslist.html', games = gameds, umm = results)

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
            type = 1 if 'type' in data else 0
        )
        gameds = list(games.select())
        idk = list(gameplayed.select().order_by(-gameplayed.points))
        results = []
        for i in range(len(idk)):
            name = students.get(students.sid == idk[i].sid).name
            print(name)
            k = {
                'name': name,
                'points': idk[i].points,
                'gid': idk[i].gid
            }
            results.append(k)
            print(results)
        return render_template('showgameslist.html', games = gameds, umm = results)



@app.route('/student/gamepage/<ids>')
def gamepage(ids):
    game = games.get(games.gid == ids)
    type = choiceQues(ids)
    loggedUser = list(logged.select())[0].sid
    return render_template('gamepage.html', game = game, type = type, id = loggedUser)


@app.route('/gamesPlayed', methods = ['POST'])
def gamePlayed():
    if request.method == 'POST':
        data = request.form
        game = games.get(games.gid == data['gid'])
        loggedUser = list(logged.select())[0].sid
        played = games.update(played = game.played + 1).where(games.gid == data['gid'])
        played.execute()
        gamea = list(gameplayed.select())
        if data['result'] == '0':
            wincalc = (game.played * game.win)/(game.played + 1) if game.win != 0 else 1/(game.played + 1)
            played = games.update(win = wincalc).where(games.gid == data['gid'])
            played.execute()
        else:
            wincalc = ((game.played * game.win) + 1)/(game.played + 1) if game.win != 0 else 1/(game.played + 1)
            played = games.update(win = wincalc).where(games.gid == data['gid'])
            played.execute()
            check = False
            for g in gamea:
                print('loop')
                if g.gid == data['gid'] and g.sid == loggedUser:
                    print(g.id)
                    update = gameplayed.update(points = g.points + 1).where(gameplayed.id == g.id)
                    update.execute()
                    check = True
            if check == False:
                gameplayed.create(
                    gid = data['gid'],
                    sid = loggedUser,
                    points = 1
                )
                print('didnt work================')
        print(gamea)
        gameds = list(games.select())
        idk = list(gameplayed.select().order_by(-gameplayed.points))
        results = []
        for i in range(len(idk)):
            name = students.get(students.sid == idk[i].sid).name
            print(name)
            k = {
                'name': name,
                'points': idk[i].points,
                'gid': idk[i].gid
            }
            results.append(k)
            print(results)
        return render_template('student.html', games = gameds, umm = results)


if __name__ == "__main__":
    db.connect()
    create_tables()
    app.run(debug=True)
