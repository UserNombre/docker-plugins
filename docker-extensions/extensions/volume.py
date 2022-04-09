import logging
import os

from pathlib import Path
from docker.errors import NotFound

from . import client

log = logging.getLogger(__name__)

def list(volume_scheme, recursive):
    name = volume_get_name(volume_scheme)
    path = volume_get_path(volume_scheme)
    path = str(Path("/volume/" + path))

    cmd = "find" if recursive else "ls"
    container = client.containers.run( "alpine", f"{cmd} {path}",
            volumes=[f'{name}:/volume'], remove=True)
    print(container.decode().strip())

def get(volume_scheme, system_path):
    copy(volume_scheme, system_path, True, False)

def put(volume_scheme, system_path):
    copy(system_path, volume_scheme, False, True)

def clone(source, destination):
    copy(source, destination, True, True)

def rename(source, destination):
    copy(source, destination, True, True)
    src_vol = client.volumes.get(source)
    src_vol.remove()

def copy(src, dst, src_is_vol, dst_is_vol):
    csrc = "/src/"
    cdst = "/dst/"
    if src_is_vol:
        vsrc = volume_get_name(src)
        csrc += volume_get_path(src)
    else:
        vsrc = os.path.realpath(src)

    if dst_is_vol:
        vdst = volume_get_name(dst)
        cdst += volume_get_path(dst)
        uid = 0
    else:
        vdst = os.path.realpath(dst)
        uid = os.getuid()

    csrc = str(Path(csrc))
    cdst = str(Path(cdst))
    cmd = f"cp -r -T {csrc} {cdst}; chown -R {uid}:{uid} {cdst}"
    log.debug(cmd)
    client.containers.run("alpine", f"sh -c '{cmd}'",
            volumes=[f'{vsrc}:/src', f'{vdst}:/dst'],
            remove=True)

def volume_get_name(volume_scheme):
    try:
        idx = volume_scheme.index(":")
        return volume_scheme[:idx]
    except:
        return volume_scheme

def volume_get_path(volume_scheme):
    try:
        idx = volume_scheme.index(":")
        return volume_scheme[idx+1:]
    except:
        return "/"
