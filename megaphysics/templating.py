# The template generator.

# -------- Standard Libraries -------- #

import os


# -------- Third Party Libraries -------- #

from jinja2 import Environment, PackageLoader


# -------- Template Generator -------- #

def generate_demo_templates():

	"""Creates a demo pair of templates for the site."""

	# Creates a jinja2 environment.
	jinja_env = Environment(loader = PackageLoader('megaphysics', 'templates'))

	# Pulls in two templates.
	base_template = jinja_env.get_template('base_template.html')
	demo_template = jinja_env.get_template('demo_template.html')

	# The location to save the result of the demo.
	BUILD_LOCATION = 'template_demo'

	# Makes sure the demo subdirectory exists.
	if not os.path.isdir(BUILD_LOCATION):
		os.mkdir(BUILD_LOCATION)

	# Renders the demo pages.
	with open('template_demo/base.html', 'w') as f:
		f.write(base_template.render())
	with open('template_demo/demo.html', 'w') as f:
		f.write(demo_template.render())

	print 'Templates rendered. Find them in directory \'' + BUILD_LOCATION + '\'.'
