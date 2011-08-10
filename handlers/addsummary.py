from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db

from datetime import datetime

import os, re, md5
import conf
import logging
from model import Story, Summary, Coder 
points = [20,15,12,10,8,6,4,3,2,1]

class AddSummary( webapp.RequestHandler ):
    def get(self):
        template_values = {
            'is_debug' : conf.DEBUG
        }
        
        path = os.path.join( conf.APP_ROOT, 'templates', 'addsummary.html' )
        self.response.out.write( template.render( path, template_values ) )
    
    # update data from one file
    def process(self, f):
        
        pattern = r"""
            <td>(\d+)</td>            # rank
            <td>([A-Za-z. ]+)</td>    # name
            .*                        # rest of the line
            <td>(\d+)/(\d+)</td>      # attempt, problemcount
            """
        reg = re.compile( pattern, re.VERBOSE )
       
        rankpat = r"""
            [A-Za-z]+\ ([A-Za-z]+\ \d+)            # weekday, month, day
            \ \d\d:\d\d:\d\d\ [A-Za-z]+\ (\d+)</p> # year
            """
        rankreg = re.compile( rankpat, re.VERBOSE ) 
        
        #finding the date of the event
        match = rankreg.search( f )
        cdate = ""
        if match:
            cdate = match.group(1) + " " + match.group(2)

        bests = ""
        results = reg.finditer(f)
        for result in results:
            # picking up details
            
            rank = int(result.group(1))
            name = result.group(2)
            attempts = int(result.group(3))
            solved = int(result.group(4))
            earned = 0

            # pick up the earned points
            if rank <= 10 and int(solved) != 0:
                earned = points[ rank-1 ]
                if rank <= 3:
                    if rank == 2:
                        bests += ", "
                    elif rank == 3:
                        bests += " and "
                    bests += name
           

            c = db.Query( Coder )
            c.filter( 'name =' , name )
            coders = c.fetch(1)
            
            # updating database
            if len( coders ) == 0:
                # it was never in ranklist
                coder = Coder()
                coder.name = name
                coder.solve = solved
                coder.points = earned
                coder.contest = 1
                coder.attempt = attempts
                coder.accuracy = str( round(( coder.solve * 100. ) /  coder.attempt, 2) )
                coder.md5 = "?d=mm"
                coder.put()
            else:
                for coder in coders: # it's one object though
                    coder.solve += solved
                    coder.points += earned
                    coder.contest += 1
                    coder.attempt += attempts
                    coder.accuracy = str( round(( coder.solve * 100. ) / coder.attempt,2) )
                    if coder.email:
                        coder.md5 = md5.new( email ).hexdigest()
                    coder.put()
            
            
        return [ bests, cdate ]



    def post(self):
        
        ifile = self.request.get("summary")
        if not ifile:
            logging.error("no file selected")
            self.redirect( "/addsummary" )
        else:
            mytuple = self.process( ifile ) 
            bests = mytuple[0]
            contestdate = mytuple[1]

            s = Summary(
                summary = ifile,
                bests = bests,
                name = contestdate
            )
            s.put()
            self.redirect( "/archive" )



