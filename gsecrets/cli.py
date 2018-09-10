import sys
import click
from .client import Client
from .exceptions import SecretNotFound

@click.group()
def cli():
    pass

def parse_vault_location(path):
    sp = path.split("/")
    return sp[0] + "/" + sp[1]

@cli.command()
@click.argument("path")
@click.argument("content")
@click.option("--replace/--no-replace", default=False)
def put(path, content, replace):
    client = Client(parse_vault_location(path))
    client.put(path, content, replace)

@cli.command()
@click.argument("path")
def get(path):
    client = Client(parse_vault_location(path))
    try:
        secret = client.get(path)
        print(secret.decode("utf-8"))
    except core.SecretNotFound:
        sys.exit("Secret not found")