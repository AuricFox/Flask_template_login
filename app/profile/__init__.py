# Creating a blueprint for profile pages
from flask import Blueprint
bp = Blueprint('profile', __name__)
from app.profile import routes