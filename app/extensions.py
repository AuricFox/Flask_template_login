'''
Manages flask application extensions 
'''
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

login_manager = LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()
