chat-app/
├── app.py                   # Main Flask application
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── extension.py
├── models.py                # Database models
├── routes/
│   ├── __init__.py          # Initialize Blueprints
│   ├── auth.py              # Authentication routes (registration, login)
│   ├── chat.py              # Chat routes (start chat, send message)
│   ├── routes.py
│   └── user.py
├── templates/               # HTML templates (if using Flask for rendering)
│   ├── index.html
│   ├── MUC_Chatwindowui.html
│   ├── MUC_listuserui.html
│   ├── MUC_loginui.html
│   └── MUC_register.html
└── migrations/              # Database migrations
