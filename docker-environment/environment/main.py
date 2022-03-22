import click
import sys

@click.group()
def cli():
    """Entrypoint"""
    pass

@cli.command()
def docker_cli_plugin_metadata():
    print('{"SchemaVersion":"0.1.0","Vendor":"-","Version":"1.0","ShortDescription":"Manage environments"}')

@cli.group()
def environment():
    """Environment entrypoint"""
    pass

@environment.command()
def setup():
    print("Setup")

@environment.command()
def restore():
    print("Restore")

if __name__ == "__main__":
    cli()
