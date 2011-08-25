# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users

import os, re
import conf
import logging
from model import Contest, LastUpdate
from common import get_user, moderator
from datetime import datetime
from datetime import date, timedelta, datetime
from conf import DEBUG
from google.appengine.api import urlfetch


class AddContest( webapp.RequestHandler ):
   
    user, login_url, logout_url, username = None, None, None, None 
   
    
    def get_date( self, day, time ):
        
        # parsing it from the string
        pattern = r"""
            (\d+).(\d+).(\d+)    # day, month, year
            """
        reg = re.compile( pattern, re.VERBOSE )
        match = reg.search( day )
        d, m, y = int( match.group(1) ), int( match.group(2) ), int( match.group(3) )

        pattern = r"""
            (\d+):(\d+)         # hour, minute
            """
        reg = re.compile( pattern, re.VERBOSE )
        match = reg.search( time )
        hh, mm = int( match.group(1) ), int( match.group(2) )
        
        # creating the datetime object
        date = datetime( y, m, d, hh, mm )

        # taking offset +3h to make it bangladeshi time
        date = date + timedelta( hours=3 ) 
        return date

    
    def get_detail( self, date ):
        return date.strftime("%B %d, %Y - %A")  # August 15, 2011 - Monday  
    
    def get_time( self,  date ):
        return date.strftime("%I:%M%p")  # 04:30PM

    def load_contests(self):
      
        # let's see if we need to update it or not
        q = db.Query( LastUpdate )
        last = q.fetch( 1 )

        f = "" 
#        try:
#            webpage = urlfetch.fetch( "http://fs13.net/events/" ) 
#            f = webpage.content 
#        except:
#            return

        if not last:
            # fetching the contest events for the first time
            try:
                webpage = urlfetch.fetch( "http://fs13.net/events/" ) 
                f = webpage.content 
                update =  LastUpdate(
                    date = datetime.now()
                )
                update.put()
            except:
                # cannot find the page
                return
        else:
            # if it's not been updated for a whole day
            cdate = datetime.now() - timedelta( days=1 )
            for l in last:
                if l.date < cdate:
                    # fetching the contest events
                    try:
                        webpage = urlfetch.fetch( "http://fs13.net/events/" ) 
                        f = webpage.content 
                        update =  LastUpdate(
                            date = datetime.now()
                        )
                        update.put()
                        l.delete() # removing the old data
                    except:
                        # cannot find the page
                        print "cannot find the page"
                        return
                else:
                    # i don't need update
                    return
            
    
        # cleaning up the previous data
        q = db.Query( Contest )
        contests = q.fetch( 1000 )
        db.delete( contests )
        
        # we won't pick the russian contests
        russia = [ 'contests.snarknews.info' , 'dl.gsu.by' ]  
        
        pattern = ur"""
            \s+<tr\ class=\'[A-Za-z_]+\'>\s+
            \s+<td\ style=\'color:\ rgb.*\s+
            \s+(\d+.\d+.\d+)\s+                 # date
            \s+</td>\s+
            \s+<td\ style=\'color:\ rgb.*\s+
            \s+(\d+:\d+)\s?                     # time
            \s+</td>\s+
            \s+
            \s+<td\ align=.*>\s?
            \s+(.*)                             # name
            \s+</td>\s?
            \s+<td>\s?
            \s+<a\ .*
            \s+\'>(.*)\s?                       # url
            """

        reg = re.compile( pattern, re.VERBOSE | re.UNICODE )
        matches = reg.finditer( f )       
        
        # pushing the contests into datastore
        for match in matches:
            date = self.get_date( match.group(1), match.group(2) )
            detailed_date = self.get_detail( date )
            time = self.get_time( date )
            name = match.group( 3 )
            location = match.group( 4 ).strip()
            
            if location in russia: 
                continue
            else:
                contest = Contest( 
                    date = date, 
                    detailed_date = detailed_date, 
                    time = time.lower(),
                    name = name,
                    location = location
                )
                contest.put()
    

    @get_user
    def get(self):
        
        self.load_contests()

        q = db.Query( Contest )
        q.order( "date" )
        contests = q.fetch(10) 
    
        template_values = {
            'is_debug' : conf.DEBUG,
            'user'     : self.user,
            'username' : self.username,
            'login_url' : self.login_url,
            'logout_url' : self.logout_url,
            'contests'  : contests 
        }
        
        path = os.path.join( conf.APP_ROOT, 'templates', 'contests.html' )
        self.response.out.write( template.render( path, template_values ) )



