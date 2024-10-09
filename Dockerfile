FROM python:3.12

RUN mkdir /cdn_app

WORKDIR /cdn_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x app/docker/*.sh

CMD ["sh", "app/docker/start.sh"]
#CMD ["uvicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
