FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SERVICE=${run_service:-backend}
ENV QUEUES=${queues:-celery}

WORKDIR /opt/djangoTrading/

RUN pip install --upgrade pip
COPY entrypoint.sh /opt/djangoTrading/
COPY requirements.txt /opt/djangoTrading/
RUN pip install -r requirements.txt --no-cache-dir

COPY . /opt/djangoTrading/

ENTRYPOINT [ "/bin/bash", "/opt/djangoTrading/entrypoint.sh" ]