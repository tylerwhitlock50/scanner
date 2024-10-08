from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .ocr_routes import ocr
from .crud_routes_v2 import crud
from .extensions import db
import os
from dotenv import load_dotenv


load_dotenv()


def create_app():
    app = Flask(__name__)

    # App configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)  # Bind SQLAlchemy to this Flask app

    # Create database tables within the application context
    with app.app_context():
        from .models import SerialNumberRecord, SnStatus  # Import models
        db.create_all()  # Create the database tables

    CORS(app)  # Enable Cross-Origin Resource Sharing

    # Register blueprints
    app.register_blueprint(ocr)
    app.register_blueprint(crud)

    return app
