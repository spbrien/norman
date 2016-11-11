# -*- coding: utf-8 -*-

import os
import shutil

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
@click.option(
    '--filename',
    default='index.html',
    help='Filename'
)
def test(filename, domain, api_key, recipients):
    """
    Send a test of your email.
    """
    if not os.environ.get('CLOUDINARY_URL'):
        click.echo(click.style("\n[!] You must set the CLOUDINARY_URL environment variable to use this script.", fg='red'))
        click.abort()

    root_dir = find_root()

    # ---------------------------------------------------
    ind = os.path.join(root_dir, filename)
    css_filename = os.path.join(root_dir, 'css/main.min.css')
    with open(ind, 'r') as f:
        html = transform(f.read())
        css = open(css_filename, 'r').read()
        out = apply_test_transformations(create_style_tag(html, css))

    out_filename = os.path.join(root_dir, "out-%s" % filename)
    with open(out_filename, 'w') as f:
        f.write(out.decode('utf8').encode('ascii', 'xmlcharrefreplace'))
    # ---------------------------------------------------

    # ---------------------------------------------------
    f = open(out_filename, 'r')
    html = f.read()

    mailer = Mailer(domain, api_key)
    click.echo(click.style("\n[+] Uploading images...", fg='white'))
    hosted = mailer.host_images(html)
    click.echo(click.style("[+] Sending test email...", fg='white'))
    mailer.send_email(hosted, recipients)
    # ---------------------------------------------------

    os.remove(out_filename)
    click.echo(click.style("[!] Finished", fg='white'))


@main.command()
@click.option(
    '--filename',
    default='index.html',
    help='Filename'
)
def package(filename):
    """
    Transpile your code into email-ready html.
    A directory called dist will be created in your project root.
    """
    root_dir = find_root()
    if not root_dir:
        click.echo(click.style("You are not in a Norman project directory!", fg='red'))

    # ---------------------------------------------------
    fname = os.path.join(root_dir, filename)
    css_filename = os.path.join(root_dir, 'css/main.min.css')
    with open(fname, 'r') as f:
        html = transform(f.read())
        css = open(css_filename, 'r').read()
        out = apply_package_transformations(create_style_tag(html, css))

    with open('out.html', 'w') as f:
        f.write(out.decode('utf8').encode('ascii', 'xmlcharrefreplace'))
    # ---------------------------------------------------

    dist_dir_name = os.path.join(root_dir, 'dist')
    if not os.path.exists(dist_dir_name):
        os.makedirs(dist_dir_name)
    else:
        shutil.rmtree(dist_dir_name)
        os.makedirs(dist_dir_name)

    shutil.copytree(
        os.path.join(root_dir, 'images'),
        os.path.join(dist_dir_name, 'images')
    )

    shutil.copy(
        os.path.join(root_dir, 'out.html'),
        os.path.join(dist_dir_name, 'index.html')
    )

    os.remove(os.path.join(root_dir, 'out.html'))

    package = os.path.join(root_dir, 'package')
    partials = os.path.join(root_dir, 'partials')
    if not os.path.exists(package):
        os.makedirs(package)
    else:
        shutil.rmtree(package)
        os.makedirs(package)

    shutil.copytree(
        partials,
        os.path.join(package, 'partials')
    )

    shutil.copytree(
        dist_dir_name,
        os.path.join(package, 'dist')
    )

    shutil.rmtree(partials)
    shutil.rmtree(dist_dir_name)

    archive = "%s.zip" % filename.split('.')[0]
    shutil.make_archive(os.path.join(root_dir, archive), 'zip', package)


if __name__ == "__main__":
    main()
