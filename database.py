# The database library for the static site generator.

# -------- Third Party Libraries -------- #

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# -------- Project Libraries -------- #

from models import Base, WikiArticle, Course, CourseArticle


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


def add_wiki_article(name):

	"""Adds a wiki article to the database."""

	# Instantiates a database session.
	database = generate_database()

	# Declares a new article.
	article = WikiArticle(name = name)

	# Adds the article to the database.
	database.add(article)
	database.commit()


def add_course(course_name):

	"""Adds a course to the database."""

	# Instantiates a database session.
	database = generate_database()

	# Declares a new course.
	course = Course(name = course_name)

	# Adds the course to the database.
	database.add(course)
	database.commit()


def add_course_article(name, course_name):

	"""Adds a course article to the database."""

	# Instantiates a database session.
	database = generate_database()

	# Declares a new article.
	article = CourseArticle(name = name)
	course = database.query(Course).filter(Course.name == course_name)
	article.course_id = course[0].id

	# Adds the article to the database.
	database.add(article)
	database.commit()


def list_articles():

	"""Prints out a list of articles in the database."""

	# Instantiates a database session.
	database = generate_database()

	# Creates and executes queries for all articles in the database.
	wiki_articles = database.query(WikiArticle).order_by(WikiArticle.name).all()
	course_articles = database.query(CourseArticle).order_by(
		CourseArticle.name).all()

	# Puts all articles in one list.
	articles = wiki_articles + course_articles

	# Prints the results of the query.
	for article in articles:
		print article
