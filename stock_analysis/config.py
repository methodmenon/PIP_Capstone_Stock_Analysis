class DevelopmentConfig(object):
    DATABASE_URI = "postgresql://vivek:math@localhost/vivek"
    DEBUG = True

class TestingConfig(object):
    DATABASE_URI = "sqlite://"
    DEBUG = True