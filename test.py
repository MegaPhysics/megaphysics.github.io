import subprocess
from megaphysics.build import run
from BeautifulSoup import BeautifulSoup

article_text = """title: Test
course: Articles
author: Test Author

Test Article
====

This article is a test to ensure that the build system works correctly.

"""


def test_build():
    run()
    return 0


def test_article():
    with open('articles/test.md', 'w') as f:
        f.write(article_text)
    try:
        run()
    except Exception, e:
        raise e
    finally:
        subprocess.call(["rm", "articles/test.md"])
    test = BeautifulSoup(open('build/Articles/test.html', 'r').read()).prettify()
    ref = BeautifulSoup(open('test_article_reference.html', 'r').read()).prettify()
    subprocess.call(["rm", "build/Articles/test.html"])
    print test
    print ref
    assert test == ref, "Rendered article is not the same as reference."
    return 0

if __name__ == "__main__":
    """Assume we are being called by megphys to update the tests"""
    with open('articles/test.md', 'w') as f:
        f.write(article_text)
    run()
    subprocess.call([
        "cp",
        "build/Articles/test.html",
        "test_article_reference.html"])
    subprocess.call(["rm", "articles/test.md"])
