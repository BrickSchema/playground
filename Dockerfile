FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN apt update && \
    apt install -y vim certbot net-tools nmap htop git

ARG SRC="/usr/src/playground"

COPY $PWD/playground-src $SRC
#RUN    cd $SRC  && \
    #git submodule update --init --recursive --remote
    #&& \
    #git checkout --track origin/fastapi

RUN rm -rf /app  && \
    mv $SRC /app

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt && \
    pip install -r /app/brick-server-minimal/requirements.txt && \
    pip uninstall -y fastapi && \
    pip install git+https://github.com/jbkoh/fastapi.git@fix-bodyparsing

#COPY configs/configs.json /app/configs/
ENV BRICK_CONFIGFILE "/app/configs/configs.json"

CMD /app/docker/start.sh
