from datetime import datetime

from peewee import *


db = SqliteDatabase('data/lws.db')


class User(Model):
    username = CharField()
    password = CharField()
    address = CharField()
    view_key = CharField()
    date = DateTimeField(default=datetime.utcnow)

    class Meta:
        database = db


db.create_tables([User])
