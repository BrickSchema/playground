FROM tiangolo/uwsgi-nginx-flask:python3.7

ENV HOME="/root"
WORKDIR /root

COPY ./requirements.txt /root/
RUN --mount=type=cache,target=/root/.cache pip install -r /root/requirements.txt
COPY . /root

CMD python3 -m geniebackend.endpoints
