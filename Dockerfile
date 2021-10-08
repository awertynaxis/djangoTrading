FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SERVICE=${run_service:-backend}
ENV QUEUES=${queues:-celery}

RUN apt-get update &&  apt-get install -y netcat

WORKDIR /opt/djangoTrading/

RUN pip install --upgrade pip
COPY requirements.txt /opt/djangoTrading/
RUN pip install -r requirements.txt --no-cache-dir

COPY . /opt/djangoTrading/

RUN chmod +x /opt/djangoTrading/run_backend.sh
RUN chmod +x /opt/djangoTrading/run_worker.sh
RUN chmod +x /opt/djangoTrading/run_scheduler.sh

ENTRYPOINT [ "/bin/bash", "/opt/djangoTrading/run_backend.sh" ]
