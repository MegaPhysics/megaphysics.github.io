# Defines the handling of urls and linking for the site.

# -------- Standard Libraries -------- #

import os
import re
from functools import partial


# -------- Globals -------- #

if 'MEGPHYS_ROOT' in os.environ:
    ROOT = os.environ['MEGPHYS_ROOT']
else:
    ROOT = "/"
 

# -------- URLs and Linking -------- #

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
            partial(article_link, articles_metadata),
            text)

        with open("temp/" + filename, "w") as f:
            f.write(text)


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

    return "[" + link_text + "](" + ROOT + data["course"] + "/" + article_name + \
        ".html)"


def articles_urls(articles_metadata):

    """Returns a list of {title, url} dictionaries, one for each article."""

    articles = []
    for a in articles_metadata.keys():
        meta = articles_metadata[a]
        url = ROOT + meta["course"] + "/" + a + ".html"
        articles.append({'title': meta['title'], 'url': url})
    return articles


def image_link(article_name):

    """A generator for functions that can be passed to re.sub to format
    image links.
    Returns a function that expects a match of the form [alt text](image name)
    and returns the correct (markdown formatted) link for the image.
    """

    def repl(match):
        alt_text = match.group(1)
        image_name = match.group(2)
        return "![" + alt_text + "]" + "(" + ROOT + "assets/article_assets/" + \
            article_name + "/images/" + image_name + ")"

    return repl
