from app import db

class IDB:
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_collate': 'utf8_general_ci'}

class PKID:
    id = db.Column(db.Integer, primary_key=True)
    
class Money(IDB, PKID, db.Model):
    
    __tablename__ = 'money'
    
    currency  = db.Column(db.Unicode(140))
    value = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    
    def __init__(self, *args, **kwargs):
        super(Money, self).__init__(*args, **kwargs)

class MoneyTotal(IDB, PKID, db.Model):
    
    __tablename__ = 'moneytotal'
    
    currency  = db.Column(db.Unicode(140))
    total = db.Column(db.Integer, nullable=False)