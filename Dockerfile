FROM python:3.12

COPY . .

RUN pip install -r requirements.txt

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:80

EXPOSE 80