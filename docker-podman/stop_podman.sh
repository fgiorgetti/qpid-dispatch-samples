#!/bin/bash

routers=(routera routerb)
network="testnet"

for router in ${routers[@]}; do
    sudo podman stop ${router} 2> /dev/null || continue
done
sleep 2
sudo podman network rm -f $network
