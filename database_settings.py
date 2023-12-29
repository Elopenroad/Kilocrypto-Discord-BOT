from peewee import *


db = SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    ids = CharField(primary_key=True)
    username = CharField(max_length=500)
    trial_expiration = DateTimeField(null=True)  # Add a new field for trial expiration
    

class Coins(BaseModel):
    coin_name = CharField(max_length=200)
    changes = FloatField(default=0)
    active = BooleanField(default=False)
    lastminutechanges = FloatField(default=0)


db.connect()
db.create_tables([User , Coins])

