import os

class Config(object):
    #per environment settings
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'

    if   FLASK_ENV == 'development':
        DEBUG   = True
        TESTING = True #disable recaptcha
    elif FLASK_ENV == 'production' :
        DEBUG   = False
