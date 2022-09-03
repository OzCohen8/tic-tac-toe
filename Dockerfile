FROM python:3.10-slim-buster as builder

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD [ "python", "main.py"]