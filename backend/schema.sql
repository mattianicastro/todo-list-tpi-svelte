CREATE TABLE IF NOT EXISTS users(
    user_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    pic_url TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS tasks(
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE,
    user_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);