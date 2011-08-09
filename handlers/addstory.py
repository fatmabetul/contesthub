from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db

from datetime import datetime

import os
import conf
import logging
from model import Story

class AddStory( webapp.RequestHandler ):
    def get(self):
        template_values = {
            'is_debug' : conf.DEBUG
        }
        
        path = os.path.join( conf.APP_ROOT, 'templates', 'addstory.html' )
        self.response.out.write( template.render( path, template_values ) )


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


