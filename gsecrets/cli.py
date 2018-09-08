import sys
import click
from . import core

@click.group()
def cli():
    pass

@cli.command()
@click.argument('path')
@click.argument('content')
@click.option('--replace/--no-replace', default=False)
def put(path, content, replace):
    core.put(path, content, replace)

@cli.command()
@click.argument('path')
def get(path):
	try:
	    secret = core.get(path)
	    print(secret.decode('utf-8'))
	except core.SecretNotFound:
		sys.exit("Secret not found")