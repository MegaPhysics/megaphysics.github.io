# Minify all the import css files under `/assets`

# -------- Standard Libraries -------- #

import os


# -------- Third Party Libraries -------- #

from cssmin import cssmin


# -------- Functions -------- #

def minify_css(css_file):

	""" Minify the css in filename. """

	with open(css_file, 'r') as f:
		contents = f.read()

	if css_file.endswith('.min.css'):
		return contents
	else:
		return cssmin(contents)


def compress_assets(directory):

	""" Gets list of css files, minifies them. """

	print 'Compressing assets...'

	with open('build/assets/styles.min.css', 'w') as mincss, \
		open('build/assets/scripts.min.js', 'w') as minjs:

		for path, dirs, files in os.walk(directory):

			for f in files:

				if f.endswith('.css'):
					filepath = os.path.join(path, f)
					minified_css = minify_css(filepath)
					mincss.write(minified_css)

				elif f.endswith('js'):

					filepath = os.path.join(path, f)
					with open(filepath, 'r') as jsfile:
						contents = jsfile.read()
					minjs.write(contents)
