from db import con


class User:
    def __init__(self, user_id, username, pic_url):
        self.id = user_id
        self.username = username
        self.pic_url = pic_url

    @staticmethod
    def get(user_id):
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = %s", (str(user_id),))
        user = cur.fetchone()
        if not user:
            return None

        user = User(user_id=user[0], username=user[1], pic_url=user[2])
        return user

    @staticmethod
    def create(user_id, username, pic_url):
        cur = con.cursor()

        cur.execute(
            "INSERT INTO users (user_id, username, pic_url) VALUES (%s, %s, %s)",
            (str(user_id), username, pic_url),
        )
        con.commit()
