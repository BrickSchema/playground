#!/usr/bin/env bash

# create a docker bridge network as docker1
docker network create -o "com.docker.network.bridge.name"="docker1" -d bridge --subnet 172.25.0.0/16 isolated_nw

# the following needs to be executed once rebooted

# set up the default firewall rules
# decline any communication with external hosts
iptables -C DOCKER-USER -i docker1 -j DROP
RET=$?
if [ $RET -eq 1 ]; then
    echo "Create new rule."
    iptables -I DOCKER-USER -i docker1 -j DROP
elif [ $RET -eq 0 ]; then
    echo "Rule 'DOCKER-USER -i docker1 -j DROP' already exists."
fi

# allow communication with host ephemeral ports
iptables -C INPUT -i docker1 -p udp --match multiport --dport 32768:60999 -j ACCEPT
RET=$?
if [ $RET -eq 1 ]; then
    echo "Create new rule."
    iptables -I INPUT -i docker1 -p udp --match multiport --dport 32768:60999 -j ACCEPT
elif [ $RET -eq 0 ]; then
    echo "Rule 'INPUT -i docker1 -p udp --match multiport --dport 32768:60999 -j ACCEPT' already exists."
fi

iptables -C INPUT -i docker1 -p tcp --match multiport --dport 32768:60999 -j ACCEPT
RET=$?
if [ $RET -eq 1 ]; then
    echo "Create new rule."
    iptables -I INPUT -i docker1 -p tcp --match multiport --dport 32768:60999 -j ACCEPT
elif [ $RET -eq 0 ]; then
    echo "Rule 'INPUT -i docker1 -p tcp --match multiport --dport 32768:60999 -j ACCEPT' already exists."
fi

# decline any other communication with host
iptables -C INPUT -i docker1 -j DROP
RET=$?
if [ $RET -eq 1 ]; then
    echo "Create new rule."
    iptables -I INPUT -i docker1 -j DROP
elif [ $RET -eq 0 ]; then
    echo "Rule 'INPUT -i docker1 -j DROP' already exists."
fi

# PLAYGROUND_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' playground)
PLAYGROUND_IP=$(docker network inspect isolated_nw | grep Gateway | awk 'NR==1 {print $2}' | sed 's/0.1/0.2/'| sed -e 's/^"//' -e 's/"$//')
iptables -C DOCKER-USER -i docker1 -p tcp --match multiport -d $PLAYGROUND_IP --dport 32768:60999 -j ACCEPT
RET=$?
if [ $RET -eq 1 ]; then
    echo "Create new rule."
    iptables -I DOCKER-USER -i docker1 -p tcp --match multiport -d $PLAYGROUND_IP --dport 32768:60999 -j ACCEPT
elif [ $RET -eq 0 ]; then
    echo "Rule 'DOCKER-USER -i docker1 -p tcp --match multiport -d $PLAYGROUND_IP --dport 32768:60999 -j ACCEPT' already exists."
fi
