@click.group()
def volume():
    """Volume entrypoint"""
    pass

def volume_exists(volume)
    try:
        client.volumes.get(volume)
    except docker.errors.NotFound:
        return False

    return True

@volume.command()
@click.argument("source")
@click.argument("destination")
def clone(source, destination):
    if not volume_exists(source):
        print(f"Source volume {source} doest not exist")
        return 1
    elif volume_exists(destination):
        print(f"Destination volume {destination} already exists")
        return 1

    src_vol = client.volumes.get(source)
    dst_vol = client.volumes.create(source)

    try:
        client.containers.run("alpine", "cp -r /src /dst", \
                volumes=[f'{src_vol}:/src', f'{dst_vol}:/dst'])
    except:
        print("Execution failed")
        return 1

    return 0

@volumes.command()
@click.argument("source")
@click.argument("destination")
def rename(source, destination):
    print("Rename")
    return 0
