import git
import os
import click
import git
import sys
from github import Github
import subprocess


# cli_commands for the buildpan 
from cli_commands import build
from cli_commands import deploy
from cli_commands import init
from cli_commands import version
@click.group(help="CLI tool to manage CI- CD of projects")
def buildpan():
    pass


buildpan.add_command(build.build)
buildpan.add_command(deploy.deploy)
buildpan.add_command(init.init)
buildpan.add_command(version.version)
if __name__ == '__main__':
    buildpan()