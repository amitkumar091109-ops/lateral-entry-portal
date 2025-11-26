"""
Authentication Module
Exports authentication services and decorators
"""

from .google_oauth import google_oauth_service, GoogleOAuthService, InvalidTokenError
from .session_manager import session_manager, SessionManager
from .token_encryption import encrypt_token, decrypt_token
from .decorators import require_auth, require_admin, require_own_profile, optional_auth

__all__ = [
    'google_oauth_service',
    'GoogleOAuthService',
    'InvalidTokenError',
    'session_manager',
    'SessionManager',
    'encrypt_token',
    'decrypt_token',
    'require_auth',
    'require_admin',
    'require_own_profile',
    'optional_auth',
]
