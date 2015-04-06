__author__ = 'Lucian Tuca'

from google.appengine.ext import ndb
from author import Author


class Note(ndb.Model):
    """
    A main model for representing an individual Notebook entry.
    """
    author = ndb.StructuredProperty(Author)
    title = ndb.StringProperty(indexed=False)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

    state = ndb.StringProperty(indexed=False)
    color = ndb.StringProperty(indexed=False)