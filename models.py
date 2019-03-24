# todo - namontovat na to databazi, jen ciste jednuche logovani kdo kdy kde byl, kjak se oteviralo a jak to vlastne funguje a je to, teoreticky se muze
# logovat i otevriani dverim pomoci toho senzoru co je na dverich -- musi se to promeri !!!!


import sqlite3
import sys
import json
import os

_PATH = os.path.dirname(os.path.realpath(__file__))

class Database(object):
    """docstring for Database."""
    def __init__(self, db_name = 'mantag.db'):
        if db_name == 'mantag.db':
            self.db_path_name = '{}/{}'.format(_PATH, db_name)
        else:
            self.db_path_name = db_name

        self.db_name = db_name
        self.create_tables()
        # set tables
        self.measurement = Measurement(self.db_path_name)
        self.device = Device(self.db_path_name)
        self.layers = Layers(self.db_path_name)

    def create_tables(self):
        try:
            with sqlite3.connect(self.db_path_name, detect_types=sqlite3.PARSE_DECLTYPES ) as db:
                cur = db.cursor()
                cur.execute("""CREATE TABLE layers
                                ( id INTEGER PRIMARY KEY AUTOINCREMENT
                                , type          TEXT
                                , name          TEXT
                                , position      TEXT
                                , description   TEXT)""")

                cur.execute("""CREATE TABLE device
                                ( id   INTEGER PRIMARY KEY AUTOINCREMENT
                                , mac  TEXT
                                , name TEXT
                                , last_time DATETIME
                                , last_position TEXT
                                , zones TEXT
                                , CONSTRAINT mac_unique UNIQUE (mac) )""")

                cur.execute("""CREATE TABLE wifi
                                ( id   INTEGER PRIMARY KEY AUTOINCREMENT
                                , data TEXT )""")

                cur.execute("""CREATE TABLE mag
                                ( id INTEGER PRIMARY KEY AUTOINCREMENT
                                , data TEXT )""")

                cur.execute("""CREATE TABLE acc
                                ( id INTEGER PRIMARY KEY AUTOINCREMENT
                                , data TEXT )""")

                cur.execute("""CREATE TABLE measurement
                                ( id INTEGER PRIMARY KEY AUTOINCREMENT
                                , timestamp DATETIME
                                , location TEXT
                                , dev_id   INTEGER
                                , wifi_id   INTEGER
                                , mag_id   INTEGER
                                , acc_id   TEXT
                                , FOREIGN KEY(dev_id) REFERENCES device(id)
                                , FOREIGN KEY(wifi_id) REFERENCES wifi(id)
                                , FOREIGN KEY(mag_id) REFERENCES mag(id) )""")

        except Exception as e:
            # tables already exist
            pass

class Measurement(object):
    """measurement table class."""
    def __init__(self, db_name):
        self.db_path_name = db_name
        self.name = 'measurement'

    def send_query(self, query):
        with sqlite3.connect(self.db_path_name, detect_types=sqlite3.PARSE_DECLTYPES ) as db:
            cur = db.cursor()
            return cur.execute(query)

    def insert(self, timestamp, location, tag, wifi, magnetometer, acc = []):
        wifi = json.dumps(wifi)

        # if magnetometer is array needs to be put every peace of it
        # mag = json.dumps(magnetometer)
        loc = json.dumps(location)
        # put wifi data
        query = "INSERT INTO wifi VALUES (NULL, '{}')".format(wifi)
        wifi_id = self.send_query(query).lastrowid

        # put defice if not exist
        query = "SELECT id FROM device WHERE mac = '{}'".format(tag)
        t = self.send_query(query).fetchone()
        if t == None:
            query = "INSERT INTO device VALUES (NULL, '{}', '{}', '{}', '{}')".format( tag
                                                                   , '', timestamp, loc)
            t = self.send_query(query).lastrowid
        else:
            t = t[0]

        for c, mag in enumerate(magnetometer):
            # put mag data
            query = "INSERT INTO mag VALUES (NULL, '{}')".format(json.dumps(mag))
            mag_id = self.send_query(query).lastrowid

            add_id = None
            if acc != []:
                query = "INSERT INTO acc VALUES (NULL, '{}')".format(json.dumps(acc[c]))
                acc_id = self.send_query(query).lastrowid

            query = "INSERT INTO {} VALUES (NULL, '{}', '{}', '{}', {}, {})".format(\
                                                    self.name, timestamp, loc,
                                                     t, wifi_id, mag_id )
            last = self.send_query(query)
        return last

    def get(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

class Device(object):
    """docstring for Device."""
    def __init__(self, db_name):
        self.db_path_name = db_name
        self.name = 'device'

    def send_query(self, query):
        with sqlite3.connect(self.db_path_name, detect_types=sqlite3.PARSE_DECLTYPES ) as db:
            cur = db.cursor()
            return cur.execute(query)

    def insert(self, mac, name, last_time, last_position, zones = '[]'):
        query = "INSERT INTO {} VALUES (NULL, '{}', '{}', '{}', '{}', '{}')".format(\
                                                self.name, mac, name, last_time, last_position, zones)
        return self.send_query(query)

    def get( self
           , ide = None
           , mac = None ):
        if mac:
            query = "SELECT * FROM {} WHERE mac = '{}'".format(self.name, mac)
        else:
            query = "SELECT * FROM {}".format(self.name)
        return self.send_query(query)

    def update( self
              , ide = None
              , mac = None
              , name = None
              , last_time = None
              , last_position =  None
              , zones = None ):
        pre_query = []
        if ide == None and mac == none:
            return False

        if mac != None and ide != None:
            pre_query.append("mac = '{}'".format(mac))
        if name != None:
            pre_query.append("name = '{}'".format(name))
        if last_time != None:
            pre_query.append("last_time = '{}'".format(last_time))
        if last_position != None:
            pre_query.append("last_position = '{}'".format(last_position))
        if zones != None:
            pre_query.append("zones = '{}'".format(zones))

        if ide != None:
            where = "id = {}".format(ide)
        else:
            where = "mac = '{}'".format(mac)

        query = "UPDATE {} SET {}  WHERE {}".format(self.name, ', '.join(pre_query), where)
        return self.send_query(query)

    def delete(self, ide):
        query = "DELETE FROM {} WHERE id = {}".format(self.name, ide)
        return self.send_query(query)

class Layers(object):
    """docstring for Layers."""
    def __init__(self, db_name):
        self.db_path_name = db_name
        self.name = 'layers'
        # check if zeros exist - if is not blank database
        # if not just add new zeros on 0,0
        zeros = self.get(type='zeros').fetchall()
        if not len(zeros):
            self.insert('zeros', 'zeros', json.dumps([0, 0]), '')

    def send_query(self, query):
        with sqlite3.connect(self.db_path_name, detect_types=sqlite3.PARSE_DECLTYPES ) as db:
            cur = db.cursor()
            return cur.execute(query)

    def insert(self, type, name, position, description):
        query = "INSERT INTO {} VALUES (NULL, '{}', '{}', '{}', '{}')".format(\
                                                self.name, type, name, position, description)
        return self.send_query(query)

    def get( self
           , ide = None
           , type = 'zone' ):
        if ide:
            query = "SELECT * FROM {} WHERE id = '{}' && type = '{}'".format(self.name, ide, type)
        else:
            query = "SELECT * FROM {} WHERE type = '{}'".format(self.name, type)
        return self.send_query(query)

    def update( self
              , ide = None
              , name = None
              , position = None
              , description =  None ):
        pre_query = []
        if ide == None:
            return False

        if name != None:
            pre_query.append("name = '{}'".format(name))
        if position != None:
            pre_query.append("position = '{}'".format(position))
        if description != None:
            pre_query.append('description = "{}"'.format(description.replace('"', '""')))

        query = "UPDATE {} SET {}  WHERE id = {}".format(self.name, ', '.join(pre_query), ide)
        return self.send_query(query)

    def delete(self, ide):
        query = "DELETE FROM {} WHERE id = {}".format(self.name, ide)
        return self.send_query(query)
