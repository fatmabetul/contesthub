from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db

from datetime import datetime

import os
import conf
import logging
from model import Story
from model import Summary

class AddSummary( webapp.RequestHandler ):
    def get(self):
        template_values = {
            'is_debug' : conf.DEBUG
        }
        
        path = os.path.join( conf.APP_ROOT, 'templates', 'addsummary.html' )
        self.response.out.write( template.render( path, template_values ) )


    def process( self, summary ):
        return "fahim"

    def post(self):
        
        ifile = self.request.get("summary")
        s = Summary(
            summary = db.Blob( str(ifile) ),
            name = self.process( ifile ) 
        )
        
        if not s.summary :
            logging.error("no file selected")
        else:
            s.put()

        self.redirect( "/" )



