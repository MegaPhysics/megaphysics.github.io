# Minify all the import css files under `/assets`

# -------- Standard Libraries -------- #

import os


# -------- Third Party Libraries -------- #

from cssmin import cssmin


def get_assets():
    """ Gets a list of files under the `assets` directory. """

    return os.listdir("./assets")


def minify(filename):
    """ Minify the css in filename. """

    with open("assets/" + filename) as f:
        minified = cssmin(f.read())

    output_fn = filename[:-3] + "min.css"

    with open("assets/" + output_fn, "w") as output:
        output.write(minified)

    return True


def is_css(filename):
    """ Tests if filename has `.css` extension. """

    # If it's already minified, our work is done
    if filename[-8:] == ".min.css":
        return False

    if filename[-4:] == ".css":
        return True

    return False


def main():
    """ Gets list of css files under `assets`, and minifies them. """

    all_files = get_assets()

    css_files = filter(is_css, all_files)

    for f in css_files:
        print "Minifying", f
        minify(f)

if __name__ == "__main__":
    main()
