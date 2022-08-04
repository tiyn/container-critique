from datetime import date as dt
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


class User():
    """
    A class to represent a user.

    Attributes:
    name (str): name of the user
    id (int): id of the user
    is_active (bool): check if the user is active
    is_authenticated (bool): check if the user is logged in
    is_anonymous (bool): check if the user is is_anonymous
    pass_hash (str): hash of the users password
    """

    def __init__(self, name, pass_hash=None):
        self.name = name
        self.id = None
        self.is_active = True
        self.is_authenticated = True
        self.is_anonymous = False
        self.pass_hash = pass_hash

    def set_password(self, password):
        """
        Set the password hash of the user from a password.

        Parameters:
        password (str): password to add to the user

        Returns:
        None
        """
        self.pass_hash = generate_password_hash(password)

    def set_id(self, ident):
        """
        Set the id of the user.

        Parameters:
        id (str): id to add to the user

        Returns:
        None
        """
        self.id = ident

    def check_password(self, password):
        """
        Check if a given password matches the one of the users by comparing the
        hashes.

        Parameters:
        password (str): password to compare the users password to

        Returns:
        bool: True if it matches the users password, False otherwise
        """
        return check_password_hash(self.pass_hash, password)

    def get_id(self):
        """
        Get the id of the user.

        Returns:
        int: id of the user
        """
        return self.id


class Item():
    """
    A class to represent an item.

    Attributes:
    name (str): name of the item
    id (int): id of the item
    date (str): date the item was created
    """

    def __init__(self, name, date):
        self.name = name
        self.date = date
        self.id = None

    def set_id(self, ident):
        """
        Set the id of the item.

        Returns:
        int: id of the item
        """
        self.id = ident


class Entry():
    """
    A class to represent an entry.

    Attributes:
    text (str): text of the entry
    rating (int): rating of the item
    date (str): date the entry was created
    item (Item): item that is referenced by the entry
    user (User): user that authored the entry
    id (int): id of the item
    """

    def __init__(self, text, rating, date):
        self.text = text
        self.rating = rating
        self.date = date
        self.item = None
        self.user = None

    def set_id(self, ident):
        """
        Set the id of the entry.

        Parameters:
        ident(int): id of the entry
        """
        self.id = ident

    def set_item(self, item):
        """
        Set the item of the entry.

        Parameters:
        item(Item): item of the entry
        """
        self.item = item

    def set_user(self, user):
        """
        Set the user of the entry.

        Parameters:
        user(User): user of the entry
        """
        self.user = user


class Database:
    """
    A class to represent an entry.

    Attributes:
    USER_TABLE_FILE (str): name of the user table
    ENTRY_TABLE_FILE (str): name of the entry table
    ITEM_TABLE_FILE (str): name of the item table
    DB_DIR(PathLike): path that leads to the directory containing the database
    """

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

        Return:
        Connection: connection to the database
        """
        path = os.path.join(self.DB_DIR, "data.db")
        return sqlite3.connect(path)

    def setup_db(self):
        """
        Creates a database with the needed tables if it doesn't already exits.
        """
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
            "date CHAR(10) NOT NULL)"
        crs.execute(query)
        db.commit()

    def insert_user(self, username, password):
        """
        Insert a row in the user table.

        Parameters:
        username (str): name of the user to add
        password (str): password of the user to add

        Returns:
        int: number of the line the row was added, None if it wasn't successful
        """
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
        """
        Insert a row in the entry table.

        Parameters:
        name (str): name of the entry to add
        date (str): date of the entry to add
        text (str): text of the entry to add
        rating (str): rating of the entry to add
        user_id (int): id of the user referenced by the entry to add

        Returns:
        int: number of the line the row was added
        """
        db = self.connect()
        crs = db.cursor()
        query = "INSERT OR IGNORE INTO " + self.ITEM_TABLE_FILE + \
            "(`name`,`date`)" + "VALUES (?, ?)"
        crs.execute(query, (name, date))
        query = "SELECT id FROM " + self.ITEM_TABLE_FILE + \
            " WHERE name = ? AND date = ?"
        crs.execute(query, (name, date))
        item_id = crs.fetchone()[0]
        date = dt.today().strftime('%Y-%m-%d')
        query = "INSERT INTO " + self.ENTRY_TABLE_FILE + \
            "(`item_id`, `text`, `rating`, `user_id`, `date`)" + \
            "VALUES (?, ?, ?, ?, ?)"
        crs.execute(query, (item_id, text, rating, user_id, date))
        db.commit()
        return crs.lastrowid

    def delete_entry(self, ident):
        """
        Delete a row from the entry table based on the entrys id.

        Parameters:
        ident (int): id of the entry to remove

        Returns:
        int: number of the line the row was removed from
        """
        db = self.connect()
        crs = db.cursor()
        query = "DELETE FROM " + self.ENTRY_TABLE_FILE + " WHERE id = ?"
        crs.execute(query, (ident, ))
        db.commit()
        return crs.lastrowid

    def get_entries(self):
        """
        Return all the entries stored in the database.

        Return:
        List(Entry): list of entries in database
        """
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.ENTRY_TABLE_FILE
        crs.execute(query)
        res = []
        for item in crs.fetchall():
            res.append(self.entry_from_db(*item))
        return res

    def get_entry_by_id(self, ident):
        """
        Return an entry stored in the database based on the entrys id.

        Parameters:
        ident (int): id of the entry to return

        Returns:
        Entry: entry that matched the given id
        """
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.ENTRY_TABLE_FILE + " WHERE id = ?"
        crs.execute(query, (ident, ))
        fetched = crs.fetchone()
        if fetched is None:
            return None
        else:
            return self.entry_from_db(*fetched)

    def get_entries_by_username(self, username):
        """
        Return a entries stored in the database based on the entries name.

        Parameters:
        username (str): name of the entries to return

        Returns:
        List(Entry): entries that matched the given name
        """
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.ENTRY_TABLE_FILE + \
                " WHERE user_id = (SELECT id FROM " + self.USER_TABLE_FILE + \
                " WHERE name = ?)"
        crs.execute(query, (username, ))
        res = []
        for item in crs.fetchall():
            res.append(self.entry_from_db(*item))
        return res

    def get_item_by_id(self, ident):
        """
        Return an item stored in the database based on the items id.

        Parameters:
        ident (int): id of the item to return

        Returns:
        Item: item that matched the given id
        """
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.ITEM_TABLE_FILE + " WHERE id = ?"
        crs.execute(query, (ident, ))
        fetched = crs.fetchone()
        if fetched is None:
            return None
        else:
            return self.item_from_db(*fetched)

    def get_user_by_id(self, ident):
        """
        Return a user stored in the database based on the users id.

        Parameters:
        ident (int): id of the user to return

        Returns:
        Item: user that matched the given id
        """
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.USER_TABLE_FILE + " WHERE id = ?"
        crs.execute(query, (ident, ))
        fetched = crs.fetchone()
        if fetched is None:
            return None
        else:
            return self.user_from_db(*fetched)

    def get_user_by_name(self, name):
        """
        Return a user stored in the database based on the user name.

        Parameters:
        name (str): name of the user to return

        Returns:
        Entry: user that matched the given name
        """
        db = self.connect()
        crs = db.cursor()
        query = "SELECT * FROM " + self.USER_TABLE_FILE + " WHERE name = ?"
        crs.execute(query, (name, ))
        fetched = crs.fetchone()
        if fetched is None:
            return None
        else:
            return self.user_from_db(*fetched)

    def user_from_db(self, ident, name, pass_hash):
        """
        Return a user from given database parameters.

        Parameters:
        ident: id of the user
        name: text of the user
        pass_hash: password hash of the user

        Returns:
        User: user element with given variables
        """
        user = User(name, pass_hash)
        user.set_id(ident)
        return user

    def item_from_db(self, ident, name, date):
        """
        Return an item from given database parameters.

        Parameters:
        ident: id of the item
        name: text of the item
        date: date of the day the item was created

        Returns:
        Item: entry element with given variables
        """
        item = Item(name, date)
        item.set_id(ident)
        return item

    def entry_from_db(self, ident, item_id, text, rating, user_id, date):
        """
        Return an entry from given database parameters.

        Parameters:
        ident: id of the entry
        item_id: id of the referenced item
        text: text of the entry
        rating: rating of the entry
        user_id: id of the user that authored the entry
        date: date of the day the entry was written

        Returns:
        Entry: entry element with given variables
        """
        entry = Entry(text, rating, date)
        entry.set_id(ident)
        entry.set_item(self.get_item_by_id(item_id))
        entry.set_user(self.get_user_by_id(user_id))
        return entry
