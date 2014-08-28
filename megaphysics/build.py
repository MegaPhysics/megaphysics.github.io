# The build code for the site.

# -------- Standard Libraries -------- #

import os
import re
import subprocess
from functools import partial


# -------- Third Party Libraries -------- #

import yaml


# -------- Project Libraries -------- #

from megaphysics.templating import generate_page
from megaphysics.database import generate_database
from megaphysics.models import Course


# -------- Globals -------- #

BUILD_DIR = os.getcwd()


# -------- Functions -------- #

def files():

    """Returns a list of articles."""

    return os.listdir("./articles")


def metadata(filename):

    """Extract the YAML block at the top of each article and parse it into a
    dictionary.
    """

    with open("./articles/" + filename) as f:
        contents = f.read()

    match = re.search('---\n(.+?)\n---', contents, flags=re.DOTALL)
    yaml_block = match.group(1)

    return yaml.load(yaml_block)


def generate_base_site(articles_metadata):

    # Creates homepage.
    generate_page('home.html', 'build/index.html')

    # Creates about page.
    generate_page('about.html', 'build/about.html')

    # Creates articles index.
    generate_page('articles.html',
                  'build/articles.html',
                  articles = articles_urls(articles_metadata))

    # Creates courses index.
    generate_page('courses.html',
                  'build/courses.html',
                  articles = courses(articles_metadata))


def run():

    """Runs the build."""

    # Check if we're in the root dir.
    if re.search("MegaPhysics$", os.getcwd()) is None:
        raise Exception(
            "This script must be run from the root MegaPhysics directory")

    # Empty the build dir.
    if os.path.isdir("build"):
        subprocess.call(['rm', '-r', 'build'])

    subprocess.call(['mkdir', 'build'])

    # We will make destructive modifications to the articles before passing
    # them to pandoc, so copy them to a temp location first.
    subprocess.call(['cp', '-r', 'articles', 'temp'])

    # Get metadata for all the articles
    # TODO: check that all metadata is valid at this point
    # e.g. must have a 'course' field
    # This dictionary will store all metadata for the articles,
    # this is so we can dynamically generate valid links between articles.
    articles_metadata = {}

    for f in files():
        name = re.match("(.+)\.", f).group(1)
        articles_metadata[name] = metadata(f)

    try:

        generate_links(articles_metadata)

        # Builds each individual article page.
        for f in files():
            if f[0] == ".":
                break

            name = re.match("(.+)\.", f).group(1)
            print "rendering " + f
            course = articles_metadata[name].get('course')

            if course is None:
                raise Exception(f + " metadata has no 'course' entry")

            if not os.path.isdir("build/" + course):
                subprocess.call(['mkdir', 'build/' + course])

            content = subprocess.check_output(["pandoc", "-t", "html5",
                                               "--template=" + BUILD_DIR +
                                               "/template.html", BUILD_DIR +
                                               "/temp/" + f])

            article_path = 'build/' + course + '/' + name + '.html'
            generate_page('article.html', article_path, content = content)

        # Builds the core site pages (index, about etc.).
        generate_base_site(articles_metadata)

        subprocess.call(['cp', '-r', 'assets', 'build/assets'])

    finally:
        # Clean up after ourselves
        subprocess.call(['rm', '-r', 'temp'])


def generate_links(articles_metadata):

    """Looks for links of the form [text](link) and for those where 'link' is a
    valid article name, replaces 'link' with the correct url to the article.
    """

    for filename in os.listdir("temp"):
        text = open("temp/" + filename).read()

        image = image_link(filename.replace(".md", ""))
        text = re.sub("\!\[(.+?)\]\((.+?)\)", image, text)
        text = re.sub(
            "\[(.+?)\]\((.+?)\)",
            partial(article_link,
            articles_metadata),
            text)

        with open("temp/" + filename, "w") as f:
            f.write(text)


def image_link(article_name):

    """A generator for functions that can be passed to re.sub to format
    image links.
    Returns a function that expects a match of the form [alt text](image name)
    and returns the correct (markdown formatted) link for the image.
    """

    def repl(match):
        alt_text = match.group(1)
        image_name = match.group(2)
        return "![" + alt_text + "]" + "(/assets/article_assets/" + \
            article_name + "/images/" + image_name + ")"

    return repl


def article_link(articles_metadata, match):

    """A replace function that can be passed to re.sub.
    Expects a match of the form [link text](article name) and returns the
    correct (markdown formatted) link for the article.
    """

    link_text = match.group(1)
    article_name = match.group(2)
    data = articles_metadata.get(article_name)

    if data is None:
        return "[" + link_text + "](" + article_name + ")"

    return "[" + link_text + "](/" + data["course"] + "/" + article_name + \
        ".html)"


def articles_urls(articles_metadata):

    """Returns a list of {title, url} dictionaries, one for each article."""

    articles = []
    for a in articles_metadata.keys():
        meta = articles_metadata[a]
        url = "/"+meta["course"]+"/"+a+".html"
        articles.append({'title': meta['title'], 'url': url})
    return articles


def courses(articles_metadata):

    """Returns an array of (unique) courses."""

    courses = set()
    for a in articles_metadata.keys():
        courses.add(articles_metadata[a]['course'])
    return list(courses)


def courses_list():

    """Pulls in and returns a list of courses from the database."""

    # Creates database session.
    db = generate_database()
    course_list = db.query(Course).order_by(Course.name)

    return course_list
