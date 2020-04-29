# Demonstrates how to run qpid dispatch router in containers

## Overview

The following sample runs qpid dispatch router using containers (using docker or podman),
mounting the respective configuration directories on each container.

Both are using a docker/podman network, so all related containers can resolve each other
by name.

## Running with podman

Using podman, the network creation is being done using `sudo`,
as it not allowed for rootless users (at least I am not aware of it).

1. Create the network and run the containers

```
./run_podman.sh
```

2. Verify the network

```
./verify_podman.sh
```

3. Stop and remove both containers and network

```
./stop_podman.sh
```

## Running with docker

1. Create the network and run the containers

```
./run_docker.sh
```

2. Verify the network

```
./verify_docker.sh
```

3. Stop and remove both containers and network

```
./stop_docker.sh
```

