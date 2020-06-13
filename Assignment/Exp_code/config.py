import os   #for defining environmental variables

class Config(object):
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'This_is_a_secret_key'

        #‘MAX_CONTENT_PATH’
