# The template generator.

# -------- Standard Libraries -------- #

import os


# -------- Third Party Libraries -------- #

from jinja2 import Environment, PackageLoader


# -------- Template Generator -------- #

def generate_templates():

	"""Creates a demo pair of templates for the site."""

	# The location to save the result of the demo.
	BUILD_LOCATION = 'template_demo'

	# Makes sure the demo subdirectory exists.
	if not os.path.isdir(BUILD_LOCATION):
		os.mkdir(BUILD_LOCATION)

	# Creates a jinja2 environment.
	jinja_env = Environment(loader = PackageLoader('megaphysics', 'templates'))

	# Cycles through templates and renders them.
	for template in os.listdir('megaphysics/templates'):

		# Only includes html files, and excludes stuff like the base template.
		if template.endswith('.html') and 'template' not in template:
	
			# Pull in template.
			page = jinja_env.get_template(template)
			# Render to file.
			with open('template_demo/' + template, 'w') as f:
				f.write(page.render())

	print 'Templates rendered. Find them in directory \'' + BUILD_LOCATION + '\'.'
