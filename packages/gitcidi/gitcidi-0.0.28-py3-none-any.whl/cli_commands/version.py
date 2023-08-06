import click
import json
import os
@click.command()
def version():
    '''
    Find the version of the buildpan
    '''
    a = '{"version": "0.1", "languages": "Python"}'
    y = json.loads(a)
    version = y["version"]
    # with open(file_path, 'r') as f:
    #      data = json.load(f)
    #      version = data["Version"]
    
    print(f'Current Buildspan version is {version}')