from google.appengine.ext import db

class Story( db.Model ):
    day = db.StringProperty(required=True)
    month = db.StringProperty(required=True)
    year = db.StringProperty(required=True)
    heading = db.StringProperty(required=True)
    content = db.StringProperty(multiline=True, required=True)
    entrytime = db.DateTimeProperty()
