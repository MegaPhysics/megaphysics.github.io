# The views for the site.

# -------- Standard Libraries -------- #

import os
import re
import subprocess


# -------- Project Libraries -------- #

from megaphysics.templating import generate_page
from megaphysics.urls import articles_urls


# -------- Views -------- #

def index():

	"""Creates the home page."""

	generate_page('home.html', 'build/index.html')


def about():

	"""Creates the about page."""

	generate_page('about.html', 'build/about.html')


def article_list(articles_metadata):

	"""Generates a list of all articles on the site."""

	generate_page(
		'articles.html',
		'build/articles.html',
		articles = articles_urls(articles_metadata)
	)


def course_list(articles_metadata):

	"""Generates a list of all courses on the site."""

	courses = set()

	for a in articles_metadata.keys():
		courses.add(articles_metadata[a]['course'])

	courses = list(courses)

	generate_page(
		'courses.html',
		'build/courses.html',
		courses = courses
	)


def generate_article(f, articles_metadata, build_dir):

	"""Creates the page for an article."""

	name = re.match("(.+)\.", f).group(1)
	print "rendering " + f
	course = articles_metadata[name].get('course')

	if course is None:
		raise Exception(f + " metadata has no 'course' entry")

	if not os.path.isdir("build/" + course):
		subprocess.call(['mkdir', 'build/' + course])

	content = subprocess.check_output([
		"pandoc",
		"-t",
		"html5",
		"--template=" + build_dir +
		"/template.html", build_dir +
		"/temp/" + f
	])

	article_path = 'build/' + course + '/' + name + '.html'
	generate_page('article.html', article_path, content = content)
