from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users 

import os
import conf
import logging
from common import get_user
from model import Event, Contest
from datetime import date, timedelta, datetime

class Events( webapp.RequestHandler ):
    
    user, login_url, logout_url, username = None, None, None, None 

    @get_user
    def get(self):
       
        last = datetime.now() - timedelta(days=2)

        q = db.Query( Event )
        q.filter( "date >", last )
        q.order( "date" )
        events = q.fetch(100)
    
        q = db.Query( Contest )
        q.filter( "date >", last )
        q.order( "date" )
        contests = q.fetch(10) 

        template_values = {
            'is_debug' : conf.DEBUG,
            'user'     : self.user,
            'username' : self.username,
            'login_url' : self.login_url,
            'logout_url' : self.logout_url,
            'events' : events,
            'contests' : contests
        }
        
        path = os.path.join( conf.APP_ROOT, 'templates', 'events.html' )
        self.response.out.write( template.render( path, template_values ) )


