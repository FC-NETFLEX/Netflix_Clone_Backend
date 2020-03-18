FROM        python:3.7-slim

RUN         apt -y update && apt -y dist-upgrade && apt -y autoremove
RUN         apt -y install nginx

RUN         mkdir /var/log/gunicorn
RUN         mkdir /root/.aws
COPY        requirements.txt /srv/Netflex_Clone_Backend/
RUN         pip install -r /srv/Netflex_Clone_Backend/requirements.txt

COPY         . /srv/Netflex_Clone_Backend
WORKDIR      /srv/Netflex_Clone_Backend/app



