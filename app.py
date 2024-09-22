# app.py

from flask import Flask
from routes import main as main_blueprint
from flask_smorest import Api
from flask_cors import CORS
from extensions import db, migrate, jwt, socketio
from routes import main as main_blueprint  # Import updated Blueprint from flask_smorest
from routes.auth import auth_bp  # Use the updated Blueprint import
from routes.chat import chat_bp  # And other blueprints
from routes.user import user_bp  # And other blueprints

app = Flask(__name__)
app.config.from_object('config.Config')

CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for the entire app

db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
socketio.init_app(app)


api = Api(app)

api.register_blueprint(main_blueprint, url_prefix='/')
api.register_blueprint(auth_bp, name='auth_blueprint', url_prefix='/auth')
api.register_blueprint(chat_bp, name='chat_blueprint', url_prefix='/chat')
api.register_blueprint(user_bp, name='user_blueprint', url_prefix='/user')

if __name__ == '__main__':
    app.run(debug=True)