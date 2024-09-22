import logging
from datetime import datetime
from flask import request, jsonify
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token
from app import db, socketio
from models import User, Chat, Message, UserChat
from flask_socketio import emit, join_room, disconnect
from jwt import InvalidTokenError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chats', methods=['GET'])
@jwt_required()
def get_or_create_chat():
    user_identity = get_jwt_identity()
    user_name = request.args.get('userName')
    
    logger.info(f"User {user_identity} is attempting to start a chat with {user_name}")

    if not user_name:
        logger.error("UserName is missing in request")
        return jsonify({'error': 'UserName is required.'}), 400

    recipient = User.query.filter_by(username=user_name).first()
    if not recipient:
        logger.error(f"Recipient with username {user_name} not found.")
        return jsonify({'error': 'User not found.'}), 404

    sender_id = user_identity
    existing_chat = Chat.query.join(UserChat).filter(
        ((UserChat.user_id == sender_id) & (UserChat.chat_id == Chat.chat_id)) |
        ((UserChat.user_id == recipient.user_id) & (UserChat.chat_id == Chat.chat_id))
    ).first()

    if existing_chat:
        logger.info(f"Existing chat found for User {sender_id} and User {recipient.user_id}")
        chat = existing_chat
    else:
        # Create a new chat if one doesn't exist
        logger.info(f"No existing chat found. Creating a new chat for User {sender_id} and User {recipient.user_id}")
        chat = Chat()
        db.session.add(chat)
        db.session.commit()
        chat_id = chat.chat_id

        # Add both users to the chat
        db.session.add(UserChat(user_id=sender_id, chat_id=chat_id))
        db.session.add(UserChat(user_id=recipient.user_id, chat_id=chat_id))
        db.session.commit()

        logger.info(f"Chat {chat_id} created and both users added.")

    return jsonify({'chatId': chat.chat_id, 'recipientUsername': recipient.username}), 200


# Listen for the send_message event from the client
@socketio.on('send_message')
#@jwt_required()
def handle_send_message(data):
    logger.info(f"Executing send_message event for User ")
    logger.info(f'{data}')
    chat_id = data.get('chatId')
    message_content = data.get('message')
    recipient_username = data.get('recipientUsername')
    sender_id = data.get('userid')
    token = data.get('token')
    logger.info(f'sender is {sender_id} and recipient is {recipient_username}')

    if not token:
        logger.error('No JWT token provided in send_message event.')
        return False  # Optionally, disconnect the user or send an error message

    try:
        # Decode the token and extract user information
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']  # Assuming 'sub' contains the user ID

        # Log the message details
        chat_id = data.get('chatId')
        message = data.get('message')
        logger.info(f'User {user_id} is sending a message to chat {chat_id}')
    
    except InvalidTokenError as e:
        logger.error(f'Invalid JWT token: {e}')
        return False  # Optionally handle invalid token (e.g., disconnect user)

    logger.info(f"User {sender_id} is sending a message to chat {chat_id}")

    recipient = User.query.filter_by(username=recipient_username).first()
    if not recipient:
        logger.error(f"Recipient with username {recipient_username} not found.")
        emit('error', {'error': 'Recipient not found.'})
        return

    new_message = Message(chat_id=chat_id, sender_id=sender_id, content=message_content, timestamp=datetime.utcnow())
    db.session.add(new_message)
    db.session.commit()

    logger.info(f"Message from User {sender_id} added to Chat {chat_id}")

    # Broadcast the message to the room associated with this chat
    room = f'chat_{chat_id}'
    logger.info(f"Executing broadcast event for User ")
    emit('receive_message', {
        'chatId': chat_id,
        'message': message_content,
        'senderUsername': User.query.get(sender_id).username,
        'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }, room=room,  broadcast=True, skip_sid=request.sid)

    logger.info(f"Message broadcasted to room {room}")


# Join a specific chat room
@socketio.on('join_room')
#@jwt_required()
def on_join_room(data):
    logger.info(f"Executing join_room event for User ")
    chat_id = data.get('chatId')
    room = f'chat_{chat_id}'

    logger.info(f"User is joining room {room}")

    join_room(room)
    emit('user_joined', {'message': f'User joined chat {chat_id}'}, room=room)

    logger.info(f"User successfully joined room {room}")


@socketio.on('connect')
def handle_connect():
    logger.info(f"Executing connect event for User")
    token = request.args.get('token')

    logger.info("User attempting to connect via WebSocket.")

    if not token:
        logger.error("Connection attempt without JWT token.")
        disconnect()
        return

    try:
        # Decode the token and validate it
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']  # Assuming the user ID is stored in the 'sub' field
        logger.info(f"Token validated for User {user_id}, joining room user_{user_id}")
        #join_room(f"user_{user_id}")
    except InvalidTokenError:
        logger.error("Invalid token provided during connection attempt.")
        disconnect()
        return
