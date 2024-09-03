import sqlite3
connection = sqlite3.connect('Database.db')
currsor = connection.cursor()

def get_connection():
    return connection

def close_connection():
    connection.close()