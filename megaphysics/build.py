# -------- Standard Libraries -------- #

import os
import re
import subprocess


# -------- Third Party Libraries -------- #

import yaml
from jinja2 import Environment, PackageLoader

# -------- Globals -------- #

# This dictionary will store all metadata for the articles,
# this is so we can dynamically generate valid links between articles.
ARTICLES = {}
jinja = Environment(loader=PackageLoader('megaphysics', 'templates'))
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


def run():

    """Runs the build."""

    global jinja

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
    global ARTICLES
    for f in files():
        name = re.match("(.+)\.", f).group(1)
        ARTICLES[name] = metadata(f)

    try:

        generate_links(ARTICLES)

        for f in files():
            name = re.match("(.+)\.", f).group(1)
            print "rendering " + f
            course = ARTICLES[name].get('course')

            if course is None:
                raise Exception(f + " metadata has no 'course' entry")

            if not os.path.isdir("build/" + course):
                subprocess.call(['mkdir', 'build/'+course])

            content = subprocess.check_output(["pandoc", "-t", "html5",
                                               "--template=" + BUILD_DIR +
                                               "/template.html", BUILD_DIR +
                                               "/temp/" + f])

            page = jinja.get_template("article.html")
            with open('build/' + course + '/' + name + '.html', 'w') as f:
                f.write(page.render(content=content))

        subprocess.call(['cp', '-r', 'assets', 'build/assets'])

    finally:
        # Clean up after ourselves
        subprocess.call(['rm', '-r', 'temp'])


def generate_links(ARTICLES):

    """Looks for links of the form [text](link) and for those where 'link' is a
    valid article name, replaces 'link' with the correct url to the article.
    """

    for filename in os.listdir("temp"):
        text = open("temp/" + filename).read()

        image = image_link(filename.replace(".md", ""))
        text = re.sub("\!\[(.+?)\]\((.+?)\)", image, text)
        text = re.sub("\[(.+?)\]\((.+?)\)", article_link, text)

        with open("temp/" + filename, "w") as f:
            f.write(text)


def image_link(article_name):

    def repl(match):
        alt_text = match.group(1)
        image_name = match.group(2)
        return "![" + alt_text + "]" + "(/assets/article_assets/" + \
            article_name + "/images/" + image_name + ")"

    return repl


def article_link(match):

    global ARTICLES
    link_text = match.group(1)
    article_name = match.group(2)
    data = ARTICLES.get(article_name)

    if data is None:
        return "[" + link_text + "](" + article_name + ")"

    return "[" + link_text + "](/" + data["course"] + "/" + article_name + \
        ".html)"
