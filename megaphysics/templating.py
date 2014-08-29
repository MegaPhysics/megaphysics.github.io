# The template generator.

# -------- Third Party Libraries -------- #

from jinja2 import Environment, PackageLoader


# -------- Template Generator -------- #

def create_jinja_env():

    """Returns a jinja2 environment."""

    return Environment(loader=PackageLoader('megaphysics', 'templates'))


def generate_page(template, filepath, **kwargs):

    """Renders a page to a file, given a template and the path of the file."""

    environment = create_jinja_env()
    page = environment.get_template(template)

    with open(filepath, 'w') as f:
        f.write(page.render(**kwargs).encode('utf-8'))
