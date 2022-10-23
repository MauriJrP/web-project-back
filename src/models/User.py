import email
from src.app import db

class User(db.Model):
    """
    User database model
    """
    
    __tablename__ = 'user'

    id = db.Column('user_id', db.Integer, primary_key=True)
    firstName = db.Column(db.String(30), nullable=False)
    lastName = db.Column(db.String(30), nullable=False)
    pwd = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    
    def __init__(self, firstName, lastName, pwd, email, address):
        self.firstName = firstName
        self.lastName = lastName
        self.pwd = pwd
        self.email = email
        self.address = address

    def __repr__(self):
        return f"User('{self.firstName}', '{self.lastName}', '{self.pwd}', '{self.email}', '{self.address}')"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        print("Getting all users")
        return User.query.all()

    @staticmethod
    def get_one(id):
        return User.query.get(id)

    @staticmethod
    def get_by_username(value):
        return User.query.filter_by(username=value).first()

    @staticmethod
    def get_by_pwd(value):
        return User.query.filter_by(pwd=value).first()

    @staticmethod
    def get_by_email(value):
        return User.query.filter_by(email=value).first()
