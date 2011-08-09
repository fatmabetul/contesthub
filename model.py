from google.appengine.ext import db

class Story( db.Model ):
    day = db.StringProperty(required=True)
    month = db.StringProperty(required=True)
    year = db.StringProperty(required=True)
    heading = db.StringProperty(required=True)
    content = db.StringProperty(multiline=True, required=True)
    entrytime = db.DateTimeProperty()

class Summary( db.Model ):
    entrytime = db.DateTimeProperty(auto_now_add=True)
    summary = db.TextProperty()
    name = db.StringProperty()    

class Coder( db.Model ):
    name = db.StringProperty()
    contest = db.IntegerProperty()
    solve = db.IntegerProperty()
    attempt = db.IntegerProperty()
    points = db.IntegerProperty()

    bestrank = db.IntegerProperty()
    bestdate = db.StringProperty()
    worstrank = db.IntegerProperty()
    worstdate = db.StringProperty()
