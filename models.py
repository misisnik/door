# todo - namontovat na to databazi, jen ciste jednuche logovani kdo kdy kde byl, kjak se oteviralo a jak to vlastne funguje a je to, teoreticky se muze
# logovat i otevriani dverim pomoci toho senzoru co je na dverich -- musi se to promeri !!!!
import datetime
import sqlite3
import sys
import json
import os

_PATH = os.path.dirname(os.path.realpath(__file__))

class Database(object):
    """docstring for Database."""
    def __init__(self, db_name = 'dvere.db'):
        if db_name == 'dvere.db':
            self.db_path_name = '{}/{}'.format(_PATH, db_name)
        else:
            self.db_path_name = db_name

        self.db_name = db_name
        self.create_tables()
        # set tables
        self.events = Events(self.db_path_name)
        self.users = Users(self.db_path_name)

    def create_tables(self):
        try:
            with sqlite3.connect(self.db_path_name, detect_types=sqlite3.PARSE_DECLTYPES ) as db:
                cur = db.cursor()
                cur.execute("""CREATE TABLE events
                                ( id INTEGER PRIMARY KEY AUTOINCREMENT
                                , type          INTEGER
                                , dt            DATETIME) """)

                cur.execute("""CREATE TABLE users
                                ( id   INTEGER PRIMARY KEY AUTOINCREMENT
                                , name  TEXT
                                , passwd TEXT
                                , last_time DATETIME)""")
        except Exception as e:
            # tables already exist
            pass

class Events(object):
    """eventst table class."""
    def __init__(self, db_name):
        self.db_path_name = db_name
        self.name = 'events'

    def send_query(self, query):
        with sqlite3.connect(self.db_path_name, detect_types=sqlite3.PARSE_DECLTYPES ) as db:
            cur = db.cursor()
            return cur.execute(query)

    def insert(self, type):
        dt = datetime.datetime.now().isoformat()
        query = "INSERT INTO {} VALUES (NULL, '{}', '{}')".format(self.name, type, dt)
        return self.send_query(query)

    def getAll(self):
        query = "SELECT * FROM {} ORDER BY id DESC".format(self.name)
        return self.send_query(query)

    def delete(self):
        pass

    def update(self):
        pass

class Users(object):
    """eventst table class."""
    def __init__(self, db_name):
        self.db_path_name = db_name
        self.name = 'users'

    def send_query(self, query):
        with sqlite3.connect(self.db_path_name, detect_types=sqlite3.PARSE_DECLTYPES ) as db:
            cur = db.cursor()
            return cur.execute(query)

    def insert(self, name, passwd):
        dt = datetime.datetime.now().isoformat()
        query = "INSERT INTO {} VALUES (NULL, '{}', '{}', '{}')".format(self.name, name, passwd, dt)
        return self.send_query(query)

    def get(self):
        query = "SELECT * FROM {} ORDER BY id DESC".format(self.name)
        return self.send_query(query)

    def delete(self):
        pass

    def update(self):
        pass
