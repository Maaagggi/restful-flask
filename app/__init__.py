import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from .middleware import error_handling_middleware

# Create Flask app and setup extensions
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Register your middleware
app.wsgi_app = error_handling_middleware(app.wsgi_app)

# Import routes and models AFTER app and extensions are fully initialized
from app import routes, models

if __name__ == '__main__':
    app.debug = True
    app.run()
