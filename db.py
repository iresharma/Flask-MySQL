from peewee import *

class BaseModel(Model):
    class Meta:
        database = db

class games:
    gid = CharField(primary_key = True, null = False)
    name = CharField(null = False)
    x_value = IntegerField(null = False)
    o_value = IntegerField(null = False)
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
    
class students:
    sid = CharField(primary_key = True, null = False)
    name = CharField(null = False)
    pas = CharField(null = False)
    win = CharField(null = False)
    
class gamesPlayed:
    gid = IntegerField(null = False)
    sid = IntegerField(null = False)
    result = BooleanField(null = False)
    gsid = CharField(primary_key = True, null = False)

def create_tables():
with database:
    database.create_tables([games, students, gamesPlayed])
