# routes/__init__.py

from flask_smorest import Blueprint

main = Blueprint('main', __name__, description="Main routes for the chat application")

from . import routes
