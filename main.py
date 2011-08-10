from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import os
import conf
from handlers import FrontPage, Hello, NSURank
from handlers import AddStory, AddSummary, Archive, ShowSummary

__application__ = webapp.WSGIApplication(
    [
        ('/hello', Hello),
        ('/addstory', AddStory),
        ('/addsummary', AddSummary),
        ('/nsurank', NSURank),
        ('/summary/([^/]+)?', ShowSummary),
        ('/archive', Archive),
        ('/', FrontPage),
    ],
    debug=conf.DEBUG)

def main():
    run_wsgi_app( __application__ )

if __name__ == "__main__" :
    main()
