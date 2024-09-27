FROM docker.io/python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

WORKDIR /app/src
CMD ["python", "main.py"]
