from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db

import os
import conf
import logging
from model import Story

class FrontPage( webapp.RequestHandler ):
    def get(self):

        q = db.Query( Story )
        q.order( "-entrytime" )
        stories = q.fetch( 7 )


        template_values = {
            'is_debug' : conf.DEBUG,
             'stories' : stories
        }
        
        path = os.path.join( conf.APP_ROOT, 'templates', 'frontpage.html' )
#        logging.error( conf.TEMPLATE_DIRS )
        self.response.out.write( template.render( path, template_values ) )

