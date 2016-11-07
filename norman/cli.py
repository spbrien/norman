# -*- coding: utf-8 -*-

import os

import click
from premailer import transform
from bs4 import BeautifulSoup

from sender import Mailer
from utils import *


@click.group()
def main():
    """Utility script for working with emails"""


@main.command()
@click.argument('project')
def start(project):
    """Start a new project."""
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


@main.command()
def process():
    """
    Transpile your code into email-ready html.
    A file called out.html will be created in your project root.
    """
    root_dir = find_root()
    if not root_dir:
        click.echo(click.style("You are not in a quick project directory!", fg='red'))

    # ---------------------------------------------------
    filename = os.path.join(root_dir, 'index.html')
    css_filename = os.path.join(root_dir, 'css/main.min.css')
    with open(filename, 'r') as f:
        html = transform(f.read())
        css = open(css_filename, 'r').read()
        out = replace_cols(replace_rows(replace_containers(create_style_tag(html, css)))).replace('float:left;', '').replace('float:left', '')

    with open('out.html', 'w') as f:
        f.write(out.encode('utf8'))
    # ---------------------------------------------------


@main.command()
@click.argument('recipients', nargs=-1)
@click.option(
    '--domain',
    prompt=True,
    default=lambda: os.environ.get('MAILGUN_DOMAIN'),
    help='Mailgun Domain'
)
@click.option(
    '--api_key',
    prompt=True,
    default=lambda: os.environ.get('MAILGUN_API_KEY'),
    help='Mailgun API Key'
)
def test(domain, api_key, recipients):
    """
    Send a test of your email.
    """
    if not os.environ.get('CLOUDINARY_URL'):
        click.echo(click.style("\n[!] You must set the CLOUDINARY_URL environment variable to use this script.", fg='red'))
        click.abort()

    root_dir = find_root()

    # ---------------------------------------------------
    ind = os.path.join(root_dir, 'index.html')
    css_filename = os.path.join(root_dir, 'css/main.min.css')
    with open(ind, 'r') as f:
        html = transform(f.read())
        css = open(css_filename, 'r').read()
        out = replace_cols(replace_rows(replace_containers(create_style_tag(html, css)))).replace('float:left;', '').replace('float:left', '')

    with open('out.html', 'w') as f:
        f.write(out.encode('utf8'))
    # ---------------------------------------------------

    # ---------------------------------------------------
    filename = os.path.join(root_dir, 'out.html')
    f = open(filename, 'r')
    html = f.read()

    mailer = Mailer(domain, api_key)
    click.echo(click.style("\n[+] Uploading images...", fg='white'))
    hosted = mailer.host_images(html)
    click.echo(click.style("[+] Sending test email...", fg='white'))
    mailer.send_email(hosted, recipients)
    # ---------------------------------------------------

    click.echo(click.style("[!] Finished", fg='white'))

if __name__ == "__main__":
    main()
