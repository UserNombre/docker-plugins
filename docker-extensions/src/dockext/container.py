import logging

from docker.errors import NotFound

from . import client

log = logging.getLogger(__name__)

def purge(filters):
    log.debug(f"Using filters {filters}")
    for container in client.containers.list(filters=filters):
        print(container.name)
        container.remove(force=True) 
