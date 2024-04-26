# Creating a blueprint for main pages
from flask import Blueprint
bp = Blueprint('main', __name__)
from app.main import routes