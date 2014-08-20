# The models for the static site generator.

# -------- Standard Libraries -------- #

from datetime import datetime


# -------- Third Party Libraries -------- #

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime


# -------- Initialisation -------- #

# Creates the 'base' class, from which all models are derived.
Base = declarative_base()


# -------- Models -------- #

class WikiArticle(Base):

	"""A model used to store individual wiki articles."""

	# Defines table name in database.
	__tablename__ = 'wiki_articles'

	id = Column(Integer, primary_key = True)
	name = Column(String)
	creation_date = Column(DateTime, default = datetime.utcnow)

	# Returns human readable name when object is called.
	def __repr__(self):
		return 'WikiArticle: ' + self.name
