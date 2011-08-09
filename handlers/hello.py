from google.appengine.ext import webapp

class Hello(webapp.RequestHandler):
    def get(self):
        name = 'World'
        self.response.out.write(
                "<html><body>Hello, %s!</body></html>" % name
        )

    def post(self):
        name = 'World'
        self.response.out.write(
                "<html><body>Hello, %s!</body></html>" % name
        )
