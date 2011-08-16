from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import os
import conf
from handlers import FrontPage, Hello, NSURank, Error 
from handlers import AddStory, AddSummary, Archive, ShowSummary
from handlers import AddEvent, Events, AddContest

__application__ = webapp.WSGIApplication(
    [
        ('/hello', Hello),
        ('/addstory', AddStory),
        ('/addsummary', AddSummary),
        ('/addevent', AddEvent),
        ('/contests', AddContest),
        ('/nsurank', NSURank),
        ('/events', Events),
        ('/error', Error),
        ('/summary/([^/]+)?', ShowSummary),
        ('/archive', Archive),
        ('/', FrontPage),
    ],
    debug=conf.DEBUG)

def main():
    run_wsgi_app( __application__ )

if __name__ == "__main__" :
    main()
