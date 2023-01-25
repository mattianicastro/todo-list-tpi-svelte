FROM python:3.12.0a4

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python create_db.py

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]

