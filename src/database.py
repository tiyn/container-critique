from datetime import date as dt
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


class User():

    def __init__(self, name, pass_hash=None):
        self.name = name
        self.id = None
        self.is_active = True
        self.is_authenticated = True
        self.is_anonymous = False
        self.pass_hash = pass_hash

    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def set_id(self, ident):
        self.id = ident

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)

    def get_id(self):
        return self.id


class Item():

    def __init__(self, name, date):
        self.name = name
        self.date = date
        self.id = None

    def set_id(self, ident):
        self.id = ident


class Entry():

    def __init__(self, text, rating, reviewed):
        self.text = text
        self.rating = rating
        self.reviewed = reviewed
        self.item = None
        self.user = None

    def set_id(self, ident):
        self.id = ident

    def set_item(self, item):
        self.item = item

    def set_user(self, user):
        self.user = user


class Database:

    def __init__(self):
        self.USER_TABLE_FILE = 'USERS'
        self.ENTRY_TABLE_FILE = 'ENTRIES'
        self.ITEM_TABLE_FILE = 'ITEMS'
        self.DB_DIR = os.path.dirname("./data/")
        self.setup_db()

    def connect(self):
        """
        Connect to an existing database instance based on the object
        attributes.
        """
        path = os.path.join(self.DB_DIR, "data.db")
        return sqlite3.connect(path)

    def setup_db(self):
        """Creates a database with tables."""
        db = self.connect()
        crs = db.cursor()
        query = "CREATE TABLE IF NOT EXISTS " + self.USER_TABLE_FILE + \
            "(id INTEGER PRIMARY KEY AUTOINCREMENT," + \
            "name CHAR(32) NOT NULL UNIQUE," + \
            "password CHAR(32) NOT NULL)"
        crs.execute(query)
        query = "CREATE TABLE IF NOT EXISTS " + self.ITEM_TABLE_FILE + \
            "(id INTEGER PRIMARY KEY AUTOINCREMENT," + \
            "name CHAR(32) NOT NULL," + \
            "date CHAR(4)," + \
            "UNIQUE(date, name))"
        crs.execute(query)
        query = "CREATE TABLE IF NOT EXISTS " + self.ENTRY_TABLE_FILE + \
            "(id INTEGER PRIMARY KEY AUTOINCREMENT," + \
            "item_id INTEGER NOT NULL REFERENCES " + self.ITEM_TABLE_FILE + "(id)," + \
            "text TEXT NOT NULL," + \
            "rating INTEGER NOT NULL," +\
            "user_id INTEGER REFERENCES " + self.USER_TABLE_FILE + "(id),"\
            "reviewed CHAR(10) NOT NULL)"
        crs.execute(query)
        db.commit()

    def insert_user(self, username, password):
        pass_hash = generate_password_hash(password)
        if self.get_user_by_name(username) is None and pass_hash is not None:
            db = self.connect()
            crs = db.cursor()
            query = "INSERT INTO " + self.USER_TABLE_FILE + \
                    "(`name`,`password`)" + \
                    "VALUES (?, ?) ON CONFLICT DO NOTHING"
            crs.execute(query, (username, pass_hash))
            db.commit()
            return crs.lastrowid
        return None

    def insert_entry(self, name, date, text, rating, user_id=None):
        db = self.connect()
        crs = db.cursor()
        query = "INSERT OR IGNORE INTO " + self.ITEM_TABLE_FILE + \
            "(`name`,`date`)" + "VALUES (?, ?)"
        crs.execute(query, (name, date))
        query = "SELECT id FROM " + self.ITEM_TABLE_FILE + \
            " WHERE name = ? AND date = ?"
        crs.execute(query, (name, date))
        item_id = crs.fetchone()[0]
        reviewed = dt.today().strftime('%Y-%m-%d')
        query = "INSERT INTO " + self.ENTRY_TABLE_FILE + \
            "(`item_id`, `text`, `rating`, `user_id`, `reviewed`)" + \
            "VALUES (?, ?, ?, ?, ?)"
        crs.execute(query, (item_id, text, rating, user_id, reviewed))
        db.commit()
        return crs.lastrowid

    def delete_entry(self, ident):
        db = self.connect()
        crs = db.cursor()
        query = "DELETE FROM " + self.ENTRY_TABLE_FILE + " WHERE id = ?"
        crs.execute(query, (ident, ))
        db.commit()
        return crs.lastrowid

    def get_entries(self):
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.ENTRY_TABLE_FILE
        crs.execute(query)
        res = []
        for item in crs.fetchall():
            res.append(self.db_to_entry(*item))
        return res

    def get_entry_by_id(self, ident):
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.ENTRY_TABLE_FILE + " WHERE id = ?"
        crs.execute(query, (ident, ))
        fetched = crs.fetchone()
        if fetched is None:
            return None
        else:
            return self.db_to_entry(*fetched)

    def get_entries_by_user(self, name):
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.ENTRY_TABLE_FILE + \
                " WHERE user_id = (SELECT id FROM " + self.USER_TABLE_FILE + \
                " WHERE name = ?)"
        crs.execute(query, (name, ))
        res = []
        for item in crs.fetchall():
            res.append(self.db_to_entry(*item))
        return res

    def get_item_by_id(self, ident):
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.ITEM_TABLE_FILE + " WHERE id = ?"
        crs.execute(query, (ident, ))
        fetched = crs.fetchone()
        if fetched is None:
            return None
        else:
            return self.db_to_item(*fetched)

    def get_user_by_id(self, ident):
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.USER_TABLE_FILE + " WHERE id = ?"
        crs.execute(query, (ident, ))
        fetched = crs.fetchone()
        if fetched is None:
            return None
        else:
            return self.db_to_user(*fetched)

    def get_user_by_name(self, name):
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.USER_TABLE_FILE + " WHERE name = ?"
        crs.execute(query, (name, ))
        fetched = crs.fetchone()
        if fetched is None:
            return None
        else:
            return self.db_to_user(*fetched)

    def db_to_user(self, ident, name, pass_hash):
        user = User(name, pass_hash)
        user.set_id(ident)
        return user

    def db_to_item(self, ident, name, date):
        item = Item(name, date)
        item.set_id(ident)
        return item

    def db_to_entry(self, ident, item_id, text, rating, user_id, reviewed):
        entry = Entry(text, rating, reviewed)
        entry.set_id(ident)
        entry.set_item(self.get_item_by_id(item_id))
        entry.set_user(self.get_user_by_id(user_id))
        return entry
