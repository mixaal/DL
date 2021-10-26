#!/bin/bash -eux

# import docker-registry
. "scripts/docker-registry.sh" $@

# build image
docker build $(getBuildOpts) -f Dockerfile .

# remove dangling images
for DANGLING_IMAGE in $(listDanglingImages); do
    docker rmi "${DANGLING_IMAGE}" &>/dev/null
done
