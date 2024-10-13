import sqlite3
import os


project_directory = os.path.dirname(os.path.abspath(__file__))
ADDRESS = os.path.join(project_directory, 'Database.db')
connection = sqlite3.connect(ADDRESS,check_same_thread=False)
currsor = connection.cursor()

def get_connection():
    return connection

def close_connection():
    connection.close()