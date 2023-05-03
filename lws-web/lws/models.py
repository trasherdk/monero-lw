from datetime import datetime

import requests
from peewee import *
from playhouse.sqliteq import SqliteQueueDatabase

from lws import config


db = SqliteQueueDatabase('data/lws-web.db')


class User(Model):
    username = CharField()
    password = CharField()
    address = CharField()
    view_key = CharField()
    date = DateTimeField(default=datetime.utcnow)

    class Meta:
        database = db


class Wallet(Model):
    name = CharField(unique=True)
    description = TextField(default="")
    address = CharField(unique=True)
    view_key = CharField(unique=True)
    restore_height = IntegerField()
    added = BooleanField(default=False)
    date = DateTimeField(default=datetime.utcnow)
    date_added = DateTimeField(null=True)
    user = ForeignKeyField(User, backref="wallets")

    def check_wallet_lws(self):
        endpoint = f"{config.LWS_ADMIN_URL}/list_accounts"
        data = {
            "auth": self.user.view_key, 
            "params": {}
        }
        try:
            req = requests.post(endpoint, json=data, timeout=5)
            req.raise_for_status()
            if req.ok:
                res = req.json()
                for _status in res:
                    for _wallet in res[_status]:
                        if _wallet["address"] == self.address:
                            self.added = True
                            self.save()
                            return True
                return False
            return False
        except Exception as e:
            print(f"Failed to list wallets: {e}")
            return False

    def add_wallet_lws(self):
        endpoint = f"{config.LWS_ADMIN_URL}/add_account"
        data = {
            "auth": self.user.view_key, 
            "params": {
                "address": self.address, 
                "key": self.view_key
            }
        }
        try:
            req = requests.post(endpoint, json=data, timeout=5)
            req.raise_for_status()
            if req.ok:
                self.added = True
                self.date_added = datetime.utcnow()
                self.save()
                return True
            return False
        except Exception as e:
            print(f"Failed to add wallet {self.address}: {e}")
            return False
    
    def get_wallet_info(self):
        endpoint = f"{config.LWS_URL}/get_address_info"
        data = {
            "address": self.address, 
            "view_key": self.view_key
        }
        try:
            req = requests.post(endpoint, json=data, timeout=5)
            req.raise_for_status()
            if req.ok:
                return req.json()
            return {}
        except Exception as e:
            print(f"Failed to get wallet info {self.address}: {e}")
            return False
    
    def rescan(self):
        endpoint = f"{config.LWS_ADMIN_URL}/rescan"
        data = {
            "auth": self.user.view_key, 
            "params": {
                "height": self.restore_height, 
                "addresses": [self.address]
            }
        }
        try:
            req = requests.post(endpoint, json=data, timeout=5)
            req.raise_for_status()
            if req.ok:
                print(r.content)
                return True
            return False
        except Exception as e:
            print(f"Failed to add wallet {self.address}: {e}")
            return False
    
    class Meta:
        database = db


db.create_tables([User, Wallet])