from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import os
import conf
from handlers import FrontPage, Hello
from handlers import AddStory

__application__ = webapp.WSGIApplication(
    [
        ('/hello', Hello),
        ('/addstory', AddStory),
        ('/', FrontPage),
    ],
    debug=conf.DEBUG)

def main():
    run_wsgi_app( __application__ )

if __name__ == "__main__" :
    main()
