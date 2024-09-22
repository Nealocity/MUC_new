# extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
# socketio = SocketIO()
socketio = SocketIO(cors_allowed_origins="*")  # Configure CORS for SocketIO