from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users 

from datetime import datetime

import os
import conf
import logging
from model import Story
from common import get_user, moderator

class AddStory( webapp.RequestHandler ):
    
    user, login_url, logout_url, username = None, None, None, None 
  
    @get_user
    def get(self):
        template_values = {
            'is_debug' : conf.DEBUG,
            'user'     : self.user,
            'username' : self.username,
            'login_url' : self.login_url,
            'logout_url' : self.logout_url
        }
        
        path = os.path.join( conf.APP_ROOT, 'templates', 'addstory.html' )
        self.response.out.write( template.render( path, template_values ) )

    @get_user
    @moderator
    def post(self):
        months = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', \
                    'Sep', 'Oct', 'Nov', 'Dec' ] 
        
        dt = datetime.now();
        dd = dt.strftime("%d")
        mm = months[ dt.month - 1 ]
        
        story = Story(
            day = dd, 
            month = mm,
            year = str( dt.year ),
            heading = self.request.get('heading'),
            content = self.request.get('content'),
            entrytime = dt
        )
        story.put() 

        self.redirect( "/" )


