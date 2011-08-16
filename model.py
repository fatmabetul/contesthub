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
    bests = db.StringProperty()

class Coder( db.Model ):
    name = db.StringProperty()
    contest = db.IntegerProperty()
    solve = db.IntegerProperty()
    attempt = db.IntegerProperty()
    points = db.IntegerProperty()
    rank = db.IntegerProperty()
    accuracy = db.StringProperty()

    email = db.StringProperty()
    md5 = db.StringProperty()

class Event( db.Model ):
    name = db.StringProperty()
    date = db.DateTimeProperty()
    detailed_date = db.StringProperty()
    time = db.StringProperty()
    location = db.StringProperty()

class Contest( db.Model ):
    name = db.StringProperty()
    date = db.DateTimeProperty()
    detailed_date = db.StringProperty()
    time = db.StringProperty()
    location = db.StringProperty()
