# routes/auth.py

from datetime import datetime
from flask import request, jsonify, render_template
from flask_smorest import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from models import User, UserStatus  

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username is already taken.'}), 409

    password_hash = generate_password_hash(password)
    new_user = User(username=username, password_hash=password_hash, first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully.'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid username or password.'}), 401

    access_token = create_access_token(identity=user.user_id)
    
        # Update or insert user status
    user_status = UserStatus.query.filter_by(user_id=user.user_id).first()
    if user_status:
        user_status.status = 'online'
        user_status.last_active = datetime.utcnow()
    else:
        user_status = UserStatus(user_id=user.user_id, status='online', last_active=datetime.utcnow())
        db.session.add(user_status)
    db.session.commit()
    return jsonify({'message': 'Login successful.', 'token': access_token, 'user_id': user.user_id}), 200