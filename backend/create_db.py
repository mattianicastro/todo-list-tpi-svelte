import sqlite3

con = sqlite3.connect("taskdb.db")
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")
cur.execute(
    """
CREATE TABLE IF NOT EXISTS users(
    user_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    pic_url TEXT NOT NULL
);
"""
)
cur.execute(
    """
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT 0,
    user_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
"""
)
con.commit()
