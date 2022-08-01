from datetime import date as dt
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


class User():

    def __init__(self, name, pass_hash=None):
        self.name = name
        self.id = 0
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


class Database:

    def __init__(self):
        self.USER_TABLE_FILE = 'USERS'
        self.ENTRY_TABLE_FILE = 'ENTRIES'
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
        query = "CREATE TABLE IF NOT EXISTS " + self.ENTRY_TABLE_FILE + \
            "(id INTEGER PRIMARY KEY AUTOINCREMENT," + \
            "name CHAR(64) NOT NULL," + \
            "date CHAR(4) NOT NULL," + \
            "text TEXT NOT NULL," + \
            "rating INTEGER NOT NULL," +\
            "user_id INTEGER," +\
            "reviewed CHAR(10) NOT NULL," +\
            "FOREIGN KEY(user_id) REFERENCES " + self.USER_TABLE_FILE + "(id))"
        crs.execute(query)
        db.commit()

    def insert_user(self, user):
        if self.check_user_name(user.name) and user.pass_hash is not None:
            db = self.connect()
            crs = db.cursor()
            query = "INSERT INTO " + self.USER_TABLE_FILE + \
                    "(`name`,`password`)" + \
                    "VALUES (?, ?) ON CONFLICT DO NOTHING"
            crs.execute(query, (user.name, user.pass_hash))
            db.commit()
            return crs.lastrowid
        return None

    def insert_entry(self, name, date, text, rating, user_id=None):
        db = self.connect()
        crs = db.cursor()
        reviewed = dt.today().strftime('%Y-%m-%d')
        query = "INSERT INTO " + self.ENTRY_TABLE_FILE + \
            "(`name`,`date`, `text`, `rating`, `user_id`, `reviewed`)" + \
            "VALUES (?, ?, ?, ?, ?, ?)"
        crs.execute(query, (name, date, text, rating, user_id, reviewed))
        db.commit()
        return crs.lastrowid

    def check_user_name(self, name):
        if self.get_user_by_name(name) is None:
            return True
        return False

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
        return crs.fetchall()

    def get_entries_by_name(self, name):
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.ENTRY_TABLE_FILE + \
                " WHERE user_id = (SELECT id FROM " + self.USER_TABLE_FILE + \
                " WHERE name = ?)"
        crs.execute(query, (name, ))
        return crs.fetchall()

    def get_entry_by_id(self, ident):
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.ENTRY_TABLE_FILE + " WHERE id = ?"
        crs.execute(query, (ident, ))
        return crs.fetchone()

    def get_user_by_id(self, ident):
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.USER_TABLE_FILE + " WHERE id = ?"
        crs.execute(query, (ident, ))
        return crs.fetchone()

    def get_user_by_name(self, name):
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.USER_TABLE_FILE + " WHERE name = ?"
        crs.execute(query, (name, ))
        return crs.fetchone()

    def db_to_user(self, ident, name, pass_hash):
        user = User(name, pass_hash)
        user.set_id(ident)
        return user
