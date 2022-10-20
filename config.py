import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = "postgresql://uqytcpjw:MJcLqItXtfgIT-NGGFwNSrrDpBXWIhAk@peanut.db.elephantsql.com/uqytcpjw"
    SQLALCHEMY_TRACK_MODIFICATIONS = False