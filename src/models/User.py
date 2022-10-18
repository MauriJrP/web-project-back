import email
from src.app import db

class Users(db.Model):
    """
    User database model
    """

    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(24))
    pwd = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), unique=True, nullable=False)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def __init__(self, username, pwd):
        self.username = username
        self.pwd = pwd

    def __repr__(self):
        return "<User: Username - {}; password - {};>".format(self.username, self.pwd)