# routes/routes.py

from flask import jsonify, request, render_template
#from flask_smorest import Blueprint
from . import main

# main = Blueprint('main', __name__, description="Main routes for the chat application")

@main.route('/')
def index():
    return jsonify({"message": "Welcome to the chat app!"})

# @main.route('/users', methods=['GET'])
# def get_users():
#     # Logic to get users goes here
#     return jsonify({"users": []})

# @main.route('/register', methods=['POST'])
# def register():
#     # Logic to register a user goes here
#     return jsonify({"message": "User registered successfully!"})

@main.route('/login', methods=['GET'])
def login():
    return render_template('MUC_loginui.html')

# Route to render the register page
@main.route('/register', methods=['GET'])
def show_register():
    return render_template('MUC_register.html')

@main.route('/listusers', methods=['GET'])
def login():
    return render_template('MUC_listuserui.html')


@main.route('/chats', methods=['GET'])
def login():
    return render_template('MUC_Chatwindowui.html')
