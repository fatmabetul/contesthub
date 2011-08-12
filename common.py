from google.appengine.api import users
from secret import ADMIN, MODERATOR

# decorator for logging in
def get_user( fn ):
    def wrapper( self ):
        self.user = users.get_current_user()
        # generating the log in/log out url 
        if not self.user :
            self.login_url = users.create_login_url(self.request.path)
        else :
            self.logout_url = users.create_logout_url(self.request.path)
            self.username = self.user.nickname()
        
        return fn(self)
    return wrapper

def moderator( fn ):
    def wrapper( self ):
        if self.username in ADMIN or self.username in MODERATOR :
            return fn(self)
        else :
            self.redirect('/error') 
    return wrapper

def admin( fn ):
    def wrapper( self ):
        if self.username in ADMIN :
            return fn(self)
        else :
            self.redirect('/error')
    return wrapper

