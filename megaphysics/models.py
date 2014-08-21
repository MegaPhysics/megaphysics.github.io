# The models for the static site generator.

# -------- Standard Libraries -------- #

from datetime import datetime


# -------- Third Party Libraries -------- #

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


# -------- Initialisation -------- #

# Creates the 'base' class, from which all models are derived.
Base = declarative_base()


# -------- Models -------- #

class WikiArticle(Base):

	"""A model used to store individual wiki articles."""

	# Defines table name in database.
	__tablename__ = 'wiki_article'

	id = Column(Integer, primary_key = True)
	name = Column(String)
	creation_date = Column(DateTime, default = datetime.utcnow)

	# Returns human readable name when object is called.
	def __repr__(self):
		return 'WikiArticle: ' + self.name


class Course(Base):

	"""A model used to store courses."""

	# Defines table name in database.
	__tablename__ = 'course'

	id = Column(Integer, primary_key = True)
	name = Column(String)

	# Links a course to a collection of articles.
	articles = relationship('CourseArticle', backref = 'course')

	# Returns human readable name when object is called.
	def __repr__(self):
		return 'Course: ' + self.name


class CourseArticle(Base):

	"""A model used to store individual course articles."""

	# Defines table name in database.
	__tablename__ = 'course_article'

	id = Column(Integer, primary_key = True)
	name = Column(String)
	creation_date = Column(DateTime, default = datetime.utcnow)

	# Links each article to a course.
	course_id = Column(String, ForeignKey('course.id'))

	# Returns human readable name when object is called.
	def __repr__(self):
		return 'CourseArticle: ' + self.name
