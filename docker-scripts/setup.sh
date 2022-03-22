#!/bin/bash

# FIXME add error handling
# FIXME refactor logging
# FIXME use local variables 

# TODO migrate code to python before it's too late
# TODO? symlink the base file to environments instead of symlinking
# environments to the override file to avoid volume naming issues

base_file="docker-compose.yml"
override_file="docker-compose.override.yml"
environment_file=".env"
environment_dir="env"
working_dir="${PWD##*/}"
context_name="default"

print_help()
{
    echo "Usage: $0 [options]
OPTIONS
    -h      Print a summary of the command line options and exit
    -g      Process .cfg files and generate the corresponding output files
    -s directory
            Configure the environment with files in 'directory'
    -e      List the current environment's configuration
    -u      Execute docker-compose up with the current environment's configuration
    -d      Execute docker-compose down with the current environment's configuration"
}

# FIXME improve checks

validate_link()
{

    if [[ ! -e ./$1 ]]
    then
        echo "$1 not found"
        return 1
    elif [[ ! -L ./$1 ]]
    then
        echo "$1 is not a symlink"
        return 1
    fi

    realpath=$(readlink "$1")
    echo "  $realpath"
    if [[ ! -e $realpath ]]
    then
        echo "$realpath does not exist, broken symlink"
        return 1
    fi

    return 0
}

validate_links()
{
    if ! (validate_link "$override_file" &&
          validate_link "$environment_file" &&
          validate_link "$environment_dir")
    then
        return 1
    fi
    
    return 0
}

set_names()
{
    if [[ -e "$1/context.env" ]]
    then
        source "$1/context.env"
        context_name="${CONTEXT_PREFIX:-$working_dir}-$1"
    fi
    project_name="${CONTEXT_PREFIX:-$working_dir}_$1"
}

validate_context()
{
    set_names "$real_dir"
    docker context inspect "$context_name" &> /dev/null
}

validate_compose()
{
    if [[ ! -e ./$base_file ]]
    then
        echo "$base_file not found"
        return 1
    elif ! docker-compose config > /dev/null
    then
        echo "$base_file invalid"
        return 1
    fi
}

validate_environment()
{
    real_dir=$(basename $(realpath $environment_dir))
    echo "Working on $real_dir"

    validate_links || return 1
    echo "All links valid"

    validate_compose || return 1
    echo "Compose files valid"

    validate_context || return 1
    echo "Context valid"

    return 0
}

# TODO refactor

setup_links()
{
    if [[ ! -d $new_dir ]]
    then
        echo "$new_dir directory not found"
        return 1
    fi
    # Use -n to treat LINK_NAME as a normal file
    ln -sfn "$new_dir" "$environment_dir"
    echo "  $new_dir"

    if [[ ! -f $new_dir/$override_file ]]
    then
        echo "$new_dir/$override_file not found"
        return 1
    fi
    ln -sf "$new_dir/$override_file" "$override_file"
    echo "  $new_dir/$override_file"

    if [[ ! -f $new_dir/$environment_file ]]
    then
        echo "$new_dir/$environment_file not found"
        return 1
    fi
    ln -sf "$new_dir/$environment_file" "$environment_file"
    echo "  $new_dir/$environment_file"

    return 0
}

# TODO? create unique ID for context

setup_context()
{
    set_names "$new_dir"
    docker context inspect "$context_name" &> /dev/null ||
    docker context create --docker="host=$DOCKER_HOST" "$context_name" &> /dev/null
}

setup_environment()
{
    echo "Setting up links"
    if ! setup_links
    then
        echo "Failed to set up links"
        return 1
    fi

    echo "Setting up context"
    if ! setup_context
    then
        echo "Failed to set up context"
        return 1
    fi

    echo "Environment successfully set up"
    return 0
}

expand_configuration()
{
    echo -n > "$2"
    while read line
    do
        if [[ ${line:0:1} != "#" ]]
        then
            key=${line%%=*}
            value=$(eval "echo ${line#*=}")
            echo "$key=$value" >> "$2"
        fi
    done < "$1"
}

process_configuration()
{
    while read line
    do
        echo "Processing '$line'"
        # Remove .cfg extension, a .ext files should end in .ext.cfg
        expand_configuration "$line" "${line%.*}"
    done < <(find . -name "*.cfg")
}

# TODO add verbose option (-v)
# TODO add reset option (-r)

while getopts "hgs:eud" opt
do
    case "$opt" in
        h)  print_help
            exit 0
            ;;
        g)  set -e
            process_configuration
            exit $?
            ;;
        s)  new_dir=${OPTARG%/} # Remove single trailing /
            setup_environment
            exit $?
            ;;
        e)  validate_environment
            exit $?
            ;;
        u)  validate_environment || exit $?
            shift $(($OPTIND - 1))
            set -x
            docker context use "$context_name" &> /dev/null
            docker-compose -p "$project_name" up -d $@
            docker context use default &> /dev/null
            set +x
            exit 0
            ;;
        d)  validate_environment || exit $?
            shift $(($OPTIND - 1))
            set -x
            docker context use "$context_name" &> /dev/null
            docker-compose -p "$project_name" down $@
            docker context use default &> /dev/null
            set +x
            exit 0
            ;;
    esac
done

print_help
exit 1
