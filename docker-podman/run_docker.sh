#!/bin/bash

curdir=`readlink -f .`
network="testnet"
image="registry.redhat.io/amq7/amq-interconnect"
exposed=15672

function run() {
    name=$1
    dir=$2
    docker run --name ${name} -p ${exposed}:5672 --network ${network} --rm -d -v ${curdir}/${dir}:/var/lib/qdrouterd:Z ${image} qdrouterd -c /var/lib/qdrouterd/qdrouterd.conf
    ((exposed++))
}

function running() {
    echo container $1 is already running
}

docker network create ${network} 2> /dev/null
run routera router.a 2> /dev/null || running $_
run routerb router.b 2> /dev/null || running $_
