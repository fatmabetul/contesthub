from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db

import os
import conf
import logging
from model import Coder 

class NSURank( webapp.RequestHandler ):
    def get(self):

        q = db.Query( Coder )
        q.order( "-points" )
        coders = q.fetch( 1000 )
       
        # find the rank of each coder
        rank, last, total = 0, 100000, 0

        for coder in coders:
            if coder.points != last:
                rank = total + 1
            coder.rank = rank
            last = coder.points
            total += 1
            coder.put()

        template_values = {
            'is_debug' : conf.DEBUG,
             'coders'  : coders
        }
        
        path = os.path.join( conf.APP_ROOT, 'templates', 'nsurank.html' )
#        logging.error( conf.TEMPLATE_DIRS )
        self.response.out.write( template.render( path, template_values ) )

