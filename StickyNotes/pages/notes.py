__author__ = 'p3700473'

import urllib
import cgi
import os

import webapp2
import jinja2

from entities.note import Note
from google.appengine.api import users
from google.appengine.ext import ndb


DEFAULT_NOTEBOOK = 'default_notebook'
POSSIBLE_STATES = ['Done', 'In progress', 'To do']


def notebook_key(notebook_name=DEFAULT_NOTEBOOK):
    """
    Constructs a Datastore key for a Notebook entity

    :param notebook_name:
    :return:
    """
    return ndb.Key('Notebook', notebook_name)


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class NotesPage(webapp2.RequestHandler):
    def get(self):
        notebook_name = self.request.get('notebook_name', DEFAULT_NOTEBOOK)

        notes_query = Note.query(
            ancestor=notebook_key(notebook_name)).order(-Note.date)
        notes = notes_query.fetch(10)

        user = users.get_current_user()
        if not user:
            self.redirect('/')


        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'

        template_values = {
            'user': user,
            'notes': notes,
            'POSSIBLE_STATES': POSSIBLE_STATES,
            'notebook_name': notebook_name,
            'url': url,
            'url_linktext': url_linktext
        }

        template = JINJA_ENVIRONMENT.get_template('html/notes.html')
        self.response.write(template.render(template_values))
