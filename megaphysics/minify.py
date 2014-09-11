# Handles asset minification and compression.

# -------- Standard Libraries -------- #

import os


# -------- Third Party Libraries -------- #

from cssmin import cssmin


# -------- Functions -------- #

def read_css(css_file):

	"""Returns the contents of a CSS file. If the file has not been minified,
	does so.
	"""

	with open(css_file, 'r') as f:
		contents = f.read()

	if css_file.endswith('.min.css'):
		return contents
	else:
		return cssmin(contents)


def compress_assets(jquery_location, assets_location):

	"""Gets the CSS files and minifies them. Combines all the CSS into
	one file, and all the js into another.
	"""

	print 'Compressing assets...'

	# Opens files to be populated with minifed content.
	with open('build/assets/styles.min.css', 'w') as mincss, \
		open('build/assets/scripts.min.js', 'w') as minjs:

		# Makes sure to write the jquery in first, as other things rely on it.
		with open(jquery_location, 'r') as jquery:
			minjs.write(jquery.read())

		# Walks the asset directory.
		for path, dirs, files in os.walk(assets_location):

			# Runs through all the files found.
			for f in files:

				# Handles the CSS files.
				if f.endswith('.css'):
					filepath = os.path.join(path, f)
					minified_css = read_css(filepath)
					mincss.write(minified_css)

				# Handles the js files.
				elif f.endswith('.js'):
					filepath = os.path.join(path, f)
					with open(filepath, 'r') as jsfile:
						contents = jsfile.read()
					minjs.write(contents)
