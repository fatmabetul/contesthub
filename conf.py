import os
APP_ROOT = os.path.dirname(__file__)
DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

