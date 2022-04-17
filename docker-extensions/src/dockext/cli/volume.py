import click
import logging

from .. import volume as vol

log = logging.getLogger(__name__)

@click.group()
def volume():
    """Volume entrypoint"""

@volume.command()
@click.argument("volume")
@click.option("-r", "--recursive", is_flag=True)
def ls(volume, recursive):
    """List files in a volume"""
    log.debug("Executing ls")
    return vol.ls(volume, recursive)

@volume.command()
@click.argument("volume")
@click.argument("file")
def get(volume, file):
    """Copy files from a volume to the host"""
    log.debug("Executing get")
    return vol.get(volume, file)

@volume.command()
@click.argument("volume")
@click.argument("file")
@click.option("-t/-T", "--target-directory/--no-target-directory",
              is_flag=True, default=False)
def put(volume, file, target_directory):
    """Copy files from the host to a volume"""
    log.debug("Executing put")
    return vol.put(volume, file, target_directory)

@volume.command()
@click.argument("source")
@click.argument("destination")
def clone(source, destination):
    """Clone a volume"""
    log.debug("Executing clone")
    return vol.clone(source, destination)

@volume.command()
@click.argument("source")
@click.argument("destination")
def rename(source, destination):
    """Rename a volume"""
    log.debug("Executing rename")
    return vol.rename(source, destination)
