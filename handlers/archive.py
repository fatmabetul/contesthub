from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db

import os
import conf
import logging
from model import Story, Summary

class Archive( webapp.RequestHandler ):
    def get(self):

        q = db.Query( Summary )
        q.order( "entrytime" )
        ranklists = q.fetch(1000) 

        template_values = {
            'is_debug' : conf.DEBUG,
             'ranklists' : ranklists 
        }
        
        path = os.path.join( conf.APP_ROOT, 'templates', 'archive.html' )
#        logging.error( conf.TEMPLATE_DIRS )
        self.response.out.write( template.render( path, template_values ) )


