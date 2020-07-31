
#importing required modules

from flask import Flask #main flask modulw
from flask import render_template #to render html templates to the browser
from flask import request #to manage requests made by the browser
from uuid import uuid4 #to provide unique id to all data entries
from peewee import * #Mysql connector package
from hashlib import sha256 #hashing library to encrypt the passwords
import random #random library to random functions

db = MySQLDatabase('project', user = 'proj', password = 'password123*', host = '127.0.0.1')


#project
#proj
#password123*

#MySQL schema
class BaseModel(Model):
    class Meta:
        database = db

class games(BaseModel):
    #sql table thst stores the game info
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
    played = IntegerField(default = 0)
    win = FloatField(default = 100.0)
    
class students(BaseModel):
    #sql table that stores student values
    sid = CharField(primary_key = True, null = False)
    name = CharField(null = False)
    pas = CharField(null = False)
    email = CharField(null = False, unique = True)

class gameplayed(BaseModel):
    #sql table that stores game stats
    gid = CharField(null = True)
    sid = CharField(null = True)
    points = IntegerField(null = False)

class logged(BaseModel):
    #sql table to store current active student
    sid = CharField(null = False)

#function to create tables in the database
def create_tables():
    db.create_tables([games, students, gameplayed, logged])

#function to select a random question type
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


#routes
@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')
                
@app.route('/teacher')
def teacher():
    gameds = list(games.select()) #fetching the list of games
    gameplayeddata = list(gameplayed.select().order_by(-gameplayed.points)) #fetching game stats in descending 
    results = {} #initializing array for cleaner data\
    for j in gameds:
        results[j.gid] = []
    for i in range(len(gameplayeddata)):
        name = students.get(students.sid == gameplayeddata[i].sid).name
        k = {
            'name': name,
            'points': gameplayeddata[i].points,
        }
        results[gameplayeddata[i].gid].append(k)
    return render_template('teacher.html', games = gameds, umm = results)
    

@app.route('/register')
def register():
    return render_template('register.html', emailerr = '', passerr = '')

@app.route('/student')
def student():
    gameds = list(games.select()) #fetching the list of games
    gameplayeddata = list(gameplayed.select().order_by(-gameplayed.points)) #fetching game stats in descending 
    results = {} #initializing array for cleaner data
    for j in gameds:
        results[j.gid] = []
    for i in range(len(gameplayeddata)):
        name = students.get(students.sid == gameplayeddata[i].sid).name
        k = {
            'name': name,
            'points': gameplayeddata[i].points,
        }
        results[gameplayeddata[i].gid].append(k)
    return render_template('student.html', games = gameds, umm = results)

@app.route('/student/pastgames')
def pastgames():
    return render_template('pastgame.html')

@app.route('/teacher/createagame')
def createagame():
    return render_template('creategame.html')


#########################################################################################################
############################################## Logic routes #############################################
#########################################################################################################


@app.route('/loginLogic', methods = ['GET', 'POST'])
def loginLogic():
    #checking for the type of request
    if request.method == 'POST':
        data = request.form #getting the forma data from request
        #checking credentials
        if data['name'] == 'teacher@gmail.com' and data['password'] == 'teacher@123':
            return render_template('teacher.html')
        elif data['name'] == 'teacher@gmail.com' and data['password'] != 'teacher@123':
            return render_template('login.html', err = 'Incorrect password')
        else:
            try:
                user = students.get(students.email == data['name']) # getting student where email == the entered value
                if user.pas == sha256(data['password'].encode()).hexdigest():
                    try:
                        gameds = list(games.select()) #getting the list of games
                        ref = list(logged.select())[0].sid 
                        remove = logged.get(logged.sid == ref) #deleting the record of older loggedIn user
                        remove.delete_instance()
                    finally:
                        logged.create(
                            sid = user.sid
                        )
                        gameplayeddata = list(gameplayed.select().order_by(-gameplayed.points)) #getting game stats in descending order
                        results = {} #initializing array to store cleaner data
                        for j in gameds:
                            results[j.gid] = []
                        for i in range(len(gameplayeddata)):
                            name = students.get(students.sid == gameplayeddata[i].sid).name
                            k = {
                                'name': name,
                                'points': gameplayeddata[i].points,
                            }
                            results[gameplayeddata[i].gid].append(k)
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
                    gameds = list(games.select()) #getting the list of games
                    ref = list(logged.select())[0].sid 
                    remove = logged.get(logged.sid == ref) #deleting the record of older loggedIn user
                    remove.delete_instance()
                finally:
                    logged.create(
                        sid = sid
                    )
                    gameplayeddata = list(gameplayed.select().order_by(-gameplayed.points)) #getting game stats in descending order
                    results = {} #initializing empty array for cleaner data
                    for j in gameds:
                        results[j.gid] = []
                    for i in range(len(gameplayeddata)):
                        name = students.get(students.sid == gameplayeddata[i].sid).name
                        k = {
                            'name': name,
                            'points': gameplayeddata[i].points,
                        }
                        results[gameplayeddata[i].gid].append(k)
                return render_template('student.html', games = gameds, umm = results)
            except:
                return render_template('register.html', emailerr = 'Email id already exist', passerr = '')


@app.route('/deleteGame/<id>')
def deleteGame(id):
    ref = games.get(games.gid == id)
    dell = ref.delete_instance()
    gameds = list(games.select())
    gameplayeddata = list(gameplayed.select().order_by(-gameplayed.points))
    results = {}
    for j in gameds:
        results[j.gid] = []
    for i in range(len(gameplayeddata)):
        name = students.get(students.sid == gameplayeddata[i].sid).name
        k = {
            'name': name,
            'points': gameplayeddata[i].points,
        }
        results[gameplayeddata[i].gid].append(k)
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
        gameplayeddata = list(gameplayed.select().order_by(-gameplayed.points))
        results = {}
        for j in gameds:
            results[j.gid] = []
        for i in range(len(gameplayeddata)):
            name = students.get(students.sid == gameplayeddata[i].sid).name
            k = {
                'name': name,
                'points': gameplayeddata[i].points,
            }
            results[gameplayeddata[i].gid].append(k)
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
        gameplayeddata = list(gameplayed.select().order_by(-gameplayed.points))
        results = {}
        for j in gameds:
            results[j.gid] = []
        for i in range(len(gameplayeddata)):
            name = students.get(students.sid == gameplayeddata[i].sid).name
            k = {
                'name': name,
                'points': gameplayeddata[i].points,
            }
            results[gameplayeddata[i].gid].append(k)
        return render_template('student.html', games = gameds, umm = results)

@app.route('/gameStats')
def gameStats():
    gameds = list(games.select()) #getting list of games
    loggedUser = 'teach' #keeping the user logged
    gameplayeddata = list(gameplayed.select().order_by(-gameplayed.points)) #getting game stats in descending order
    results = {} #initailizing array for cleaner data
    for j in gameds:
        results[j.gid] = []
    for i in range(len(gameplayeddata)):
        name = students.get(students.sid == gameplayeddata[i].sid).name
        k = {
            'name': name,
            'points': gameplayeddata[i].points,
        }
        results[gameplayeddata[i].gid].append(k)
    return render_template('showgameslist.html', games = gameds, umm = results)


if __name__ == "__main__":
    db.connect()
    create_tables()
    app.run(debug=True)

