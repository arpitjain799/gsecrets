import click
from . import secrets

@click.group()
def cli():
    pass

@cli.command()
@click.argument('path')
@click.argument('content')
def put(path, content):
    secrets.put(path, content)

@cli.command()
@click.argument('path')
def get(path):
    print(secrets.get(path))