import os
import sqlite3

from login import User


class Database:

    def __init__(self):
        self.TABLE_FILE = 'USERS'
        self.DB_DIR = os.path.dirname(".")
        self.setup_db()

    def connect(self):
        """Connect to an existing database instance based on the object
        attributes.
        """
        path = os.path.join(self.DB_DIR, "data.db")
        return sqlite3.connect(path)

    def setup_db(self):
        """Creates a database with tables."""
        db = self.connect()
        crs = db.cursor()
        query = "CREATE TABLE IF NOT EXISTS " + self.TABLE_FILE + \
            "(id INTEGER PRIMARY KEY AUTOINCREMENT," + \
            "name CHAR(32) NOT NULL UNIQUE," + \
            "password CHAR(32) NOT NULL)"
        crs.execute(query)

    def insert_user(self, name, password):
        """Insert a new user into the database.
        """
        if self.check_name(name):
            db = self.connect()
            crs = db.cursor()
            query = "INSERT INTO " + self.TABLE_FILE + "(`name`,`password`)" + \
                    "VALUES (?, ?) ON CONFLICT DO NOTHING"
            crs.execute(query, (name, password))
            db.commit()
            return True
        return False

    def check_name(self, name):
        if self.get_by_name(name) is None:
            return True
        return False

    def get_by_id(self, ident):
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.TABLE_FILE + " WHERE id = ?"
        crs.execute(query, (ident, ))
        return crs.fetchone()

    def get_by_name(self, name):
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.TABLE_FILE + " WHERE name = ?"
        crs.execute(query, (name, ))
        return crs.fetchone()

    def db_to_user(self, ident, name, pass_hash):
        user = User(name, pass_hash)
        user.set_id(ident)
        return user
