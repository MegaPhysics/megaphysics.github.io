# -------- Standard Libraries -------- #

import os
import re


# -------- Third Party Libraries -------- #

import yaml


# -------- Projecy Libraries -------- #

from megaphysics.database import add_wiki_article


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

    # Check if we're in the root dir.
    if re.search("MegaPhysics$", os.getcwd()) is None:
        raise Exception(
            "This script must be run from the root MegaPhysics directory")

    # Empty the build dir.
    if os.path.isdir("build"):
        os.system("rm -r build")

    os.system("mkdir build")

    # We will make destructive modifications to the articles before passing
    # them to pandoc, so copy them to a temp location first.
    os.system("cp -r articles temp")

    # This dictionary will store all metadata for the articles,
    # this is so we can dynamically generate valid links between articles.
    ARTICLES = {}

    # Get metadata for all the articles
    # TODO: check that all metadata is valid at this point
    # e.g. must have a 'course' field
    for f in files():
        name = re.match("(.+)\.", f).group(1)
        ARTICLES[name] = metadata(f)
        add_wiki_article(ARTICLES[name]['title'])

    try:

        generate_links(ARTICLES)

        for f in files():
            name = re.match("(.+)\.", f).group(1)
            print "rendering " + f
            course = ARTICLES[name].get('course')

            if course is None:
                raise Exception(f + " metadata has no 'course' entry")

            if not os.path.isdir("build/" + course):
                os.system("mkdir build/" + course)

            os.system("pandoc -s -t html5 --template=template.html -o build/"
                + course + "/" + name + ".html" + " temp/" + f)

    finally:
        # Clean up after ourselves
        os.system("rm -r temp")


def generate_links(ARTICLES):

    """Looks for links of the form [text](link) and for those where 'link' is a
    valid article name, replaces 'link' with the correct url to the article.
    """

    for filename in os.listdir("temp"):
        text = open("temp/" + filename).read()

        for match in re.finditer("\[.+?\]\((.+?)\)", text):
            article_name = match.group(1)
            data = ARTICLES.get(article_name)

            if data is None:
                continue

            url = "/" + data["course"] + "/" + article_name + ".html"
            text = re.sub(
                "\]\(" + article_name + "\)",
                "](" + url + ")",
                text)

        with open("temp/" + filename, "w") as f:
            f.write(text)


# -------- Run Code -------- #

run()
