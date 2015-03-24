__author__ = 'Lucian Tuca'

import re
import urllib

import webapp2

from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.api import users
from pages.notes import DEFAULT_NOTEBOOK


class UpdateNotePage(webapp2.RequestHandler):
    def post(self):
        notebook_name = self.request.get('notebook_name', DEFAULT_NOTEBOOK)

        desired_action = self.request.get('desired_action')
        desired_note = self.request.get('note')

        # Obtaining the key values
        key_strings = re.findall("Key\((.*)\), au", desired_note)[0]

        key_values = key_strings.split(',')
        new_keys = []

        for i in range(0, len(key_values) - 1):
            new_keys.append(key_values[i].replace(' ', '').replace("'", ""))
        new_keys.append(long(key_values[3].replace(' ', '').replace("'", "")))

        # Build the key to the desired note based on the parsed parameters
        note_key = ndb.Key(new_keys[0], new_keys[1], new_keys[2], new_keys[3])

        if desired_action == 'Delete':
            note = note_key.get()
            note.key.delete()
            self.send_mail("Your note has been deleted",
                           "Your note %s has just been deleted from the notebook: %s" % (note.title, notebook_name),
                           users.get_current_user().email())
        else:
            note = note_key.get()
            note.state = desired_action
            note.put()
            self.send_mail("Your note has been updated",
                           "Your note %s has been updated. Its state changed to %s" % (note.title, note.state),
                           users.get_current_user().email())

        query_params = {'notebook_name': notebook_name}
        self.redirect('/notes?' + urllib.urlencode(query_params))

    def send_mail(self, title, content, to_email):
        message = mail.EmailMessage()
        message.sender = users.get_current_user().email()
        message.to = to_email

        message.subject = title
        message.body = content
        message.send()