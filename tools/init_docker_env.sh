# create a docker bridge network as docker1, only need to be executed once
docker network create -o "com.docker.network.bridge.name"="docker1" -d bridge --subnet 172.25.0.0/16 isolated_nw

# the following needs to be executed once rebooted

# set up the default firewall rules
# decline any communication with external hosts
iptables -I DOCKER-USER -i docker1 -j DROP

# allow communication with host ephemeral ports
iptables -I INPUT -i docker1 -p udp --match multiport --dport 32768:60999 -j ACCEPT
iptables -I INPUT -i docker1 -p tcp --match multiport --dport 32768:60999 -j ACCEPT

# decline any other communication with host
iptables -A INPUT -i docker1 -j DROP

