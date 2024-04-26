# Creating a blueprint for authenication pages
from flask import Blueprint
bp = Blueprint('auth', __name__)
from app.auth import routes