#!/bin/bash

routers=(routera routerb)
network="testnet"

for router in ${routers[@]}; do
    docker stop ${router} 2> /dev/null || continue
done
docker network rm $network
