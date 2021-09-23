FROM python:3.8

ENV DEBIAN_FRONTEND=noninteractive
ADD . /opt/djangoTrading/
WORKDIR opt/djangoTrading/

RUN pip install -r requirements.txt --no-cache-dir

ENTRYPOINT [ "/bin/bash", "/opt/djangoTrading/entrypoint.sh" ]