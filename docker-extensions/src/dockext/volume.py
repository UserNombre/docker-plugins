import logging
import tarfile

from io import BytesIO
from pathlib import Path
from docker.errors import NotFound

from . import client

log = logging.getLogger(__name__)

# TODO add error checking everywhere
# TODO improve functionality

def ls(volume, recursive):
    name = volume_get_name(volume)
    path = volume_get_path(volume, "/volume")

    cmd = f"cd {path}; find *" if recursive else f"ls {path}"
    container = client.containers.run("alpine", f"sh -c '{cmd}'",
            volumes=[f'{name}:/volume'], remove=True)
    print(container.decode().strip())

def get(volume, destination):
    root_path = "/volume"
    volume_name = volume_get_name(volume)
    volume_path = volume_get_path(volume, root_path)
    dst_path = Path(destination).resolve()

    # Keep the container alive by setting tty and detach
    container = client.containers.run("alpine",
                    volumes=[f'{volume_name}:{root_path}'],
                    tty=True, detach=True)

    raw, _ = container.get_archive(volume_path)
    # get_archive appears to return a generator of raw blocks,
    # join them into bytes and convert it to something tarfile
    # understands, there probably is a better way of doing it
    stream = BytesIO(b"".join(list(raw)))
    # For some reason stop takes too long (tty + detach?), kill
    container.remove(force=True)

    with tarfile.open(fileobj=stream, mode='r') as tar:
        first = tar.getmembers()[0]
        if not first.isdir():
            tar.extract(first, dst_path)
        else:
            members = tar.getmembers()[1:]
            for member in members:
                path = Path(member.path)
                member.path = Path(*path.parts[1:])
            tar.extractall(dst_path, members=members)

def put(volume, source, no_target_directory):
    root_path = "/volume"
    volume_name = volume_get_name(volume)
    volume_path = volume_get_path(volume, root_path)
    src_path = Path(source).resolve()

    container = client.containers.run("alpine",
                    volumes=[f'{volume_name}:{root_path}'],
                    tty=True, detach=True)

    # Use a byte stream to avoid creating a file in disk
    stream = BytesIO()
    with tarfile.open(fileobj=stream, mode='w') as tar:
        if not src_path.is_dir() or not no_target_directory:
            tar.add(src_path, arcname=src_path.parts[-1])
        else:
            for path in src_path.iterdir():
                tar.add(path, arcname=path.parts[-1])
        container.put_archive(volume_path, stream.getvalue())

    container.remove(force=True)

def clone(source, destination):
    client.containers.run("alpine", f"cp -r -T /src /dst",
            volumes=[f'{source}:/src', f'{destination}:/dst'],
            remove=True)

def rename(source, destination):
    clone(source, destination)
    src_vol = client.volumes.get(source)
    src_vol.remove()

def volume_get_name(volume_scheme):
    try:
        idx = volume_scheme.index(":")
        return volume_scheme[:idx]
    except:
        return volume_scheme

def volume_get_path(volume_scheme, root="/"):
    try:
        idx = volume_scheme.index(":")
        path = volume_scheme[idx+1:]
        path = str(Path(f"{root}/{path}"))
        return path
    except:
        return root
