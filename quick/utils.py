# -*- coding: utf-8 -*-

import os
import subprocess

from jinja2 import Environment, PackageLoader


# Set up vars
env = Environment(loader=PackageLoader('quick', 'templates'))


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
