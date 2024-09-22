# routes/user.py

from flask import jsonify
from flask_smorest import Blueprint 
from extensions import db
from models import User, UserStatus
from flask_jwt_extended import get_jwt_identity, jwt_required

def get_current_user_id():
    return get_jwt_identity() 

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    # Assuming you have a way to get the current user_id, for example from the JWT token
    current_user_id = get_current_user_id()  # Replace with actual method to get user ID
    
    # Fetch online users
    online_users = db.session.query(User).join(UserStatus).filter(
        UserStatus.status == 'online'
    ).all()
    
    users = [{'username': user.username} for user in online_users]
    
    return jsonify({'users': users})
