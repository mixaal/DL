#!/bin/bash -eu

# docker repository
PROJECT_LABEL="project"
PROJECT="query-service"
DOCKER_REPOSITORY="phx.ocir.io/oraclebigdatadb/${PROJECT}"
# tags
LATEST_TAG="${1:-latest}"
BUILD_TAGS=(
    "${LATEST_TAG}"
    # maybe add a build number in future?
)

function getContainer() {
    basename $(pwd)
}

function getImage() {
    local TAG=${1:-${LATEST_TAG}}
    echo "${DOCKER_REPOSITORY}/$(getContainer):${TAG}"
}

function getBuildOpts() {
    for TAG in "${BUILD_TAGS[@]}"; do
        echo "-t"
        getImage "${TAG}"
    done
}

function listImages() {
    docker images --filter "dangling=false"  | tail -n +2 | awk '{print $1":"$2}'
}

function listDanglingImages() {
    docker images -qa --filter "dangling=true"
}