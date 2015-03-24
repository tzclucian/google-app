__author__ = 'Lucian Tuca'

import webapp2

from pages.add_note import AddNotePage
from pages.notes import NotesPage
from pages.main import MainPage

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add-note', AddNotePage),
    ('/notes', NotesPage)
], debug=True)