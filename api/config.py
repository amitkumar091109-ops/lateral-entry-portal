"""
Configuration Management for Lateral Entry Officers Database
Loads environment variables and provides configuration settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / '.env')

class Config:
    """Base configuration"""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'

    # Database
    DATABASE_PATH = str(BASE_DIR / 'database' / 'lateral_entry.db')

    # Session
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_LIFETIME_DAYS = 7

    # Base URL
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')

    # Google OAuth
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', f"{BASE_URL}/api/auth/google/callback")
    GOOGLE_SCOPES = ['openid', 'email', 'profile']

    # Token Encryption
    TOKEN_ENCRYPTION_KEY = os.getenv('TOKEN_ENCRYPTION_KEY')

    # File Uploads
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', str(BASE_DIR / 'uploads'))
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 10 * 1024 * 1024))  # 10MB
    ALLOWED_PHOTO_EXTENSIONS = set(os.getenv('ALLOWED_PHOTO_EXTENSIONS', 'jpg,jpeg,png,webp').split(','))
    ALLOWED_DOCUMENT_EXTENSIONS = set(os.getenv('ALLOWED_DOCUMENT_EXTENSIONS', 'pdf').split(','))

    # AI Configuration
    CUSTOM_AI_BASE_URL = os.getenv('CUSTOM_AI_BASE_URL')
    CUSTOM_AI_API_KEY = os.getenv('CUSTOM_AI_API_KEY')
    CUSTOM_AI_MODEL = os.getenv('CUSTOM_AI_MODEL', 'default')
    CUSTOM_AI_TIMEOUT = 10  # seconds
    CUSTOM_AI_MAX_TOKENS = 500
    CUSTOM_AI_TEMPERATURE = 0.7

    # Parallel AI Monitor
    PARALLEL_MONITOR_URL = os.getenv('PARALLEL_MONITOR_URL')
    PARALLEL_MONITOR_API_KEY = os.getenv('PARALLEL_MONITOR_API_KEY')

    # LinkedIn OAuth
    LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
    LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
    LINKEDIN_REDIRECT_URI = os.getenv('LINKEDIN_REDIRECT_URI', f"{BASE_URL}/api/linkedin/callback")

    # Social Media APIs
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
    FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID')
    FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')

    # Email/SMTP
    SMTP_HOST = os.getenv('SMTP_HOST')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    SMTP_FROM_EMAIL = os.getenv('SMTP_FROM_EMAIL')

    # Admin
    DEFAULT_ADMIN_EMAIL = os.getenv('DEFAULT_ADMIN_EMAIL', 'admin@example.com')
    DEFAULT_ADMIN_NAME = os.getenv('DEFAULT_ADMIN_NAME', 'System Administrator')

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')

    # Rate Limiting
    RATE_LIMIT_STORAGE_URL = os.getenv('RATE_LIMIT_STORAGE_URL', 'memory://')

    @classmethod
    def validate_required_config(cls):
        """Validate that required configuration is present"""
        errors = []

        if not cls.GOOGLE_CLIENT_ID:
            errors.append("GOOGLE_CLIENT_ID is required for authentication")
        if not cls.GOOGLE_CLIENT_SECRET:
            errors.append("GOOGLE_CLIENT_SECRET is required for authentication")
        if not cls.TOKEN_ENCRYPTION_KEY:
            errors.append("TOKEN_ENCRYPTION_KEY is required for token encryption")

        return errors


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # Force HTTPS in production


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    DATABASE_PATH = ':memory:'  # Use in-memory database for tests


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
