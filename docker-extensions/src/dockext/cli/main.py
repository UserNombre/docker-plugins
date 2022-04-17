import click
import logging
import sys

from docker.errors import *

from .. import __version__
from .. import volume as vol

log = logging.getLogger(__name__)
metadata_command = "docker-cli-plugin-metadata"
plugin_name = "extensions"

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in [metadata_command, plugin_name]:
        entry = extensions
    else:
        sys.argv[0] = "docker"
        entry = cli
    try:
        entry()
    except (NotFound, ContainerError) as e:
        xlog(e)
    except Exception as e:
        xlog(e)

def setup_logging(log_level):
    if not log_level:
        log_level = "WARNING"
    logging.basicConfig(format='[%(levelname)s] %(message)s',
            level=getattr(logging, log_level))
    logging.getLogger("urllib3").propagate = False
    logging.getLogger("requests").propagate = False
    logging.getLogger("docker").propagate = False

def xlog(log_msg=None, exit_code=1):
    if log_msg:
        if not exit_code:
            log.info(log_msg)
        else:
            log.error(log_msg)
    sys.exit(exit_code)

@click.group()
def cli():
    """Docker CLI plugin entrypoint"""

@cli.command()
def docker_cli_plugin_metadata():
    """Docker CLI pugin metadata helper"""
    print('{{"SchemaVersion":"0.1.0",'
          '"Vendor":"None Inc.",'
          '"Version":"{}",'
          '"ShortDescription":"Docker CLI extensions"}}'
            .format(__version__))

@cli.group()
@click.option("-l", "--log-level", type=click.Choice(
    ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]))
def extensions(log_level):
    """Docker CLI extensions"""
    setup_logging(log_level)

##### Volume commands

@extensions.group()
def volume():
    """Volume entrypoint"""

@volume.command()
@click.argument("volume")
@click.option("-r", "--recursive", is_flag=True)
def ls(volume, recursive):
    log.debug("Executing ls")
    return vol.ls(volume, recursive)

@volume.command()
@click.argument("volume")
@click.argument("file")
def get(volume, file):
    log.debug("Executing get")
    return vol.get(volume, file)

@volume.command()
@click.argument("volume")
@click.argument("file")
@click.option("-T", "--no-target-directory", is_flag=True)
def put(volume, file, no_target_directory):
    log.debug("Executing put")
    return vol.put(volume, file, no_target_directory)

@volume.command()
@click.argument("source")
@click.argument("destination")
def clone(source, destination):
    log.debug("Executing clone")
    return vol.clone(source, destination)

@volume.command()
@click.argument("source")
@click.argument("destination")
def rename(source, destination):
    log.debug("Executing rename")
    return vol.rename(source, destination)
