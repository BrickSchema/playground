#!/usr/bin/env sh

mkdir -p /app/configs

if [ -f /app/configs/jwtRS256.key ]; then
  if [ -f /app/configs/jwtRS256.key.pub ]; then
    echo "Reusing existing JWT key"
  else
    echo "JWT private key is given but not its public key"
    exit 1
  fi
else
  ssh-keygen -t rsa -N '' -b 4096 -m PEM -f /app/configs/jwtRS256.key
  openssl rsa -in /app/configs/jwtRS256.key -pubout -outform PEM -out /app/configs/jwtRS256.key.pub
  echo "JWT private and public keys are created."
fi

# obtain host ip
HOST_DOMAIN="host.docker.internal"
# ping -q -c1 $HOST_DOMAIN > /dev/null 2>&1
# if [ $? -ne 0 ]; then
# can't use the above scripts because caller has set -e
echo "Search for Host IP"
HOST_IP=$(ip route | awk 'NR==1 {print $3}')
echo "Host IP is" $HOST_IP
echo "$HOST_IP\t$HOST_DOMAIN" >> /etc/hosts
