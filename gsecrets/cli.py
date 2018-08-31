import click
from . import secrets

@click.group()
def cli():
    pass

@cli.command()
@click.argument('path')
@click.argument('content')
@click.option('--replace/--no-replace', default=False)
def put(path, content, replace):
    secrets.put(path, content, replace)

@cli.command()
@click.argument('path')
def get(path):
    print(secrets.get(path))