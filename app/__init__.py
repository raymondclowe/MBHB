"""
MBHB Flask Application
Student Performance Analysis and Worksheet Generation System
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        if config_name == 'production':
            raise ValueError('SECRET_KEY environment variable must be set in production')
        secret_key = 'dev-secret-key-change-in-production'
    
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mbhb.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['HOMEWORK_FOLDER'] = os.environ.get('HOMEWORK_FOLDER', './homework_submissions')
    app.config['WORKSHEET_FOLDER'] = os.environ.get('WORKSHEET_FOLDER', './generated_worksheets')
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Register blueprints
    from app.routes import main, students, analysis, worksheets, api
    app.register_blueprint(main.bp)
    app.register_blueprint(students.bp)
    app.register_blueprint(analysis.bp)
    app.register_blueprint(worksheets.bp)
    app.register_blueprint(api.bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Initialize default categories if database is empty
        from app.models.mistake_category import MistakeCategory
        if MistakeCategory.query.count() == 0:
            from app.utils.init_categories import initialize_default_categories
            initialize_default_categories()
    
    return app
