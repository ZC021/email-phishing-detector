from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging

load_dotenv()

def create_app():
    """Initialize the Flask application"""
    app = Flask(__name__, static_folder='static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-testing')
    app.config['MODEL_PATH'] = os.path.join('models', 'phishing_model.pkl')
    app.config['VECTORIZER_PATH'] = os.path.join('models', 'vectorizer.pkl')
    app.config['UPLOAD_FOLDER'] = os.path.join('data', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )
    
    # Initialize CORS
    CORS(app)
    
    # Register blueprints
    from app.routes.api import api_bp
    from app.routes.frontend import frontend_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(frontend_bp)
    
    # Create required directories
    os.makedirs('models', exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join('data', 'raw'), exist_ok=True)
    os.makedirs(os.path.join('data', 'processed'), exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Register custom filters
    from app.utils.filters import register_filters
    register_filters(app)
    
    # Register error handlers
    from app.routes.errors import register_error_handlers
    register_error_handlers(app)
    
    return app