#!/bin/bash

# TODO refactor code

set -e

print_help()
{
    echo "Usage: $0 target"
}

if [[ $# -ne 1 ]]
then
    print_help
    exit 0
fi

container=backup
is_running=$(docker inspect --format="{{.State.Running}}" "$container")
target=$1
# Duplicity configuration
target_env=env/restore/$target.env
# Deployment specific script (restore DB, sanitize configuration, ...)
target_script=env/restore/$target.sh

# TODO additional checks
if [[ $is_running != "true" ]]
then
    echo "Duplicity container '$container' not running"
    exit 1
elif [[ ! -e $target_env ]]
then
    echo "$target_env does not exist"
    exit 1
fi

docker container exec --env-file="$target_env" "$container" \
    restore --force

if [[ $? -eq 0 && -e $target_script ]]
then
    echo "Executing $target_script"
    # TODO allow different scripting languages, at least those
    # allowed within the Duplicity container
    # Do not use -t, as we are executing from a pipe, not TTY
    cat "$target_script" | docker container exec -i "$container" sh
fi
