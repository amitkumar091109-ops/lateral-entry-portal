#!/usr/bin/env python3
"""
Flask API Server for Lateral Entry Officers Database
Main application server with all routes
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
from pathlib import Path

from .config import get_config
from .routes.auth_routes import auth_bp
from .routes.admin_routes import admin_bp
from .routes.profile_routes import profile_bp
from .routes.upload_routes import upload_bp
from .routes.linkedin_routes import linkedin_bp
from .routes.ai_routes import ai_bp
from .routes.job_routes import job_bp
from .routes.feed_routes import feed_bp

# Get configuration
config = get_config()

# Create Flask app
app = Flask(__name__,
            static_folder='../assets',
            static_url_path='/assets')

# Load configuration
app.config.from_object(config)

# Enable CORS
CORS(app, supports_credentials=True, origins=[
    'http://localhost:8000',
    'http://localhost:5000',
    config.BASE_URL
])

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(linkedin_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(job_bp)
app.register_blueprint(feed_bp)


# Health check endpoint
@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'lateral-entry-api',
        'version': '1.0.0'
    })


# Serve static files
@app.route('/')
def serve_index():
    """Serve main index.html"""
    return send_from_directory('..', 'index.html')


@app.route('/pages/<path:filename>')
def serve_pages(filename):
    """Serve pages"""
    return send_from_directory('../pages', filename)


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(403)
def forbidden(error):
    """403 error handler"""
    return jsonify({'error': 'Forbidden'}), 403


@app.errorhandler(401)
def unauthorized(error):
    """401 error handler"""
    return jsonify({'error': 'Unauthorized'}), 401


# Initialize logging
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    # Ensure logs directory exists
    log_dir = Path(__file__).parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)

    # Set up file handler
    file_handler = RotatingFileHandler(
        config.LOG_FILE,
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(getattr(logging, config.LOG_LEVEL))
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))

    app.logger.addHandler(file_handler)
    app.logger.setLevel(getattr(logging, config.LOG_LEVEL))
    app.logger.info('Lateral Entry API startup')


if __name__ == '__main__':
    # Validate required configuration
    errors = config.validate_required_config()
    if errors:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"   - {error}")
        print("\n📝 Please check your .env file and ensure all required variables are set.")
        print("   See .env.example for reference.\n")
        exit(1)

    print("=" * 60)
    print("🚀 Lateral Entry Officers Database API")
    print("=" * 60)
    print(f"Environment: {config.FLASK_ENV}")
    print(f"Database: {config.DATABASE_PATH}")
    print(f"Base URL: {config.BASE_URL}")
    print(f"Google OAuth: {'✅ Configured' if config.GOOGLE_CLIENT_ID else '❌ Not configured'}")
    print("=" * 60)
    print("\n▶️  Starting server...\n")

    # Run server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=config.DEBUG
    )
