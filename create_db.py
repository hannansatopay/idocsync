import sqlite3

conn = sqlite3.connect('data.db')
print("Opened database successfully");

conn.execute('''CREATE TABLE DATA
         (ID TEXT PRIMARY KEY      NOT NULL,
         TIMESTAMP          INT    NOT NULL,
         CONTENT            TEXT     NOT NULL,
         UPDATE_TIME          INT    NOT NULL);''')
print("Table created successfully");

conn.close()
