from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users 

import os
import conf
import logging
from model import Coder 
from common import get_user

class NSURank( webapp.RequestHandler ):
    
    user, login_url, logout_url, username = None, None, None, None 
        
    @get_user
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
            'username'  : self.username,
            'user'      : self.user,
            'login_url' : self.login_url,
            'logout_url' : self.logout_url,
            'coders'  : coders
        }
        
        path = os.path.join( conf.APP_ROOT, 'templates', 'nsurank.html' )
#        logging.error( conf.TEMPLATE_DIRS )
        self.response.out.write( template.render( path, template_values ) )

