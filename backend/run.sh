flask --app main initdb
gunicorn --bind 0.0.0.0:8080 main:app