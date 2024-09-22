# routes/chat.py

from datetime import datetime
from flask import request, jsonify
from flask_smorest import Blueprint 
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token 
from app import db, socketio
from models import User, Chat, Message, UserChat
from flask_socketio import emit, join_room

chat_bp = Blueprint('chat', __name__)

# @chat_bp.route('/start', methods=['POST'])
# @jwt_required()
# def start_chat():
#     data = request.get_json()
#     recipient_username = data.get('recipientUsername')
#     recipient = User.query.filter_by(username=recipient_username).first()

#     if not recipient:
#         return jsonify({'error': 'User not found.'}), 404

#     print('recipient data:', recipient.id)

#     sender_id = get_jwt_identity()
#     # Check if a chat already exists between these users
#     existing_chat = Chat.query.join(UserChat).filter(
#         ((UserChat.user_id == sender_id) & (UserChat.chat_id == Chat.chat_id)) |
#         ((UserChat.user_id == recipient.id) & (UserChat.chat_id == Chat.chat_id))
#     ).first()

#     if existing_chat:
#         chat = existing_chat
#     else:
#         # Create a new chat
#         chat = Chat()
#         db.session.add(chat)
#         db.session.commit()
#         chat_id = chat.chat_id


#         # Add both users to the chat
#         db.session.add(UserChat(user_id=sender_id, chat_id=chat_id))
#         db.session.add(UserChat(user_id=recipient.id, chat_id=chat_id))
#         db.session.commit()

#     return jsonify({'message': f'Chat started with {recipient.username}', 'chatId': chat.chat_id}), 200

@chat_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    data = request.get_json()
    print('Received data:', data)  # Log the received data
    chat_id = data.get('chatId')
    message_content = data.get('message')
    recipient_username = data.get('recipientUsername')  # Get recipient username from the request
    sender_id = get_jwt_identity()

    recipient = User.query.filter_by(username=recipient_username).first()
    print('recipient:', recipient)  # Debug line to check the user identity
    if not recipient:
        return jsonify({'error': 'Recipient not found.'}), 404

    new_message = Message(chat_id=chat_id, sender_id=sender_id, content=message_content, timestamp=datetime.utcnow())
    db.session.add(new_message)
    db.session.commit()

    # # Notify the other users in the chat
    # participants = UserChat.query.filter(UserChat.chat_id == chat_id).all()
    # for participant in participants:
    #     if participant.user_id != sender_id:
    #         socketio.emit('receive_message', {
    #             'chatId': chat_id,
    #             'message': message_content,
    #             'senderId': sender_id,
    #             # 'recipientId': recipient.user_id,
    #             'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    #         }, room=f'user_{participant.user_id}')
    #         print(f'Message sent to user_{participant.user_id}')  # Log the room notification

        # Notify the recipient
    socketio.emit('receive_message', {
        'chatId': chat_id,
        'message': message_content,
        'senderUsername': User.query.get(sender_id).username,
        'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }, room=f'user_{recipient.user_id}')
    return jsonify({'message': 'Message sent.', 'status': 'single_tick'}), 200

# @socketio.on('join_chat')
# def on_join_chat(data):
#     chat_id = data['chatId']
#     room = f'chat_{chat_id}'
#     join_room(room)
#     emit('user_joined', {'message': f'User joined chat {chat_id}'}, room=room)

@chat_bp.route('/chats', methods=['GET'])
@jwt_required()
def get_or_create_chat():
    user_identity = get_jwt_identity()
    print('User Identity:', user_identity)  # Debug line to check the user identity
    user_name = request.args.get('userName')
    if not user_name:
        return jsonify({'error': 'UserName is required.'}), 400

    recipient = User.query.filter_by(username=user_name).first()
    if not recipient:
        return jsonify({'error': 'User not found.'}), 404
    print('recipient:', recipient)  # Debug line to check the user identity


    sender_id = get_jwt_identity()
    print('Sender Identity:', sender_id)  # Debug line to check the user identity

    # Check if a chat already exists between these users
    existing_chat = Chat.query.join(UserChat).filter(
        ((UserChat.user_id == sender_id) & (UserChat.chat_id == Chat.chat_id)) |
        ((UserChat.user_id == recipient.user_id) & (UserChat.chat_id == Chat.chat_id))
    ).first()
    print('existing_chat:', existing_chat)  # Debug line to check the user identity

    if existing_chat:
        chat = existing_chat
    else:
        # Create a new chat
        chat = Chat()
        db.session.add(chat)
        db.session.commit()
        chat_id = chat.chat_id

        # Add both users to the chat
        db.session.add(UserChat(user_id=sender_id, chat_id=chat_id))
        db.session.add(UserChat(user_id=recipient.user_id, chat_id=chat_id))
        db.session.commit()

    return jsonify({'chatId': chat.chat_id, 'recipientUsername': recipient.username}), 200

# @socketio.on('connect')
# def handle_connect():
#     token = request.args.get('token')  # Get the token from the query parameter
#     if not token:
#         return False  # Disconnect the client if no token is found
    
#     try:
#         decoded_token = decode_token(token)
#         user_id = decoded_token['sub']  # Assuming 'sub' is the user identity field in your JWT
#         join_room(f'user_{user_id}')
#         print(f'User {user_id} connected and joined room user_{user_id}')
#     except Exception as e:
#         print(f"Token decoding error: {e}")
#         return False  # Disconnect the client if token is invalid
    
@socketio.on('join_room')
def on_join(data):
    room = data['room']
    join_room(room)
