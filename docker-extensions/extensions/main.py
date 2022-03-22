import click

from . import volume

@click.group()
def extensions():
    """Entrypoint"""
    pass

@extensions.command()
def docker_cli_plugin_metadata():
    print('{"SchemaVersion":"0.1.0","Vendor":"-","Version":"1.0","ShortDescription":"Manage environments"}')

extensions.add_command(volume)

if __name__ == "__main__":
    extensions()
