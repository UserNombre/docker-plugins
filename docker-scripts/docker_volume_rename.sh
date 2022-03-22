#!/bin/bash

source "$(dirname $0)/docker_volume_clone.sh"
docker volume rm "$1" &> /dev/null
