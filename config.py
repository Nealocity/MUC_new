import os

class Config:
    # Existing configuration...
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/chat_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
   
    # Other configuration options...

    API_TITLE = 'Multi-User Chat API'
    API_VERSION = '1.0'
    API_DESCRIPTION = 'A simple API for a multi-user chat application.'
    OPENAPI_VERSION = '3.0.3'  # OpenAPI version used for documentation
    OPENAPI_URL_PREFIX = '/api'
    OPENAPI_SWAGGER_UI_PATH = '/swagger-ui'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
