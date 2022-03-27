import click
import sys

metadata_command = "docker-cli-plugin-metadata"
plugin_name = "extensions"

from .. import __version__
from .. import volume as vol

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in [metadata_command, plugin_name]:
        extensions()
    else:
        sys.argv[0] = "docker"
        cli()

@click.group()
def cli():
    """Docker CLI entrypoint"""
    pass

@cli.command()
def docker_cli_plugin_metadata():
    """Docker CLI pugin metadata helper"""
    print('{{"SchemaVersion":"0.1.0",'
          '"Vendor":"None Inc.",'
          '"Version":"{}",'
          '"ShortDescription":"Docker CLI extensions"}}'
            .format(__version__))

@cli.group()
def extensions():
    """Docker CLI extensions"""

##### Volume commands

@extensions.group()
def volume():
    """Volume entrypoint"""
    pass

@volume.command()
@click.argument("source")
@click.argument("destination")
def clone(source, destination):
    return vol.clone(source, destination)

@volume.command()
@click.argument("source")
@click.argument("destination")
def rename(source, destination):
    return vol.rename(source, destination)
