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

    
    # for now i will assume that it works
    def process( self, summary ):
        logging.error( summary )
        return "fahim"

    def post(self):
        
        ifile = self.request.get("summary")
        if not ifile:
            logging.error("no file selected")
            self.redirect( "/addsummary" )
        else:
            s = Summary(
                summary = ifile,
                name = self.process( str(ifile) ) 
            )
            s.put()
            self.redirect( "/archive" )



