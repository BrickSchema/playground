# syntax=docker/dockerfile:1
FROM tiangolo/uvicorn-gunicorn:python3.10-slim

ENV HOME="/root"
WORKDIR /root/brick-server-playground/

# install apt dependencies
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates git wget curl && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
   tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*

# install dockerize
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# install poetry
ARG PYPI_MIRROR
RUN if [ -n "$PYPI_MIRROR" ]; then pip config set global.index-url $PYPI_MIRROR; fi
RUN --mount=type=cache,target=/root/.cache pip install poetry

# create virtualenv
ENV VIRTUAL_ENV=/root/.venv
RUN python3 -m virtualenv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install dependencies
COPY ./brick-server-minimal/pyproject.toml ./brick-server-minimal/poetry.lock ./brick-server-minimal/README.md /root/brick-server-minimal/
COPY ./brick-server-playground/pyproject.toml ./brick-server-playground/poetry.lock ./brick-server-playground/README.md /root/brick-server-playground/
COPY ./brick-server-minimal/brick_server/minimal/__init__.py /root/brick-server-minimal/brick_server/minimal/
COPY ./brick-server-playground/brick_server/playground/__init__.py /root/brick-server-playground/brick_server/playground/
RUN --mount=type=cache,target=/root/.cache poetry install --no-dev
RUN --mount=type=cache,target=/root/.cache pip3 install torch --index-url https://download.pytorch.org/whl/cpu
COPY ./brick-server-minimal /root/brick-server-minimal/
COPY ./brick-server-playground /root/brick-server-playground/
# RUN rm /root/brick-server-playground/.env/
RUN --mount=type=cache,target=/root/.cache poetry install --no-dev

EXPOSE $PORT

CMD python3 -m brick_server.playground
