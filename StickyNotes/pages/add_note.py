__author__ = 'Lucian Tuca'

import urllib

import webapp2

from google.appengine.api import users
from google.appengine.api import mail
from entities.note import Note
from entities.author import Author
from pages.notes import DEFAULT_NOTEBOOK, notebook_key


class AddNotePage(webapp2.RequestHandler):
    def post(self):
        notebook_name = self.request.get('notebook_name', DEFAULT_NOTEBOOK)
        note = Note(parent=notebook_key(notebook_name))

        if users.get_current_user():
            note.author = Author(
                identity=users.get_current_user().user_id(),
                email=users.get_current_user().email())

        note.title = self.request.get('content')
        note.content = self.request.get('description')
        note.state = self.request.get('state')
        note.color = self.request.get('color')

        note.put()
        self.send_mail(note.title, note.content, users.get_current_user().email())

        query_params = {'notebook_name': notebook_name}
        self.redirect('/notes?' + urllib.urlencode(query_params))


    def send_mail(self, title, content, to_email):
        message = mail.EmailMessage()
        message.sender = users.get_current_user().email()
        message.to = to_email

        message.subject = "New note added: " + title
        message.body = "You have added a new note to the notes application. You can find the note content below: %s" % content
        message.send()