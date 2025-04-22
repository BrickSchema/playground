# syntax=docker/dockerfile:1
FROM python:3.10-slim

ENV HOME="/root"
WORKDIR /root/sbos-monitor/

# install apt dependencies
#RUN --mount=type=cache,target=/var/cache/apt \
#    apt-get update && \
#    apt-get install -y --no-install-recommends ca-certificates git wget curl && \
#    rm -rf /var/lib/apt/lists/*

# install poetry
ARG PYPI_MIRROR
RUN if [ -n "$PYPI_MIRROR" ]; then pip config set global.index-url $PYPI_MIRROR; fi
RUN --mount=type=cache,target=/root/.cache pip install poetry

# create virtualenv
ENV VIRTUAL_ENV=/root/.venv
RUN python3 -m virtualenv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install dependencies
COPY pyproject.toml poetry.lock README.md /root/sbos-monitor/
COPY sbos/monitor/__init__.py /root/sbos-monitor/sbos/monitor/
RUN --mount=type=cache,target=/root/.cache poetry install --without dev
COPY . /root/sbos-monitor
RUN --mount=type=cache,target=/root/.cache poetry install --without dev

CMD python3 -m sbos.monitor
