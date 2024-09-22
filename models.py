# models.py

#from flask_sqlalchemy import SQLAlchemy
from extensions import db


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Chat(db.Model):
    __tablename__ = 'chats'
    chat_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Message(db.Model):
    __tablename__ = 'messages'
    message_id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.chat_id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    # recipient_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # New field
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(50), default='sent', nullable=False)

class UserChat(db.Model):
    __tablename__ = 'user_chat'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.chat_id'), primary_key=True)
    role = db.Column(db.String(50), default='participant', nullable=False)

class UserStatus(db.Model):
    __tablename__ = 'user_status'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    last_active = db.Column(db.DateTime, nullable=False)
    # Relationship to link user status with users
    user = db.relationship('User', backref='status', uselist=False)
