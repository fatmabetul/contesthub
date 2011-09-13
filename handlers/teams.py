from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users 

import os
import conf
import logging
from model import Team 
from common import get_user

class Teams( webapp.RequestHandler ):
    
    user, login_url, logout_url, username = None, None, None, None 
        
    @get_user
    def get(self):
        q = db.Query( Team )
        q.order( "-points" )
        teams = q.fetch( 1000 )
       
        # find the rank of each team
        rank, last, total = 0, 100000, 0

        for team in teams:
            if team.points != last:
                rank = total + 1
            team.rank = rank
            last = team.points
            total += 1
            team.put()
        
        template_values = {
            'is_debug' : conf.DEBUG,
            'username'  : self.username,
            'user'      : self.user,
            'login_url' : self.login_url,
            'logout_url' : self.logout_url,
            'teams'  : teams
        }
        
        path = os.path.join( conf.APP_ROOT, 'templates', 'teams.html' )
        self.response.out.write( template.render( path, template_values ) )



