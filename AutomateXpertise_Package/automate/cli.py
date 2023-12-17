# automate/cli.py

"""Import module"""
import click
from automate.core import create_container, list_containers, start_container, stop_container, delete_container

@click.group()
def cli():
    """Fonction cli"""

@cli.command()
@click.argument('name')
def create(name):
    """Fonction create"""
    create_container(name)

@cli.command()
def list():
    """Fonction list"""
    list_containers()

@cli.command()
@click.argument('container_name')
def start(container_name):
    """Fonction start"""
    start_container(container_name)

@cli.command()
@click.argument('container_name')
def stop(container_name):
    """Fonction stop"""
    stop_container(container_name)

@cli.command()
@click.argument('container_name')
def delete(container_name):
    """Fonction delete"""
    delete_container(container_name)
