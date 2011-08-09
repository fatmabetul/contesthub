from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db

import os
import conf
import logging
from model import Summary 

class ShowSummary( webapp.RequestHandler ):
    def get(self, key):
        if not key:
            logging.error( "no key found" ) 
        else:
            s = Summary.get(key)
            if s:
                template_values = {
                    'is_debug' : conf.DEBUG,
                     'summaryfile' : s.summary,
                     'name' : s.name
                }
                
                path = os.path.join( conf.APP_ROOT, 'templates', 'summary.html' )
                self.response.out.write( template.render( path, template_values ) )

