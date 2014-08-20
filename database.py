# The database library for the static site generator.

# -------- Third Party Libraries -------- #

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# -------- Project Libraries -------- #

from models import Base, WikiArticle


# -------- Database -------- #

def generate_database():

	"""Generates a database engine and session, and returns the session."""

	# Creates the database engine.
	db = create_engine('sqlite:///megaphysics.db')

	# Creates the session.
	Session = sessionmaker(bind = db)
	session = Session()

	# Creates the database tables (if they do not exist).
	Base.metadata.create_all(db, checkfirst = True)

	return session


def add_article(name):

	"""Adds an article to the database."""

	# Instantiates a database session.
	database = generate_database()

	# Declares a new article.
	article = WikiArticle(name = name)

	# Adds the article to the database.
	database.add(article)
	database.commit()


def list_articles():

	"""Prints out a list of articles in the database."""

	# Instantiates a database session.
	database = generate_database()

	# Creates a query for all articles in the database.
	articles = database.query(WikiArticle).order_by(WikiArticle.id)

	# Prints the results of the query.
	for article in articles:
		print article
