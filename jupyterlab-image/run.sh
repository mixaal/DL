#!/bin/bash -xe

THEME=${1:-chesterish}

#docker run -it --rm  jupyterlab /bin/bash
docker run -eSET_THEME="$THEME"  -eMYSQL_PASSWORD="$MYSQL_PASSWORD" --name jupyterlab  -p8889:8889 -p8888:8888 -v "$HOME/git/DL:/notebooks" --rm  jupyterlab
