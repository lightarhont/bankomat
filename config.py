
class Configuration(object):
    TESTING = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:speed1@localhost/bank'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secretkey'
    
valuerub = [100, 200, 500, 1000, 2000, 5000]
valueusd = [1, 2, 5, 10, 20, 50, 100]
valueeur = [5, 10, 20, 50, 100, 200, 500]