def volume_exists(volume):
    try:
        client.volumes.get(volume)
    except docker.errors.NotFound:
        return False

    return True

def clone(src, dst):
    if not volume_exists(src):
        print(f"Source volume {src} doest not exist")
        return 1
    elif volume_exists(dst):
        print(f"Destination volume {dst} already exists")
        return 1

    src_vol = client.volumes.get(src)
    dst_vol = client.volumes.create(dst)

    try:
        client.containers.run("alpine", "cp -r /src /dst", \
                volumes=[f'{src_vol}:/src', f'{dst_vol}:/dst'])
    except:
        print("Execution failed")
        return 1

    return 0

def rename(source, destination):
    print("Rename")
    return 0
