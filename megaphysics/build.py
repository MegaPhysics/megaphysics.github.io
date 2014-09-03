# The build code for the site.

# -------- Standard Libraries -------- #

import os
import re
import subprocess


# -------- Third Party Libraries -------- #

import yaml
import markdown


# -------- Project Libraries -------- #

import megaphysics.views
from megaphysics.urls import generate_links


# -------- Globals -------- #

BUILD_DIR = os.getcwd()


# -------- Functions -------- #

def files():

    """Returns a list of articles."""

    return os.listdir("./articles")


def metadata(filename):

    """Extract the metadata block at the top of each article and parse it into a
    dictionary.
    """

    with open("./articles/" + filename) as f:
        contents = f.read()

    md = markdown.Markdown(extensions=['meta'])
    md.convert(contents)
    meta = md.Meta
    meta["course"] = meta["course"][0]
    meta["title"] = meta["title"][0]
    meta["author"] = meta["author"][0]
    return meta


def generate_base_site(articles_metadata):

    """Builds the core site pages (index, about etc.)."""

    megaphysics.views.index()
    megaphysics.views.about()
    megaphysics.views.article_list(articles_metadata)
    megaphysics.views.course_list(articles_metadata)


def run():

    """Runs the build."""

    # Check if we're in the root dir.
    if re.search("MegaPhysics$", os.getcwd()) is None:
        raise Exception(
            "This script must be run from the root MegaPhysics directory")

    # Empty and recreate the build dir.
    if os.path.isdir("build"):
        subprocess.call(['rm', '-r', 'build'])
    subprocess.call(['mkdir', 'build'])

    # We will make destructive modifications to the articles before passing
    # them to pandoc, so copy them to a temp location first.
    subprocess.call(['cp', '-r', 'articles', 'temp'])

    # This dictionary will store all metadata for the articles,
    # this is so we can dynamically generate valid links between articles.
    articles_metadata = {}

    # Get metadata for all the articles
    # TODO: check that all metadata is valid at this point
    # e.g. must have a 'course' field
    for f in files():
        name = re.match("(.+)\.", f).group(1)
        articles_metadata[name] = metadata(f)

    try:

        generate_links(articles_metadata)

        # Builds each individual article page.
        for f in files():
            if f[0] == ".":
                break
            megaphysics.views.generate_article(f, articles_metadata, BUILD_DIR)

        # Builds the core site pages (index, about etc.).
        generate_base_site(articles_metadata)

        # Copies in the assets folder.
        subprocess.call(['cp', '-r', 'assets', 'build/assets'])

    finally:
        # Clean up after ourselves
        subprocess.call(['rm', '-r', 'temp'])
