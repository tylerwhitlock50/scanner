from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .routes import api

import os
from dotenv import load_dotenv


load_dotenv()


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # App configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)  # Bind SQLAlchemy to this Flask app
    CORS(app)         # Enable Cross-Origin Resource Sharing

    app.register_blueprint(api)

    return app
