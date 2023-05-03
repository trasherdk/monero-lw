from datetime import datetime

from peewee import *
from playhouse.sqliteq import SqliteQueueDatabase


db = SqliteQueueDatabase('chat.db')


class Message(Model):
    message = CharField()
    datestamp = DateTimeField(default=datetime.utcnow)

    class Meta:
        database = db


db.create_tables([Message])