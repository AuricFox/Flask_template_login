# Creating a blueprint for user pages
from flask import Blueprint
bp = Blueprint('manage', __name__)
from app.manage import routes