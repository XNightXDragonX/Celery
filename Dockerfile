FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p uploads/original uploads/processed

EXPOSE 5000

CMD ["sh", "-c", "redis server & celery -A celery_worker.celery worker --loglevel=info & python app.py"]