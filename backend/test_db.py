import sqlite3

con = sqlite3.connect("taskdb.db")
cur = con.cursor()

print(cur.fetchall())
