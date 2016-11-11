# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import re
import string

from bs4 import BeautifulSoup
from jinja2 import Environment, PackageLoader


# Set up vars
env = Environment(loader=PackageLoader('norman', 'templates'))


# Utility Functions
# -------------------------------

def template_factory(data, out_dir):
    def create_template(template_name):
        template = env.get_template(template_name)
        out = template.render(data=data)
        with open("%s/%s" % (out_dir, template_name), "w") as f:
            f.write(out)
    return create_template


def create_dir(parent, name):
    new = os.path.join(parent, name)
    if not os.path.exists(new):
        os.makedirs(new)


def create_file(parent, name):
    new = os.path.join(parent, name)
    if not os.path.exists(new):
        open(new, 'w').close()


def find_root():
    working_dir = os.getcwd().split(os.sep)
    length = len(working_dir) + 1
    build_paths = filter(lambda x: x != '', ['/'.join(working_dir[:x]) for x in range(length)])
    paths = [x for x in reversed(build_paths)]
    for path in paths:
        test_root = os.path.join(path, '.quick')
        if os.path.isfile(test_root):
            return path
    return None


def create_style_tag(html, css):
    soup = BeautifulSoup(html, 'lxml')
    style = soup.find('style')
    style.string.replace_with(css)
    return soup.prettify()


def replace_containers(html):
    soup = BeautifulSoup(html, 'lxml')
    wrappers = soup.find_all("div", {"class": "container"})
    for container in wrappers:
        table = soup.new_tag('table')
        table.attrs = container.attrs
        table['border'] = 0
        table['cellpadding'] = 0
        table['cellspacing'] = 0

        td = soup.new_tag('td')
        td.contents = container.contents

        tr = soup.new_tag('tr')
        tr.append(td)

        table.append(tr)
        container.replace_with(table)
    return soup.prettify()


def replace_rows(html):
    soup = BeautifulSoup(html, 'lxml')
    rows = soup.find_all("div", {"class": "row"})
    for container in rows:
        table = soup.new_tag('table')
        table.attrs = container.attrs
        table['border'] = 0
        table['cellpadding'] = 0
        table['cellspacing'] = 0

        tr = soup.new_tag('tr')
        tr.contents = container.contents

        table.append(tr)
        container.replace_with(table)

    return soup.prettify()


def replace_cols(html):
    soup = BeautifulSoup(html, 'lxml')
    cols = soup.find_all("div", {"class": "column"})
    for item in cols:
        td = soup.new_tag('td')
        td.contents = item.contents
        td.attrs = item.attrs
        item.replace_with(td)

    return soup.prettify()


def strip_floats(html):
    return html.replace('float:left;', '').replace('float:left', '')


def strip_template_tags(html):
    tag_match = re.compile(r"(<custom[\s\S]*?</custom>)")
    tags = tag_match.findall(html)
    for tag in tags:
        tag_contents = re.findall(r"(?<=\>)[\s\S]*(?=\<\/custom\>)", tag)[0]
        html = html.replace(tag, tag_contents)
    return html

def strip_template_tags_content(html):
    # Make dirs for partials
    root_dir = find_root()
    partials_dir = os.path.join(root_dir, 'partials')
    if not os.path.exists(partials_dir):
        os.makedirs(partials_dir)
    else:
        shutil.rmtree(partials_dir)
        os.makedirs(partials_dir)

    # Process
    tag_match = re.compile(r"(<custom[\s\S]*?</custom>)")
    tags = tag_match.findall(html)
    for tag in tags:
        tag_contents = re.findall(r"(?<=\>)[\s\S]*(?=\<\/custom\>)", tag)[0]
        open_tag = re.findall(r"(?<=<custom).*?(?=>)", tag)[0]
        name = re.findall(r"(?<=name=(?:\"|\')).*?(?=(?:\"|\'))", open_tag)[0]
        fname = os.path.join(partials_dir, "%s.html" % name.lower().replace(" ", "-"))
        with open(fname, 'w') as f:
            f.write(tag_contents.encode('ascii', 'xmlcharrefreplace'))
        replacement = tag.replace(tag_contents, '')
        html = html.replace(tag, replacement)
    return html


def apply_test_transformations(html):
    transformations = [
        replace_containers,
        replace_rows,
        replace_cols,
        strip_floats,
        strip_template_tags
    ]
    return reduce(lambda x, y: y(x), transformations, html).encode('utf8')

def apply_package_transformations(html):
    transformations = [
        replace_containers,
        replace_rows,
        replace_cols,
        strip_floats,
        strip_template_tags_content
    ]
    return reduce(lambda x, y: y(x), transformations, html).encode('utf8')
