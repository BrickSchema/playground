FROM node:18-alpine

ENV HOME="/root"
WORKDIR /root

COPY ./package.json ./yarn.lock  /root/
RUN --mount=type=cache,target=/usr/local/share/.config/yarn/global yarn
COPY . /root

CMD node backend/index.js
