# The template generator.

import os

# -------- Third Party Libraries -------- #

from jinja2 import Environment, PackageLoader


# -------- Template Generator -------- #

environment = Environment(loader=PackageLoader('megaphysics', 'templates'))
if 'MEGPHYS_ROOT' in os.environ:
    environment.globals['ROOT'] = os.environ['MEGPHYS_ROOT']
else:
    environment.globals['ROOT'] = "/"


def generate_page(template, filepath, **kwargs):

    """Renders a page to a file, given a template and the path of the file."""

    page = environment.get_template(template)

    with open(filepath, 'w') as f:
        f.write(page.render(**kwargs).encode('utf-8'))
