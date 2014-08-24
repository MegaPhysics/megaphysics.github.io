from megaphysics.build import run
from megaphysics.templating import generate_templates
from megaphysics.database import generate_database


def test_build():

    run()

    return 0


def test_templates():

    generate_templates()

    return 0


def test_database():

    generate_database()

    return 0
