import click
import logging

from .. import container as con

log = logging.getLogger(__name__)

@click.group()
def container():
    """Container entrypoint"""

# Filters should be of the form "a=b,c=d"
# https://docs.docker.com/engine/reference/commandline/ps/
def process_filters(filters):
    if filters is None:
        return {}
    filters = [f.split("=") for f in filters.split(",")]
    return {k: v for k, v in filters}

@container.command()
@click.option("-f", "--filter", "filters")
def purge(filters):
    """Kill and remove all containers"""
    log.debug("Executing purge")
    return con.purge(process_filters(filters))
