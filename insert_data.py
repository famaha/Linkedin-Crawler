
import sqlite3
from wsproto import connection

class database:

    def connection(self) :
        
        # Connecting to sqlite
        self.conn = sqlite3.connect('Linkedin.db')
        # Creating a cursor object using the
        self.cursor = self.conn.cursor()
        # Creating table
        return self.cursor

    def insert(self,name,location,about):
        self.connection()
        self.table = """
      CREATE TABLE IF NOT EXISTS CRAWLER (
      NAME VARCHAR(255),
      LOCATION VARCHAR(255),
      ABOUT VARCHAR(255))"""
        self.cursor.execute(self.table)
        # Queries to INSERT records.
        self.cursor.execute('''INSERT INTO CRAWLER (NAME,LOCATION,ABOUT) VALUES(?,?,?)''',(name,location,about))
        # Commit your changes in the database	
        self.conn.commit()

    def close(self):
        # Closing the connection
        self.conn.close()

