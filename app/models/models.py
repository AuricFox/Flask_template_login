'''
Creating Database Models
'''
from app.extensions import db, bcrypt
from datetime import datetime
from flask_login import UserMixin

# ====================================================================
class User(UserMixin, db.Model):
    '''
    Model for user login info
    '''

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, email, password, is_admin=False):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin

    def __repr__(self):
        return f"Name: {self.name}\nEmail: {self.email}"

# ====================================================================
class Models(db.Model):
    '''
    Default model
    '''
    __tablename__ = 'Models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date)
    message = db.Column(db.Text)

    def __repr__(self):
        return f'Name: {self.name}, Date: {self.date}, Message: {self.message}'