import sqlite3


def get_cursor():
    con = sqlite3.connect("taskdb.db")
    cur = con.cursor()
    return cur


class User:
    def __init__(self, user_id, username, pic_url):
        self.id = user_id
        self.username = username
        self.pic_url = pic_url

    @staticmethod
    def get(user_id):
        cur = get_cursor()
        user = cur.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(user_id=user[0], username=user[1], pic_url=user[2])
        return user

    @staticmethod
    def create(user_id, username, pic_url):
        cur = get_cursor()
        cur.execute(
            "INSERT INTO users (user_id, username, pic_url) VALUES (?, ?, ?)",
            (user_id, username, pic_url),
        )
        cur.connection.commit()
