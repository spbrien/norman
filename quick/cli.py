# -*- coding: utf-8 -*-

import os

import click
from utils import *

@click.group()
def main():
    """Utility script for working with emails"""


@main.command()
@click.argument('project')
def start(project):
    # Set up vars
    project_dir = os.path.join(os.getcwd(), project)
    scss_dir = os.path.join(project_dir, 'scss')
    data = {
        "project": project
    }

    # Create project directory
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
    else:
        click.echo(click.style("A directory named %s already exists" % project, fg='red'))
        click.abort()

    # Create SCSS directory
    if not os.path.exists(scss_dir):
        os.makedirs(scss_dir)

    # Create initial files
    create = template_factory(data, project_dir)
    map(create, [
        'scss/_base.scss',
        'scss/main.scss',
        '.editorconfig',
        '.gitignore',
        '.quick',
        'gulpfile.js',
        'index.html',
        'package.json'
    ])

if __name__ == "__main__":
    main()
