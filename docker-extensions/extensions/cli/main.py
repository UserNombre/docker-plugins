import click

from .. import __version__
from .. import volume as vol

@click.group()
def main():
    """Entrypoint"""
    pass

@main.command()
def docker_cli_plugin_metadata():
    print('{{"SchemaVersion":"0.1.0",'
          '"Vendor":"-",'
          '"Version":"{}",'
          '"ShortDescription":"Additional commands"}}'
            .format(__version__))

##### Volume commands

@main.group()
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
