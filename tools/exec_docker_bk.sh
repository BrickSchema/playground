#/usr/bin/env bash
#
docker rm -f playground

RET=$(docker inspect -f '{{.Containers}}' isolated_nw)
if [ "$RET" != 'map[]' ]; then
    echo "isolated_nw not empty! Stop non-exited containers first!"
    exit 1
fi

docker create --name playground \
    --rm \
    -p 8000:80 \
    -it \
    -v /etc/letsencrypt/:/etc/letsencrypt/ \
    -e LOG_LEVEL="debug" \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $PWD:/app \
    -e ENABLE_SSL=true \
    -e CERTFILE="/etc/letsencrypt/live/bd-testbed.ucsd.edu/fullchain.pem" \
    -e KEYFILE="/etc/letsencrypt/live/bd-testbed.ucsd.edu/privkey.pem" \
    --entrypoint /app/docker/start-reload.sh \
    --privileged=true \
    jbkoh/playground:0.1
docker network connect playground-backend-network playground
docker network connect isolated_nw playground
docker start -ai playground
    #--network "playground_default" \
    #--network "playground-frontend-network" \
    #
    #--entrypoint /app/docker/start-reload.sh \
#docker network connect playground-frontend-network playground
