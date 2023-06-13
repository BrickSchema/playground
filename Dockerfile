FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./geniebackend /app

COPY ./requirements.txt /app/

RUN pip install -r /app/requirements.txt
