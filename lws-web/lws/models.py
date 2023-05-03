from datetime import datetime

from peewee import *
from playhouse.sqliteq import SqliteQueueDatabase


db = SqliteQueueDatabase('data/lws-web.db')


class Admin(Model):
    username = CharField()
    password = CharField()
    address = CharField()
    view_key = CharField()
    date = DateTimeField(default=datetime.utcnow)

    class Meta:
        database = db


class Wallet(Model):
    name = CharField()
    description = TextField()
    address = CharField()
    view_key = CharField()
    restore_height = IntegerField()
    date = DateTimeField(default=datetime.utcnow)

    class Meta:
        database = db


db.create_tables([Admin, Wallet])