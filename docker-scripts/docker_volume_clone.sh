#!/bin/bash

if [[ $# -ne 2 ]]
then
    echo "Usage: $0 src_vol dst_vol"
    exit 1
fi

docker volume inspect $1 > /dev/null 2>&1
if [[ $? -ne 0 ]]
then
    echo "The source volume '$1' does not exist"
    exit 1
fi

docker volume inspect $2 > /dev/null 2>&1
if [[ $? -eq 0 ]]
then
    echo "The destination volume '$2' already exists"
    exit 1
fi

docker volume create --name $2
docker container run --rm -v "$1:/src" -v "$2:/dst" \
    alpine sh -c "cp -a /src /dst"
