from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users 

import os
import conf
import logging
from model import Story
from common import get_user

class FrontPage( webapp.RequestHandler ):
    
    user, login_url, logout_url, username = None, None, None, None 

    @get_user
    def get(self):

        q = db.Query( Story )
        q.order( "-entrytime" )
        stories = q.fetch( 7 ) # seven was lucky!
        
        template_values = {
            'is_debug' : conf.DEBUG,
            'user'     : self.user,
            'username' : self.username,
            'login_url' : self.login_url,
            'logout_url' : self.logout_url,
            'stories' : stories
        }
        
        path = os.path.join( conf.APP_ROOT, 'templates', 'frontpage.html' )
#        logging.error( conf.TEMPLATE_DIRS )
        self.response.out.write( template.render( path, template_values ) )

