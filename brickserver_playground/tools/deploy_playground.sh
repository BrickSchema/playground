#/usr/bin/env bash
#
docker rm -f brickserver-playground-deployment

RET=$(docker inspect -f '{{.Containers}}' isolated_nw)
if [ "$RET" != 'map[]' ]; then
    echo "isolated_nw not empty! Stop non-exited containers first!"
    exit 1
fi

docker create --name brickserver-playground-deployment \
    --rm \
    -it \
    -e LOG_LEVEL="debug" \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $PWD:/app \
    -e ENABLE_SSL=false \
    --entrypoint /app/docker/start-reload.sh \
    --privileged=true \
    --label "traefik.http.routers.bs-backend.rule=Host(\"bd-datas3.ucsd.edu\") && ( PathPrefix(\"/docs\") || PathPrefix(\"/dummy-frontend\") || PathPrefix(\"/auth\") || PathPrefix(\"/brickapi\") )" \
    --label traefik.http.routers.bs-backend.entrypoints=websecure \
    --label traefik.http.routers.bs-backend.tls=true \
    --label traefik.http.routers.bs-backend.tls.certresolver=leresolver \
    --label "traefik.docker.network=deployment_default" \
    jbkoh/playground:0.1
docker network connect deployment_default brickserver-playground-deployment
docker network connect isolated_nw brickserver-playground-deployment
docker start -ai brickserver-playground-deployment
    #--network "playground_default" \
    #--network "playground-frontend-network" \
    # 
    #--entrypoint /app/docker/start-reload.sh \
#docker network connect playground-frontend-network playground
