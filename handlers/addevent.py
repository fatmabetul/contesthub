from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users 

import os
import conf
import re 
import logging
from model import Event 
from common import get_user, moderator
from datetime import datetime
from datetime import date

class AddEvent( webapp.RequestHandler ):
    
    user, login_url, logout_url, username = None, None, None, None 

    @get_user
    def get(self):

        template_values = {
            'is_debug' : conf.DEBUG,
            'user'     : self.user,
            'username' : self.username,
            'login_url' : self.login_url,
            'logout_url' : self.logout_url,
        }
        
        path = os.path.join( conf.APP_ROOT, 'templates', 'addevent.html' )
        self.response.out.write( template.render( path, template_values ) )

    @get_user
    @moderator
    def post(self):
        
        pattern = r"""
            (\d+)/(\d+)/(\d+)  # month, day, year 
            """
        reg = re.compile( pattern, re.VERBOSE )
        match = reg.search( self.request.get( 'datepicker' ) ) 
        
        d = datetime( int( match.group(3) ), int( match.group(1) ), \
                int( match.group( 2 ) ) ) 

        # adding event
        event = Event(
            date = d,
            detailed_date = self.request.get( 'alternate' ),
            name = self.request.get( 'name' ),
            time = self.request.get( 'time' ),
            location = self.request.get('loc'),
        )
        
        event.put() 

        self.redirect( "/events" )

 
       


