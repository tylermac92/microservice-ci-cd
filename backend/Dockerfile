FROM python:3.11-slim
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean
WORKDIR /app
COPY requirements.txt .
COPY wait_for_db.sh .
RUN pip install -r requirements.txt
COPY . .
CMD ["./wait_for_db.sh", "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
