import os

from db import con
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    current_user,
    jwt_required,
    set_access_cookies,
)
from user import User

load_dotenv()

import requests
from oauthlib.oauth2 import WebApplicationClient

app = Flask(__name__)

app.config["SERVER_NAME"] = os.environ["DOMAIN"]
app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(32)
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_COOKIE_DOMAIN"] = f"{os.environ['FRONTEND_DOMAIN']}"
app.config["JWT_COOKIE_SAMESITE"] = "None"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

CORS(app, supports_credentials=True, origins=[os.environ["FRONTEND_URL"]])

jwt = JWTManager(app)
oauth_client = WebApplicationClient(os.environ["GITHUB_CLIENT_ID"])


def init_db():
    with app.open_resource("schema.sql", mode="r") as f:
        con.cursor().execute(f.read())
    con.commit()


@app.cli.command("initdb")
def initdb_command():
    """Initializes the database."""
    init_db()
    print("Initialized the database.")


@jwt.user_identity_loader
def user_identity_lookup(user: User):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.get(identity)


@app.errorhandler(401)
def custom_401(error):
    return jsonify({"msg": "Unauthorized"}), 401


@app.route("/login")
def login():
    url = oauth_client.prepare_request_uri(
        f"https://github.com/login/oauth/authorize",
        redirect_uri=f"https://{os.environ['DOMAIN']}/callback",
    )
    return redirect(url)


@app.route("/callback")
def callback():
    code = request.args.get("code")

    if not code:
        return "Missing code", 400
    token_url, headers, body = oauth_client.prepare_token_request(
        "https://github.com/login/oauth/access_token",
        authorization_response=request.url,
        redirect_url=f"https://{os.environ['DOMAIN']}/callback",
        code=code,
    )
    headers.update({"Accept": "application/json"})
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(os.environ["GITHUB_CLIENT_ID"], os.environ["GITHUB_CLIENT_SECRET"]),
    )
    token_data = token_response.json()
    oauth_client.parse_request_body_response(token_response.text)
    user_data_res = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {token_data['access_token']}"},
    )
    user_data = user_data_res.json()

    user = User(user_data["id"], user_data["login"], user_data["avatar_url"])
    if not User.get(user_data["id"]):
        User.create(user_data["id"], user_data["login"], user_data["avatar_url"])
    token = create_access_token(identity=user)
    res = redirect(os.environ["FRONTEND_URL"])
    set_access_cookies(res, token, domain=f".{os.environ['FRONTEND_DOMAIN']}")
    return res


@app.route("/me")
@jwt_required()
def me():
    return jsonify(
        {
            "id": current_user.id,
            "username": current_user.username,
            "pic_url": current_user.pic_url,
        }
    )


@app.route("/tasks", methods=["PUT"])
@jwt_required()
def task_create():
    content = request.json.get("content")
    if not content:
        return {"msg": "content is required"}, 400
    cur = con.cursor()
    cur.execute(
        """
    INSERT INTO tasks(content, user_id) VALUES(%s,%s) RETURNING id
    """,
        (content, current_user.id),
    )
    task_id = cur.fetchone()[0]
    con.commit()
    return {"id": task_id, "msg": "ok"}, 200


@app.route("/tasks/<int:id>", methods=["PATCH"])
@jwt_required()
def task_update(id):
    done = request.json.get("done")
    content = request.json.get("content")
    if done is None and content is None:
        return "nothing to update", 400
    cur = con.cursor()
    if done is not None and content:
        cur.execute(
            """
        UPDATE tasks SET done = %s, content = %s WHERE id = %s AND user_id = %s
        """,
            (done, content, id, current_user.id),
        )
    elif done is not None:
        cur.execute(
            """
        UPDATE tasks SET done = %s WHERE id = %s AND user_id = %s
        """,
            (done, id, current_user.id),
        )
    elif content:
        cur.execute(
            """
        UPDATE tasks SET content = %s WHERE id = %s AND user_id = %s
        """,
            (content, id, current_user.id),
        )
    cur.connection.commit()
    return {"msg": "ok"}, 200


@app.route("/tasks/<int:id>", methods=["DELETE"])
@jwt_required()
def task_delete(id):
    cur = con.cursor()
    cur.execute(
        """
    DELETE FROM tasks WHERE id = %s AND user_id = %s
    """,
        (id, current_user.id),
    )
    cur.connection.commit()
    return {"msg": "ok"}, 200


@app.route("/tasks")
@jwt_required()
def task_list():
    cur = con.cursor()
    cur.execute(
        """
    SELECT id, content, done FROM tasks WHERE user_id = %s
    """,
        (current_user.id,),
    )

    res = cur.fetchall()

    out = [
        {
            "id": task[0],
            "content": task[1],
            "done": bool(task[2]),
        }
        for task in res
    ]
    return jsonify(out)


@app.route("/tasks/<int:id>")
@jwt_required()
def task_details(id):
    cur = con.cursor()
    cur.execute(
        """
    SELECT id, content, done FROM tasks WHERE id = %s AND user_id = %s
    """,
        (id, current_user.id),
    )
    res = cur.fetchone()
    if not res:
        return {"msg": "not found"}, 404
    return {
        "id": res[0],
        "content": res[1],
        "done": bool(res[2]),
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
